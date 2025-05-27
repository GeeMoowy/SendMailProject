from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailings.models import MailingRecipient


def get_mailing_recipient_from_cache():
    if not CACHE_ENABLED:
        return MailingRecipient.objects.all()
    key = "recipient_list"
    recipient = cache.get(key)
    if recipient is not None:
        return recipient
    recipient = MailingRecipient.objects.all()
    cache.set(key, recipient)
    return recipient
