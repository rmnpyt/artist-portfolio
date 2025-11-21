from django.db import models
from django.utils.text import slugify


class ArtWorkSeries(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='series_cover/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Artwork Series"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ArtWork(models.Model):
    class Availability(models.TextChoices):
        AVAILABLE = "available", "Available"
        SOLD = "sold", "Sold"
        NOT_FOR_SALE = "not_for_sale", "Not for Sale"

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='artworks/')
    description = models.TextField()
    series = models.ForeignKey(
        ArtWorkSeries,
        on_delete=models.SET_NULL,
        related_name='artworks',
        null=True,
        blank=True
    )
    year_created = models.PositiveIntegerField(blank=True, null=True)
    medium = models.CharField(max_length=200, blank=True)
    dimension = models.CharField(max_length=100, blank=True)
    availability = models.CharField(
        max_length=20, 
        choices=Availability.choices, 
        default=Availability.AVAILABLE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = 'Art Works'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

