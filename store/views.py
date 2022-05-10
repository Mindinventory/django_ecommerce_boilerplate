from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from ecommerce.settings import STRIPE_PUBLISHABLE_KEY
from users.forms import EditProfileForm
from .models import Product, Category, Brand, Order, OrderItem
from .tasks import send_email_task
from .utils import cookieCart


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        cookieData = cookieCart(self.request)
        cartItems = cookieData['cartItems']

        data = {'products': Product.objects.all().order_by('-qty')[:20], 'cartItems': cartItems}
        return data


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"

    def get_object(self, queryset=None):
        try:
            category = self.get_queryset().get(pk=self.kwargs["pk"]).category
            return category

        except self.get_queryset().model.DoesNotExist:
            raise Http404("Not found")

    def get_context_data(self, **kwargs):
        cookieData = cookieCart(self.request)
        cartItems = cookieData['cartItems']

        data = {'product': self.get_queryset().get(pk=self.kwargs["pk"]),
                "categories": self.get_queryset().filter(category=self.get_object()).exclude(
                    id=self.kwargs["pk"]).order_by('name'),
                'cartItems': cartItems}
        return data


class CategoryView(ListView):
    model = Product
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        cookieData = cookieCart(self.request)
        cartItems = cookieData['cartItems']
        data = {'products': Product.objects.all().order_by('name'),
                'categories': Category.objects.all().order_by('name'),
                'brands': Brand.objects.all().order_by('name'), 'cartItems': cartItems}
        return data


class ProductByCategoryView(DetailView):
    model = Product
    template_name = "product_by_category.html"

    def get_object(self, queryset=None):
        products = self.get_queryset().filter(category=self.kwargs["pk"]).order_by('name')
        return products

    def get_context_data(self, **kwargs):
        cookieData = cookieCart(self.request)
        cartItems = cookieData['cartItems']
        data = {'products': self.get_object(),
                'categories': Category.objects.all().order_by('name'),
                'brands': Brand.objects.all().order_by('name'), 'cartItems': cartItems}
        return data


class ProductByBrandView(DetailView):
    model = Product
    template_name = "product_by_brand.html"

    def get_object(self, queryset=None):
        products = self.get_queryset().filter(brand=self.kwargs["pk"]).order_by('name')
        return products

    def get_context_data(self, **kwargs):
        cookieData = cookieCart(self.request)
        cartItems = cookieData['cartItems']
        data = {'products': self.get_object(),
                'categories': Category.objects.all().order_by('name'),
                'brands': Brand.objects.all().order_by('name'), 'cartItems': cartItems}
        return data


class CartView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        cookieData = cookieCart(self.request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        data = {'cartItems': cartItems, "items": items}
        return data


class Checkout(LoginRequiredMixin, TemplateView):
    template_name = "checkout.html"

    def get_context_data(self, **kwargs):
        cookieData = cookieCart(self.request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        sum = 0
        for item in items:
            sum += item.get('get_total')
        data = {"user": self.request.user,
                "cartItems": cartItems, "items": items,
                "key": STRIPE_PUBLISHABLE_KEY,
                "sum":sum
                }
        return data


class Confirmation(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        send_email_task(request)

        return redirect('home')
