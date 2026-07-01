from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    image_url = models.URLField(max_length=1024, blank=True, null=True)
    origin = models.CharField(max_length=100, blank=True)
    roast = models.CharField(max_length=50, blank=True)
    process = models.CharField(max_length=50, blank=True)
    strength = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name
    