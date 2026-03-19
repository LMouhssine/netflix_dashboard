"""
Management command: import netflix CSV into the database.

Usage:
    python manage.py import_netflix
    python manage.py import_netflix --path /custom/path/to/netflix_titles.csv
    python manage.py import_netflix --clear   # wipe table before importing
"""
import csv
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from dashboard.models import NetflixTitle


ADULT_RATINGS = {'R', 'NC-17', 'TV-MA'}
TEEN_RATINGS = {'PG-13', 'TV-14'}
KIDS_RATINGS = {'G', 'TV-G', 'TV-Y', 'TV-Y7', 'TV-Y7-FV', 'PG'}


def rating_category(rating):
    if rating in ADULT_RATINGS:
        return 'Adult'
    elif rating in TEEN_RATINGS:
        return 'Teen'
    elif rating in KIDS_RATINGS:
        return 'Kids'
    return 'Unknown'


def parse_date(value):
    """Try common date formats."""
    for fmt in ('%B %d, %Y', '%d-%b-%y', '%Y-%m-%d'):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except (ValueError, AttributeError):
            pass
    return None


class Command(BaseCommand):
    help = 'Import netflix_titles.csv into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default=None,
            help='Path to netflix_titles.csv (defaults to settings.NETFLIX_CSV_PATH)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear the table before importing',
        )

    def handle(self, *args, **options):
        csv_path = Path(options['path']) if options['path'] else settings.NETFLIX_CSV_PATH

        if not csv_path.exists():
            raise CommandError(
                f"CSV file not found: {csv_path}\n"
                "Place netflix_titles.csv in the data/ folder or use --path."
            )

        if options['clear']:
            count = NetflixTitle.objects.count()
            NetflixTitle.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Cleared {count} existing records."))

        self.stdout.write(f"Reading {csv_path} ...")

        created = 0
        updated = 0
        skipped = 0
        batch = []
        BATCH_SIZE = 500

        with open(csv_path, encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                show_id = row.get('show_id', '').strip()
                if not show_id:
                    skipped += 1
                    continue

                date_added = parse_date(row.get('date_added', ''))
                year_added = date_added.year if date_added else None
                release_year_raw = row.get('release_year', '').strip()
                release_year = int(release_year_raw) if release_year_raw.isdigit() else None
                rating = row.get('rating', '').strip() or None
                listed_in = row.get('listed_in', '').strip() or None
                primary_genre = listed_in.split(',')[0].strip() if listed_in else None

                obj = NetflixTitle(
                    show_id=show_id,
                    type=row.get('type', '').strip(),
                    title=row.get('title', '').strip(),
                    director=row.get('director', '').strip() or None,
                    cast=row.get('cast', '').strip() or None,
                    country=row.get('country', '').strip() or None,
                    date_added=date_added,
                    release_year=release_year,
                    rating=rating,
                    duration=row.get('duration', '').strip() or None,
                    listed_in=listed_in,
                    description=row.get('description', '').strip() or None,
                    year_added=year_added,
                    rating_category=rating_category(rating or ''),
                    primary_genre=primary_genre,
                )
                batch.append(obj)

                if len(batch) >= BATCH_SIZE:
                    n_created, n_updated = self._flush(batch)
                    created += n_created
                    updated += n_updated
                    batch = []
                    self.stdout.write(f"  Processed {i} rows ...", ending='\r')
                    self.stdout.flush()

        if batch:
            n_created, n_updated = self._flush(batch)
            created += n_created
            updated += n_updated

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f"Done! Created: {created} | Updated: {updated} | Skipped: {skipped}"
        ))

    def _flush(self, batch):
        existing_ids = set(
            NetflixTitle.objects
            .filter(show_id__in=[o.show_id for o in batch])
            .values_list('show_id', flat=True)
        )
        to_create = [o for o in batch if o.show_id not in existing_ids]
        to_update = [o for o in batch if o.show_id in existing_ids]

        if to_create:
            NetflixTitle.objects.bulk_create(to_create, ignore_conflicts=True)
        if to_update:
            NetflixTitle.objects.bulk_update(
                to_update,
                fields=[
                    'type', 'title', 'director', 'cast', 'country',
                    'date_added', 'release_year', 'rating', 'duration',
                    'listed_in', 'description', 'year_added',
                    'rating_category', 'primary_genre',
                ],
            )
        return len(to_create), len(to_update)
