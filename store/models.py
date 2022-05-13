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
