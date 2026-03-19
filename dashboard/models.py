from django.db import models


class NetflixTitle(models.Model):
    TYPE_CHOICES = [('Movie', 'Movie'), ('TV Show', 'TV Show')]
    RATING_CATEGORY_CHOICES = [
        ('Adult', 'Adult'),
        ('Teen', 'Teen'),
        ('Kids', 'Kids'),
        ('Unknown', 'Unknown'),
    ]

    show_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=300)
    director = models.CharField(max_length=300, blank=True, null=True)
    cast = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.DateField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=20, blank=True, null=True)
    duration = models.CharField(max_length=20, blank=True, null=True)
    listed_in = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Computed columns
    year_added = models.IntegerField(blank=True, null=True)
    rating_category = models.CharField(
        max_length=10, choices=RATING_CATEGORY_CHOICES, default='Unknown'
    )
    primary_genre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'netflix_titles'
        indexes = [
            models.Index(fields=['type'], name='netflix_tit_type_idx'),
            models.Index(fields=['release_year'], name='netflix_tit_release_idx'),
            models.Index(fields=['rating_category'], name='netflix_tit_rating_cat_idx'),
            models.Index(fields=['country'], name='netflix_tit_country_idx'),
            models.Index(fields=['year_added'], name='netflix_tit_year_added_idx'),
        ]

    def __str__(self):
        return f"{self.title} ({self.type}, {self.release_year})"

    def save(self, *args, **kwargs):
        # Auto-compute year_added
        if self.date_added:
            self.year_added = self.date_added.year

        # Auto-compute rating_category
        adult_ratings = {'R', 'NC-17', 'TV-MA'}
        teen_ratings = {'PG-13', 'TV-14'}
        kids_ratings = {'G', 'TV-G', 'TV-Y', 'TV-Y7', 'TV-Y7-FV', 'PG'}
        if self.rating in adult_ratings:
            self.rating_category = 'Adult'
        elif self.rating in teen_ratings:
            self.rating_category = 'Teen'
        elif self.rating in kids_ratings:
            self.rating_category = 'Kids'
        else:
            self.rating_category = 'Unknown'

        # Auto-compute primary_genre
        if self.listed_in:
            self.primary_genre = self.listed_in.split(',')[0].strip()

        super().save(*args, **kwargs)
