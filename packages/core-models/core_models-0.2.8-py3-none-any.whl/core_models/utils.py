import logging
import uuid
from collections import namedtuple
from random import randint

from django.conf import settings

MailAttachment = namedtuple('MailAttachment', ['name', 'content', 'mime'])


def log_exception(source: str, exception: Exception):
    """
    To log exception to console
    usage: log_exception(MyClass, exception_object)
    
    :param source: 
    :param exception: 
    :return: 
    """
    logger = logging.getLogger(source)
    logger.exception(exception)


def random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.lower()     # Make all characters uppercase.
    random = random.replace("-", "")    # Remove the UUID '-'.
    return random[0:string_length]  # Return the random string.


def random_numbers(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def send_invoice_update_to_seller(invoice, request=None):
    from .app import notification_manager
    print(f"Sending invoice update mailto {invoice.seller.email}")
    notification_manager.send_mail(
        subject=f"Your invoice #{invoice.reference}'s status has changed",
        template_dir='seller-invoice',
        to=[invoice.seller.email],
        context_dict={
            "invoice": invoice,
            "action_url": f"{settings.SELLER_VIEW_INVOICE_PAGE_URL}"
                          f"/{invoice.id}"
        },
        request=request
    )
    print(f"Invoice update mail sent to {invoice.seller.email}")
