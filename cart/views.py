from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from decimal import Decimal


def add_to_cart(request, item_id):

    product = get_object_or_404(Product, pk=item_id)

    cart = request.session.get("cart", {})

    item_id = str(item_id)

    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1

    request.session["cart"] = cart

    print(request.session["cart"])

    return redirect("products")

def view_cart(request):

    return render(request, "cart/cart.html")

def remove_from_cart(request, item_id):

    cart = request.session.get("cart", {})

    item_id = str(item_id)

    if item_id in cart:
        del cart[item_id]

    request.session["cart"] = cart

    return redirect("view_cart")

def increase_quantity(request, item_id):

    cart = request.session.get("cart", {})

    item_id = str(item_id)

    if item_id in cart:
        cart[item_id] += 1

    request.session["cart"] = cart

    return redirect("view_cart")

def decrease_quantity(request, item_id):

    cart = request.session.get("cart", {})

    item_id = str(item_id)

    if item_id in cart:

        if cart[item_id] > 1:
            cart[item_id] -= 1
        else:
            del cart[item_id]

    request.session["cart"] = cart

    return redirect("view_cart")