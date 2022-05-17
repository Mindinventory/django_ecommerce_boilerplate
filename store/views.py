import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, JsonResponse, HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from ecommerce.settings import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY
from .models import Product, Category, Brand
from .tasks import send_confirmation_email_task
from .utils import cookiecart


class HomeView(ListView):
    template_name = 'home.html'
    model = Product

    def get_queryset(self, *args, **kwargs):
        qs = super(HomeView, self).get_queryset()
        qs = qs.order_by("name")
        return qs

    def get_context_data(self, *args, **kwargs):
        data = {'products': self.get_queryset(), 'cartitems': cookiecart(self.request)['cartitems']}
        return data


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"

    def get_object(self, queryset=None):
        try:
            category = self.get_queryset().get(pk=self.kwargs["pk"]).category
            return category

        except self.get_queryset().model.DoesNotExist:
            raise Http404("Product not found")

    def get_context_data(self, **kwargs):

        data = {'product': self.get_queryset().get(pk=self.kwargs["pk"]),
                "categories": self.get_queryset().filter(category=self.get_object()).exclude(
                    id=self.kwargs["pk"]).order_by('name'),
                'cartitems': cookiecart(self.request)['cartitems']}
        return data


class CategoryView(ListView):
    model = Product
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        data = {'products': Product.objects.all().order_by('name'),
                'categories': Category.objects.all().order_by('name'),
                'brands': Brand.objects.all().order_by('name'), 'cartitems': cookiecart(self.request)['cartitems']}
        return data


class ProductByCategoryView(DetailView):
    model = Product
    template_name = "category.html"

    def get_object(self, queryset=None):
        products = self.get_queryset().filter(category=self.kwargs["pk"]).order_by('name')
        return products

    def get_context_data(self, **kwargs):
        data = {'products': self.get_object(),
                'categories': Category.objects.all().order_by('name'),
                'brands': Brand.objects.all().order_by('name'), 'cartitems': cookiecart(self.request)['cartitems']}
        return data


class ProductByBrandView(DetailView):
    model = Product
    template_name = "category.html"

    def get_object(self, queryset=None):
        products = self.get_queryset().filter(brand=self.kwargs["pk"]).order_by('name')
        return products

    def get_context_data(self, **kwargs):
        data = {'products': self.get_object(),
                'categories': Category.objects.all().order_by('name'),
                'brands': Brand.objects.all().order_by('name'), 'cartitems': cookiecart(self.request)['cartitems']}
        return data


class CartView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        total = 0
        product_id = 0
        for item in cookiecart(self.request)['items']:
            total += int(item.get('get_total'))
            product_id = item.get('product').get('id')
        data = {'cartitems': cookiecart(self.request)['cartitems'], "items": cookiecart(self.request)['items'],
                "product_id": product_id}
        return data


class CheckoutView(TemplateView):
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        total = 0
        product_id = 0

        for item in cookiecart(self.request)['items']:
            total += int(item.get('get_total'))
            product_id = item.get('product').get('id')
        data = {"user": self.request.user,
                "cartitems": cookiecart(self.request)['cartitems'], "items": cookiecart(self.request)['items'],
                "stripe_publishable_key": STRIPE_PUBLISHABLE_KEY,
                "sum": total,
                "product_id": product_id
                }
        return data


class ConfirmationView(View):

    def get(self, request):
        send_confirmation_email_task(request)
        return redirect('home')


class Createcheckoutsession(View):
    """
        https://stripe.com/docs/api/checkout/sessions/create?lang=python
        Create a payment checkout session for cart items with stripe
    """

    def post(self, request, **kwargs):
        get_object_or_404(Product, pk=self.kwargs['pk'])
        stripe.api_key = STRIPE_SECRET_KEY
        lineitems = []
        item_dict = {}
        for item in cookiecart(self.request)['items']:
            item_dict['price_data'] = {
                "currency": 'inr',
                "product_data": {
                    "name": item.get('product').get('name'),
                },
                "unit_amount": int(item.get('product').get('price')) * 100,
            }
            item_dict['quantity'] = item.get('quantity')
            lineitems.append(item_dict)

            item_dict = {}

        checkout_session = stripe.checkout.Session.create(

            customer_email=request.POST['email'],
            payment_method_types=['card'],
            line_items=lineitems,
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('success')
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('failed')),
        )
        return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):
    """
        Redirects to payment success page for current session and manages product stock.
    """

    template_name = "payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = STRIPE_SECRET_KEY
        stripe.checkout.Session.retrieve(session_id)
        for item in cookiecart(self.request)['items']:
            quantity = item.get('quantity')
            product_id = item.get('product').get('id')
            obj = Product.objects.get(id=product_id)
            avai = obj.qty - quantity
            obj.qty = avai
            obj.save()

        return render(request, self.template_name, context={"cartitems": cookiecart(self.request)['cartitems']})


class PaymentFailedView(TemplateView):
    template_name = "payment_failed.html"

    def get_context_data(self, **kwargs):
        data = {"cartitems": cookiecart(self.request)['cartitems']}
        return data
