from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ecommerce import logger


def send_mail_from_system(subject, context, from_email, to, html_email_template_name):
    try:
        email_message = EmailMultiAlternatives(subject=subject, from_email=from_email, to=to)
        html_email = render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

        email_message.send()
        return
    except ArithmeticError as ex:
        logger.info("Exception raised in sending mail -- {0}".format(ex.args))
