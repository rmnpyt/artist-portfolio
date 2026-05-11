from django.shortcuts import render, get_object_or_404
from .models import ArtWork, ArtWorkSeries
from content.models import Post


def home(request):
    queryset_artwork = ArtWork.objects.filter(is_published=True)
    featured_artworks = ArtWork.objects.filter(is_published=True, is_featured=True)
    recent_events = Post.objects.filter(
        is_published=True
    ).order_by('-published_at', '-created_at')
    
    context = {
        'artworks': queryset_artwork,
        'featured_artworks': featured_artworks,
        'recent_events': recent_events
    }
    return render(request, 'home.html', context=context)


def artwork_detail(request, slug):
    artwork = get_object_or_404(ArtWork, slug=slug, is_published=True)
    context = {
        'artwork': artwork
    }
    return render(request, 'artwork_detail.html', context=context)


def gallery(request):
    artworks = ArtWork.objects.filter(is_published=True).order_by('-year_created')
    series = ArtWorkSeries.objects.filter(is_published=True)
    context = {
        'artworks': artworks,
        'series': series
    }
    return render(request, 'gallery.html', context=context)
