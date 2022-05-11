from celery import shared_task
from django.core.mail import send_mail

from ecommerce.settings import EMAIL_HOST_USER


@shared_task
def send_email_task(request):
    send_mail(subject="Order confirmed!",message="Hi {0}, Your order received!".format(request.user), from_email=EMAIL_HOST_USER, recipient_list=[request.user.email])
    return


