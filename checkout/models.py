from decimal import Decimal
from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )

    full_name = models.CharField(max_length=100)

    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
    )

    town_or_city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    order_total = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0,
    )

    delivery_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    save_delivery_info = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class OrderLineItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(default=1)

    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    lineitem_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
    )

    product_name = models.CharField(
        max_length=255,
        blank=True,
    )

    product_image = models.ImageField(
        upload_to="order_images/",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.lineitem_total = self.product_price * Decimal(self.quantity)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"