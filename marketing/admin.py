from django.contrib import admin
from django.db.models import Q
from .models import NewsLetterSubscriber


class MailchimpErrorFilter(admin.SimpleListFilter):
    title = 'mailchimp error'
    parameter_name = 'mailchimp_error_status'

    def lookups(self, request, model_admin):
        return [
            ('has_error', 'Has error'),
            ('no_error', 'No error'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'has_error':
            return queryset.exclude(mailchimp_error__isnull=True).exclude(mailchimp_error='')
        if self.value() == 'no_error':
            return queryset.filter(Q(mailchimp_error__isnull=True) | Q(mailchimp_error=''))
        return queryset


@admin.register(NewsLetterSubscriber)
class NewsLetterSubscriberAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'created_at', 'is_active', 
        'mailchimp_subscribed', 'mailchimp_last_sync', 'mailchimp_error'
    ]
    list_per_page = 20
    list_editable = ['is_active']
    list_filter = ['is_active', 'mailchimp_subscribed', MailchimpErrorFilter, 'created_at']
    search_fields = ['email', 'mailchimp_error']
    actions = ['deactivate_selected']

    @admin.action(description='Deactivate selected subscribers')
    def deactivate_selected(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} subscriber(s) deactivated.')

