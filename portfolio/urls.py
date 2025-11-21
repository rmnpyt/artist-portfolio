from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('artwork/<slug:slug>/', views.artwork_detail, name='artwork_detail'),
]