from django.http import Http404
from django.views.generic import DetailView, ListView, TemplateView

from .models import Product, Category
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
                "categories": self.get_queryset().filter(category=self.get_object()).exclude(id=self.kwargs["pk"]).order_by('name'),
                'cartItems': cartItems}
        return data
