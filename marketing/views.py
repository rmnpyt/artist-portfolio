from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib import messages
from .models import NewsLetterSubscriber
from .mailchimp_service import subscribe_email_to_mailchimp
import logging
import requests


logger = logging.getLogger(__name__)
GENERIC_SUBSCRIPTION_MESSAGE = "Thanks for subscribing! Please check your email to confirm your subscription."
BLOCKED_EMAIL_DOMAINS = {
    'immenseignite.info',
    'sendproud.com',
}
MAILCHIMP_SUSPICIOUS_ERRORS = (
    'has signed up to a lot of lists recently',
)


def get_redirect_url(request):
    return request.META.get("HTTP_REFERER", "/")


def get_client_ip(request):
    return request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR') or ''


def email_domain(email):
    return email.rsplit('@', 1)[-1].lower()


def is_blocked_email(email):
    return email_domain(email) in BLOCKED_EMAIL_DOMAINS


def is_mailchimp_suspicious_error(error_message):
    if not error_message:
        return False
    normalized_error = error_message.lower()
    return any(error in normalized_error for error in MAILCHIMP_SUSPICIOUS_ERRORS)


def is_rate_limited(request):
    client_ip = get_client_ip(request)
    if not client_ip:
        return False

    cache_key = f'newsletter_subscribe_attempts:{client_ip}'
    attempts = cache.get(cache_key, 0)
    if attempts >= settings.NEWSLETTER_RATE_LIMIT_ATTEMPTS:
        return True

    cache.set(cache_key, attempts + 1, settings.NEWSLETTER_RATE_LIMIT_SECONDS)
    return False


def verify_turnstile(request):
    if not settings.TURNSTILE_SECRET_KEY:
        return True

    token = request.POST.get('cf-turnstile-response')
    if not token:
        return False

    try:
        response = requests.post(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data={
                'secret': settings.TURNSTILE_SECRET_KEY,
                'response': token,
                'remoteip': get_client_ip(request),
            },
            timeout=5,
        )
        response.raise_for_status()
    except requests.RequestException:
        logger.exception('Turnstile verification request failed')
        return False

    return response.json().get('success', False)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # build email content
            subject = f"New contact submission from {name}"
            full_message = f'From: {name} <{email}>\n\nMessage:\n{message}'

            # send email
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FORM_EMAIL,
                ['azam.kashefi@gmail.com', 'ramin.mc@gmail.com']
            )

            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def newsletter_subscribe_footer(request):
    if request.method == 'POST':
        email = request.POST.get("email", "").strip().lower()
        redirect_url = get_redirect_url(request)

        # basic check
        if not email:
            messages.error(request, "Please enter your email address")
            return redirect(redirect_url)
        
        # validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect(redirect_url)

        if is_blocked_email(email):
            logger.warning('Blocked newsletter email domain: %s', email)
            messages.success(request, GENERIC_SUBSCRIPTION_MESSAGE)
            return redirect(redirect_url)

        if is_rate_limited(request):
            logger.warning('Newsletter rate limit exceeded: IP=%s email=%s', get_client_ip(request), email)
            messages.success(request, GENERIC_SUBSCRIPTION_MESSAGE)
            return redirect(redirect_url)

        if not verify_turnstile(request):
            logger.warning('Turnstile verification failed: IP=%s email=%s', get_client_ip(request), email)
            messages.success(request, GENERIC_SUBSCRIPTION_MESSAGE)
            return redirect(redirect_url)
        
        subscriber, created = NewsLetterSubscriber.objects.get_or_create(
            email=email,
            defaults={'is_active': True},
        )
        if not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save(update_fields=['is_active'])

        # sync with mailchimp
        success, error_message = subscribe_email_to_mailchimp(email, double_opt_in=True)
        subscriber.mark_synced(success, error_message)

        if is_mailchimp_suspicious_error(error_message):
            subscriber.is_active = False
            subscriber.save(update_fields=['is_active'])
            messages.success(request, GENERIC_SUBSCRIPTION_MESSAGE)
            return redirect(redirect_url)

        if success:
            messages.success(
                request,
                GENERIC_SUBSCRIPTION_MESSAGE
            )
        else:
            # Optional: log error, or store in subscriber.mailchimp_error
            messages.warning(
                request,
                "You are subscribed. Thank you!"
            )

        # messages.success(request, "Thanks for subscribing to our newsletter!")
        return redirect(redirect_url)
    
    return redirect("/")
