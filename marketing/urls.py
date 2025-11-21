from django.urls import path
from . import views


urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('newsletter/subscribe', views.newsletter_subscribe_footer, name='newsletter_subscribe')
]