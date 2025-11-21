from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import ArtistProfile, Post, Award


def about(request):
    profile = get_object_or_404(ArtistProfile, is_published=True)
    awards = profile.awards.all().order_by('-year', 'title')
    teaching_places = profile.teaching_places.all()
    
    context = {
        'profile': profile,
        'awards': awards,
        'teaching_places': teaching_places,
    }
    return render(request, 'about.html', context=context)


def events_list(request):
    # Get all events (everything except news)
    events = Post.objects.filter(
        is_published=True
    ).exclude(
        post_type=Post.PostType.NEWS
    ).order_by('-start_date', '-published_at')
    
    context = {
        'events': events,
    }
    return render(request, 'events_list.html', context=context)


def event_detail(request, slug):
    event = get_object_or_404(
        Post, 
        slug=slug, 
        is_published=True
    )
    
    # Get related events (same type, excluding current)
    related_events = Post.objects.filter(
        is_published=True,
        post_type=event.post_type
    ).exclude(
        slug=slug
    ).order_by('-start_date', '-published_at')[:3]
    
    context = {
        'event': event,
        'related_events': related_events,
    }
    return render(request, 'event_detail.html', context=context)


def news_list(request):
    # Get all news posts
    news_posts = Post.objects.filter(
        is_published=True,
        post_type=Post.PostType.NEWS
    ).order_by('-published_at', '-created_at')
    
    context = {
        'news_posts': news_posts,
    }
    return render(request, 'news_list.html', context=context)


def news_detail(request, slug):
    news = get_object_or_404(
        Post, 
        slug=slug, 
        is_published=True,
        post_type=Post.PostType.NEWS
    )
    
    # Get related news posts (excluding current)
    related_news = Post.objects.filter(
        is_published=True,
        post_type=Post.PostType.NEWS
    ).exclude(
        slug=slug
    ).order_by('-published_at', '-created_at')[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'news_detail.html', context=context)
