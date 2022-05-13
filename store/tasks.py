from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from ecommerce import logger
from ecommerce.settings import EMAIL_HOST_USER


@shared_task
def send_confirmation_email_task(request):
    try:
        send_mail(subject="Order confirmed!", message="Hi {0}, Your order received!".format(request.user),
                  from_email=EMAIL_HOST_USER, recipient_list=[request.user.email])
        return
    except Exception as ex:
        logger.info("Exception raised in sending confirmation email -- {0}".format(ex.args))


@shared_task
def send_reset_email_task(subject, context, from_email, to, html_email_template_name):
    try:
        email_message = EmailMultiAlternatives(subject=subject, from_email=from_email, to=to)
        html_email = render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

        email_message.send()
        return
    except Exception as ex:
        logger.info("Exception raised in sending reset password mail -- {0}".format(ex.args))
