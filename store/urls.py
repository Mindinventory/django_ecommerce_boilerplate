from django.contrib.auth.decorators import login_required
from django.urls import path

from store.views import HomeView, ProductDetailView, CategoryView, ProductByCategoryView, ProductByBrandView, CartView, \
    SearchView, CheckoutView, ConfirmationView, Createcheckoutsession, PaymentSuccessView, \
    PaymentFailedView

urlpatterns = [
    path('', login_required(HomeView.as_view(), login_url='login'), name='home'),
    path('product/<int:pk>/', login_required(ProductDetailView.as_view(), login_url='login'), name='product_detail'),
    path('categories/', login_required(CategoryView.as_view(), login_url='login'), name='categories'),
    path('category/<int:pk>/product/', login_required(ProductByCategoryView.as_view(), login_url='login'),
         name='product_by_category'),
    path('brand/<int:pk>/product/', login_required(ProductByBrandView.as_view(), login_url='login'),
         name='product_by_brand'),
    path('cart/', login_required(CartView.as_view()), name='cart'),
    path('search/', login_required(SearchView.as_view()), name='search'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('api/checkout-session/<int:pk>/', Createcheckoutsession.as_view(), name='api_checkout_session'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),
]
