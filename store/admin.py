from django.contrib import admin

from store.models import Category, Brand, Product, Order, OrderItem


class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


class AdminBrand(admin.ModelAdmin):
    list_display = ['name']


class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','brand','category']


admin.site.register(Category, AdminCategory)
admin.site.register(Brand, AdminBrand)
admin.site.register(Product, AdminProduct)
admin.site.register(Order)
admin.site.register(OrderItem)

