from django.contrib.auth.decorators import login_required
from django.urls import path

from store.views import HomeView, ProductDetailView, CategoryView, CartView,\
    CheckoutView, ConfirmationView, Createcheckoutsession, PaymentSuccessView, \
    PaymentFailedView

urlpatterns = [
    path('', login_required(HomeView.as_view(), login_url='login'), name='home'),
    path('product/<int:pk>/', login_required(ProductDetailView.as_view(), login_url='login'), name='product_detail'),
    path('categories/', login_required(CategoryView.as_view(), login_url='login'), name='categories'),
    path('cart/', login_required(CartView.as_view()), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('api/checkout-session/<int:pk>/', Createcheckoutsession.as_view(), name='api_checkout_session'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),
]
