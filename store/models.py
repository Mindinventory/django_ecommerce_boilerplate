from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "brand"
        verbose_name_plural = "brands"


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    qty = models.IntegerField()
    description = models.CharField(max_length=200, blank=True, null=True)
    image = models.FileField(upload_to='uploads/products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="product_brand")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_of_customer")
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200)

    def __str__(self):
        return str(self.customer.name)

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_item")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")
    quantity = models.IntegerField()
    date_added = models.DateTimeField()

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "order_item"
        verbose_name_plural = "order_items"
