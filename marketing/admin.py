from django.contrib import admin
from .models import NewsLetterSubscriber

@admin.register(NewsLetterSubscriber)
class NewsLetterSubscriberAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'created_at', 'is_active', 
        'mailchimp_subscribed', 'mailchimp_last_sync', 'mailchimp_error'
        ]
    list_per_page = 20
    list_editable = ['is_active']

