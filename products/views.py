from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def all_products(request):
    products = Product.objects.all()

    return render(
        request,
        "products/products.html",
        {
            "products": products,
        },
    )