from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib import messages
from .models import NewsLetterSubscriber
from .mailchimp_service import subscribe_email_to_mailchimp


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

        # basic check
        if not email:
            messages.error(request, "Please enter your email address")
            return redirect(request.META.get("HTTP_REFERER","/"))
        
        # validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        
        subscriber, created = NewsLetterSubscriber.objects.get_or_create(
            email=email,
            defaults={'is_active': True},
        )
        if not created or not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save(update_fields=['is_active'])

        # sync with mailchimp
        success, error_message = subscribe_email_to_mailchimp(email, double_opt_in=False)
        subscriber.mark_synced(success, error_message)
        if success:
            messages.success(
                request,
                "Thanks for subscribing!"
            )
        else:
            # Optional: log error, or store in subscriber.mailchimp_error
            messages.warning(
                request,
                "You are subscribed. Thank you!"
            )

        # messages.success(request, "Thanks for subscribing to our newsletter!")
        return redirect(request.META.get("HTTP_REFERER", "/"))
    
    return redirect("/")