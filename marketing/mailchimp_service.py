import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from django.conf import settings
import json


def get_mailchimp_client():
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": settings.MAILCHIMP_API_KEY,
        "server": settings.MAILCHIMP_SERVER_PREFIX,
    })
    return client


def subscribe_email_to_mailchimp(email: str, double_opt_in:bool = False):
    """
    Subscribe or update a contact in a Mailchimp audience.
    Returns (success: bool, error_message: str | None)
    """
    client = get_mailchimp_client()
    list_id = settings.MAILCHIMP_AUDIENCE_ID

    # status:
    #   "subscribed"   -> immediate subscription
    #   "pending"      -> send confirmation email (double opt-in)
    status = "pending" if double_opt_in else "subscribed"

    data ={
        "email_address": email,
        "status": status,
    }

    try:
        response = client.lists.add_list_member(list_id, data)
        return True, None
    except ApiClientError as e:
        print("MAILCHIMP ERROR:", e.text)
        err_json = json.loads(e.text)
        detail = err_json.get('detail')
        return False, detail