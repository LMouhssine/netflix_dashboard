import json
from collections import Counter

from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import NetflixTitle


# ──────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────

def _apply_filters(request):
    """Parse query params and return a filtered queryset."""
    qs = NetflixTitle.objects.all()
    type_filter = request.GET.get('type', '')
    country_filter = request.GET.get('country', '')
    year_from = request.GET.get('year_from', '')
    year_to = request.GET.get('year_to', '')
    rating_cat = request.GET.get('rating_category', '')

    if type_filter:
        qs = qs.filter(type=type_filter)
    if country_filter:
        qs = qs.filter(country__icontains=country_filter)
    if year_from:
        qs = qs.filter(release_year__gte=int(year_from))
    if year_to:
        qs = qs.filter(release_year__lte=int(year_to))
    if rating_cat:
        qs = qs.filter(rating_category=rating_cat)

    return qs


def _get_filter_options():
    """Return all unique values for slicer dropdowns."""
    countries = (
        NetflixTitle.objects
        .exclude(country__isnull=True)
        .exclude(country='')
        .values_list('country', flat=True)
        .distinct()
        .order_by('country')[:200]
    )
    years = (
        NetflixTitle.objects
        .exclude(release_year__isnull=True)
        .values_list('release_year', flat=True)
        .distinct()
        .order_by('release_year')
    )
    return {
        'countries': list(countries),
        'years': list(years),
    }


# ──────────────────────────────────────────────
#  Main dashboard view
# ──────────────────────────────────────────────

def dashboard(request):
    qs = _apply_filters(request)
    options = _get_filter_options()

    # KPIs
    total = qs.count()
    tv_shows = qs.filter(type='TV Show').count()
    movies = qs.filter(type='Movie').count()
    country_count = (
        qs.exclude(country__isnull=True)
        .exclude(country='')
        .values_list('country', flat=True)
        .distinct()
        .count()
    )

    # Pie: type breakdown
    type_data = list(qs.values('type').annotate(count=Count('id')).order_by('-count'))

    # Bar: top 10 genres
    genre_counter = Counter()
    for listed in qs.exclude(listed_in__isnull=True).values_list('listed_in', flat=True):
        for genre in listed.split(','):
            genre_counter[genre.strip()] += 1
    top_genres = genre_counter.most_common(10)

    # Line: content by release_year
    year_data = (
        qs.exclude(release_year__isnull=True)
        .filter(release_year__gte=2000, release_year__lte=2023)
        .values('release_year')
        .annotate(count=Count('id'))
        .order_by('release_year')
    )

    # Donut: rating category
    rating_data = list(
        qs.values('rating_category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Top 10 countries (for map / table)
    country_data = (
        qs.exclude(country__isnull=True)
        .exclude(country='')
        .values('country')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    # Recent additions (last 10)
    recent = qs.exclude(date_added__isnull=True).order_by('-date_added')[:10]

    context = {
        # KPIs
        'total': total,
        'tv_shows': tv_shows,
        'movies': movies,
        'country_count': country_count,
        'pct_movies': round(movies / total * 100, 1) if total else 0,
        'pct_tv': round(tv_shows / total * 100, 1) if total else 0,

        # Chart data (JSON)
        'type_labels': json.dumps([d['type'] for d in type_data]),
        'type_values': json.dumps([d['count'] for d in type_data]),

        'genre_labels': json.dumps([g[0] for g in top_genres]),
        'genre_values': json.dumps([g[1] for g in top_genres]),

        'year_labels': json.dumps([d['release_year'] for d in year_data]),
        'year_values': json.dumps([d['count'] for d in year_data]),

        'rating_labels': json.dumps([d['rating_category'] for d in rating_data]),
        'rating_values': json.dumps([d['count'] for d in rating_data]),

        'country_data': list(country_data),
        'recent': recent,

        # Filters state
        'current_type': request.GET.get('type', ''),
        'current_country': request.GET.get('country', ''),
        'current_year_from': request.GET.get('year_from', ''),
        'current_year_to': request.GET.get('year_to', ''),
        'current_rating_cat': request.GET.get('rating_category', ''),

        # Filter options
        **options,
    }
    return render(request, 'dashboard/index.html', context)


# ──────────────────────────────────────────────
#  Content analysis page
# ──────────────────────────────────────────────

def content_analysis(request):
    qs = _apply_filters(request)
    options = _get_filter_options()

    # Duration distribution for movies
    duration_data = {}
    for dur in qs.filter(type='Movie').exclude(duration__isnull=True).values_list('duration', flat=True):
        try:
            mins = int(dur.replace(' min', '').strip())
            bucket = (mins // 30) * 30
            label = f"{bucket}–{bucket+30}m"
            duration_data[label] = duration_data.get(label, 0) + 1
        except ValueError:
            pass
    duration_sorted = sorted(duration_data.items(), key=lambda x: int(x[0].split('–')[0]))

    # TV show seasons distribution
    seasons_data = {}
    for dur in qs.filter(type='TV Show').exclude(duration__isnull=True).values_list('duration', flat=True):
        label = dur.strip()
        seasons_data[label] = seasons_data.get(label, 0) + 1
    seasons_sorted = sorted(seasons_data.items(), key=lambda x: x[1], reverse=True)[:15]

    # Content by rating (raw)
    rating_raw = (
        qs.exclude(rating__isnull=True)
        .exclude(rating='')
        .values('rating')
        .annotate(count=Count('id'))
        .order_by('-count')[:12]
    )

    # Genre trend: top genre per year
    genre_year = (
        qs.exclude(primary_genre__isnull=True)
        .filter(release_year__gte=2010, release_year__lte=2023)
        .values('release_year', 'primary_genre')
        .annotate(count=Count('id'))
        .order_by('release_year', '-count')
    )

    # Build top genre per year dict
    top_genre_per_year = {}
    for row in genre_year:
        yr = row['release_year']
        if yr not in top_genre_per_year:
            top_genre_per_year[yr] = {'genre': row['primary_genre'], 'count': row['count']}

    # Added per year
    added_year = (
        qs.exclude(year_added__isnull=True)
        .values('year_added')
        .annotate(count=Count('id'))
        .order_by('year_added')
    )

    # Titles table (paginated simply with top 50)
    titles = qs.order_by('-release_year')[:50]

    context = {
        'duration_labels': json.dumps([d[0] for d in duration_sorted]),
        'duration_values': json.dumps([d[1] for d in duration_sorted]),

        'seasons_labels': json.dumps([d[0] for d in seasons_sorted]),
        'seasons_values': json.dumps([d[1] for d in seasons_sorted]),

        'rating_raw_labels': json.dumps([d['rating'] for d in rating_raw]),
        'rating_raw_values': json.dumps([d['count'] for d in rating_raw]),

        'added_labels': json.dumps([d['year_added'] for d in added_year]),
        'added_values': json.dumps([d['count'] for d in added_year]),

        'top_genre_table': sorted(top_genre_per_year.items()),

        'titles': titles,
        'total': qs.count(),

        'current_type': request.GET.get('type', ''),
        'current_country': request.GET.get('country', ''),
        'current_year_from': request.GET.get('year_from', ''),
        'current_year_to': request.GET.get('year_to', ''),
        'current_rating_cat': request.GET.get('rating_category', ''),

        **options,
    }
    return render(request, 'dashboard/analysis.html', context)


# ──────────────────────────────────────────────
#  API endpoint for AJAX search
# ──────────────────────────────────────────────

@require_GET
def api_search(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': []})

    results = (
        NetflixTitle.objects
        .filter(Q(title__icontains=q) | Q(director__icontains=q) | Q(cast__icontains=q))
        .values('title', 'type', 'release_year', 'rating', 'country', 'primary_genre')
        [:20]
    )
    return JsonResponse({'results': list(results)})


@require_GET
def api_kpis(request):
    """JSON endpoint for live KPI refresh."""
    qs = _apply_filters(request)
    total = qs.count()
    return JsonResponse({
        'total': total,
        'movies': qs.filter(type='Movie').count(),
        'tv_shows': qs.filter(type='TV Show').count(),
        'countries': (
            qs.exclude(country__isnull=True)
            .values('country').distinct().count()
        ),
    })
