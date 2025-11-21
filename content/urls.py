from django.urls import path
from . import views


urlpatterns = [
    path('about/', views.about, name='about'),
    path('events/', views.events_list, name='events_list'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('blog/', views.news_list, name='news_list'),
    path('blog/<slug:slug>/', views.news_detail, name='news_detail'),
]