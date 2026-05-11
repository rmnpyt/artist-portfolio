from django.db import models
from django.utils.text import slugify


class ArtistProfile(models.Model):
    full_name = models.CharField(max_length=255)
    short_bio = models.TextField()
    long_bio = models.TextField(blank=True)

    portrait = models.ImageField(upload_to="portrait/", blank=True, null=True)

    email = models.EmailField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    teaching_statement = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name
    

class Award(models.Model):
    profile = models.ForeignKey(
        ArtistProfile,
        related_name='awards',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField(blank=True, null=True)
    organization = models.CharField(max_length=350, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        if self.year:
            return f'{self.title} - {self.year}'
        return self.title
    

class TeachingPlaces(models.Model):
    profile = models.ForeignKey(
        ArtistProfile,
        related_name='teaching_places',
        on_delete=models.CASCADE
    )
    inst_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.inst_name
    

class Post(models.Model):
    class PostType(models.TextChoices):
        NEWS = "news", "News"
        EXHIBITION = "exhibition", "Exhibition"
        WORKSHOP = "workshop", "Workshop"
        GROUP_CLASS= "group_class", "Group Class"
        FESTIVAL = "festival", "Festival"
        PRIVATE_CLASS = "private_class", "Private Class"
        OTHER_EVENT = "other_event", "Other Event"

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    post_type = models.CharField(
        max_length=40,
        choices=PostType.choices,
        default=PostType.EXHIBITION
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    location_name = models.CharField(max_length=255, blank=True)
    location_address = models.CharField(max_length=255, blank=True)
    external_link = models.URLField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='blog_covers/', blank=True, null=True)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
