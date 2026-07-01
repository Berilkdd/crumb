from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def all_products(request):
    products = Product.objects.all()

    try:
        return render(
            request,
            "products/products.html",
            {"products": products},
        )
    except Exception as e:
        return HttpResponse(f"{type(e).__name__}: {e}")