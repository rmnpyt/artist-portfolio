from django.contrib import admin
from .models import ArtistProfile, Post, TeachingPlaces, Award, ProfileSection
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin, SummernoteInlineModelAdmin
# Register your models here.

class ProfileSectionInline(SummernoteInlineModelAdmin, admin.StackedInline):
    model = ProfileSection
    summernote_fields = ['content']
    extra = 0


@admin.register(ArtistProfile)
class ArtistProfileAdmin(SummernoteModelAdmin):
    list_display = ['full_name', 'portrait_tag', 'created_at', 'is_published']
    summernote_fields = ['short_bio', 'long_bio', 'teaching_statement']
    inlines = [ProfileSectionInline]

    @admin.display(description='Portrait')
    def portrait_tag(self, obj):
        if obj.portrait:
            return format_html(
                '<img src="{}" style="height: 50px; width: auto; object-fit: cover;" />',
                obj.portrait.url,
            )
        return '-'
    

@admin.register(Award)
class AwardAdmin(SummernoteModelAdmin):
    list_display = ['title', 'year', 'organization', 'artist_name']

    def artist_name(self, Award: Award):
        return Award.profile.full_name
    

@admin.register(TeachingPlaces)
class TeachingPlacesAdmin(SummernoteModelAdmin):
    list_display = ['inst_name', 'website', 'artist_name']
    list_per_page = 10
    def artist_name(self, TeachingPlaces: TeachingPlaces):
        return TeachingPlaces.profile.full_name


@admin.register(ProfileSection)
class ProfileSectionAdmin(SummernoteModelAdmin):
    list_display = ['title', 'artist_name', 'order', 'is_published']
    list_editable = ['order', 'is_published']
    list_per_page = 10
    summernote_fields = ['content']

    def artist_name(self, obj):
        return obj.profile.full_name


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ['title', 'post_type', 'is_published', 'published_at', 'cover_image_tag']
    list_per_page = 10
    prepopulated_fields = {
        'slug': ['title',],
    }

    @admin.display(description='Cover Image')
    def cover_image_tag(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src={} style="height: 50px; width: auto; object-fit: cover;" />',
                obj.cover_image.url
            )
        return '-'
