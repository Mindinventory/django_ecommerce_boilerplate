from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(request,order_item):
    user = request.user
    m= {}
    for i in order_item:
        m[i.product.name] = i.quantity
    send_mail(f'Hi {user}, Your order received!',
    f'Thank you for your oredr! \n \n Order details:\n \n {m}' ,
    'mikadev4@gmail.com',
    ['cedobef687@pashter.com'])
    return None 

@shared_task
def send_email_task_outofstock(request):
    user = request.user
    send_mail(f'Hi {user}, We received your order',
    'Thank you for your oredr.\n \n We are sorry to inform you that product is out of stock! \n \n please try after some time.',
    'mikadev4@gmail.com',
    ['cedobef687@pashter.com'])
    return None 