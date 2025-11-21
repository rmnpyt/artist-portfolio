from django.db import models
from django.utils import timezone


class NewsLetterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # mailchimp tracker
    mailchimp_subscribed = models.BooleanField(default=False)
    mailchimp_last_sync = models.DateTimeField(blank=True, null=True)
    mailchimp_error = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.email
    
    def mark_synced(self, success: bool, error_message: str | None = None):
        self.mailchimp_last_sync = timezone.now()
        self.mailchimp_subscribed = success
        self.mailchimp_error = error_message
        self.save(update_fields=['mailchimp_subscribed', 'mailchimp_error', 'mailchimp_last_sync'])

