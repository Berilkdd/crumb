from django.db import models


class Order(models.Model):

    full_name = models.CharField(max_length=100)

    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(
        max_length=255,
        blank=True
    )

    town_or_city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name