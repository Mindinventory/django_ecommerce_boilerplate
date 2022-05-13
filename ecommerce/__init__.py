# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
import logging

__all__ = ('celery_app',)
logger = logging.getLogger("ecommerce")


def get_cookie(request):
    cookiedata = cookiecart(request)
    return cookiedata['cartitems'], cookiedata['items']
