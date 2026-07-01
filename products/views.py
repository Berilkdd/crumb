##from django.shortcuts import render
##from .models import Product


##def all_products(request):
##    """A view to display all products."""

##    products = Product.objects.all()

##    context = {
##        'products': products,
##    }

##    return render(request, 'products/products.html', context)


from django.http import HttpResponse

def all_products(request):
    return HttpResponse("Products OK")