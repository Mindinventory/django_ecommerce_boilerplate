from django.contrib import admin

from users.models import ShippingAddress, Profile

admin.site.register(ShippingAddress)
admin.site.register(Profile)
