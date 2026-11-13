from django.conf import settings


def newsletter_bot_protection(request):
    return {
        'TURNSTILE_SITE_KEY': settings.TURNSTILE_SITE_KEY,
    }
