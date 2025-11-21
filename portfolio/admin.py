from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import ArtWork, ArtWorkSeries
from django.utils.html import format_html


@admin.register(ArtWorkSeries)
class ArtWorkSeriesAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ['title', 'is_published', 'created_at']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ArtWork)
class ArtWorkAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = [
        'title', 'image_tag', 'series', 'year_created', 'price' 
    ]
    list_per_page = 20
    list_editable = ['price', 'series']
    list_display_links = ['title']
    prepopulated_fields = {
        'slug': ['title']
    }

    @admin.display(description='Image')
    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 50px; width: auto; object-fit: cover;" />',
                obj.image.url,
            )
        return '-'
    


