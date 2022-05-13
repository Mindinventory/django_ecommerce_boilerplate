from django.db import models
from django.contrib.auth.models import User


class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_shipping_address")
    address_one = models.CharField(max_length=250, null=True, blank=True)
    address_two = models.CharField(max_length=250, null=True, blank=True)
    zipcode = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "shipping_address"
        verbose_name_plural = "shipping_address"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    mobile_no = models.CharField(null=True, blank=True, max_length=15)
    alt_mobile_no = models.CharField(null=True, blank=True, max_length=15)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profile"


class ForgotPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_forgot_password")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "forgot_password"
        verbose_name_plural = "forgot_password"
