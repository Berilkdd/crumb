from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    origin = models.CharField(max_length=100, blank=True)
    roast = models.CharField(max_length=50, blank=True)
    process = models.CharField(max_length=50, blank=True)
    strength = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name