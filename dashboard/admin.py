from django.contrib import admin
from .models import NetflixTitle


@admin.register(NetflixTitle)
class NetflixTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'release_year', 'country', 'rating', 'rating_category', 'date_added')
    list_filter = ('type', 'rating_category', 'release_year')
    search_fields = ('title', 'director', 'cast', 'country')
    list_per_page = 50
    ordering = ('-release_year',)
