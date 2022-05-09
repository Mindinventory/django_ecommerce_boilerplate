from django.contrib.auth.decorators import login_required
from django.urls import path

from store.views import HomeView, ProductDetailView

urlpatterns = [
    path('', login_required(HomeView.as_view(), login_url='login'), name='home'),
    path('product/<int:pk>/', login_required(ProductDetailView.as_view(), login_url='login'), name='product_detail'),

]
