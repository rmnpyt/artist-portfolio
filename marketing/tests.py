from unittest.mock import Mock, patch

from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import NewsLetterSubscriber


@override_settings(
    TURNSTILE_SECRET_KEY='',
    NEWSLETTER_RATE_LIMIT_ATTEMPTS=3,
    NEWSLETTER_RATE_LIMIT_SECONDS=3600,
)
class NewsletterSubscribeTests(TestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse('newsletter_subscribe')

    def post_email(self, email, **extra):
        data = {'email': email}
        data.update(extra)
        return self.client.post(
            self.url,
            data,
            HTTP_REFERER='/',
            HTTP_X_REAL_IP='203.0.113.10',
        )

    @patch('marketing.views.subscribe_email_to_mailchimp')
    def test_blocked_domain_is_not_saved(self, subscribe_mock):
        response = self.post_email('bot@immenseignite.info')

        self.assertEqual(response.status_code, 302)
        self.assertFalse(NewsLetterSubscriber.objects.exists())
        subscribe_mock.assert_not_called()

    @patch('marketing.views.subscribe_email_to_mailchimp', return_value=(True, None))
    def test_successful_subscription_uses_double_opt_in(self, subscribe_mock):
        response = self.post_email('artist@example.org')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(NewsLetterSubscriber.objects.filter(email='artist@example.org', is_active=True).exists())
        subscribe_mock.assert_called_once_with('artist@example.org', double_opt_in=True)

    @patch('marketing.views.subscribe_email_to_mailchimp')
    def test_rate_limited_attempt_is_not_saved(self, subscribe_mock):
        subscribe_mock.return_value = (True, None)

        for index in range(3):
            self.post_email(f'person{index}@example.org')

        response = self.post_email('person4@example.org')

        self.assertEqual(response.status_code, 302)
        self.assertFalse(NewsLetterSubscriber.objects.filter(email='person4@example.org').exists())
        self.assertEqual(subscribe_mock.call_count, 3)

    @override_settings(TURNSTILE_SECRET_KEY='secret')
    @patch('marketing.views.subscribe_email_to_mailchimp')
    def test_missing_turnstile_token_is_not_saved(self, subscribe_mock):
        response = self.post_email('visitor@example.org')

        self.assertEqual(response.status_code, 302)
        self.assertFalse(NewsLetterSubscriber.objects.exists())
        subscribe_mock.assert_not_called()

    @override_settings(TURNSTILE_SECRET_KEY='secret')
    @patch('marketing.views.requests.post')
    @patch('marketing.views.subscribe_email_to_mailchimp', return_value=(True, None))
    def test_valid_turnstile_token_allows_subscription(self, subscribe_mock, requests_post_mock):
        turnstile_response = Mock()
        turnstile_response.json.return_value = {'success': True}
        turnstile_response.raise_for_status.return_value = None
        requests_post_mock.return_value = turnstile_response

        response = self.post_email('visitor@example.org', **{'cf-turnstile-response': 'token'})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(NewsLetterSubscriber.objects.filter(email='visitor@example.org').exists())
        subscribe_mock.assert_called_once_with('visitor@example.org', double_opt_in=True)

    @patch(
        'marketing.views.subscribe_email_to_mailchimp',
        return_value=(False, "person@example.org has signed up to a lot of lists recently; we're not allowing more signups for now"),
    )
    def test_mailchimp_suspicious_error_deactivates_subscriber(self, subscribe_mock):
        response = self.post_email('person@example.org')

        self.assertEqual(response.status_code, 302)
        subscriber = NewsLetterSubscriber.objects.get(email='person@example.org')
        self.assertFalse(subscriber.is_active)
        self.assertIn('signed up to a lot of lists', subscriber.mailchimp_error)
        subscribe_mock.assert_called_once_with('person@example.org', double_opt_in=True)

