from django.contrib.auth.decorators import login_required
from django.urls import path

from store.views import HomeView, ProductDetailView, CategoryView, CartView, \
    ProductByBrandView, ProductByCategoryView, CheckoutView, ConfirmationView, Createcheckoutsession, \
    PaymentSuccessView, \
    PaymentFailedView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('brand/<int:pk>/product/', ProductByBrandView.as_view(),
         name='product_by_brand'),
    path('category/<int:pk>/category/', ProductByCategoryView.as_view(),
         name='product_by_category'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', login_required(CheckoutView.as_view(), login_url='login'), name='checkout'),
    path('api/checkout-session/<int:pk>/', Createcheckoutsession.as_view(), name='api_checkout_session'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),
]
