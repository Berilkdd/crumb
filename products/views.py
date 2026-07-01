from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def all_products(request):
    product = Product.objects.first()
    return HttpResponse(product.name)