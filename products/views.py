from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


def all_products(request):
    return HttpResponse("Products OK")