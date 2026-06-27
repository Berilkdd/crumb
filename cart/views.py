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

    cart = request.session.get("cart", {})

    cart_items = []
    total_quantity = 0
    subtotal = 0

    for item_id, quantity in cart.items():

        product = get_object_or_404(Product, pk=item_id)

        cart_items.append({
            "product": product,
            "quantity": quantity,            
        })

        total_quantity += quantity
        subtotal += product.price * quantity

    reward_count = min(total_quantity, 5)

    if subtotal >= 35:
        shipping = Decimal("0.00")
    else:
        shipping = Decimal("3.50")

    eligible_for_free_delivery = shipping == 0
    amount_remaining = max(35 - subtotal, 0)
    
    total = subtotal + shipping

    context = {
        "cart_items": cart_items,
        "reward_count": reward_count,
        "reward_range": range(reward_count),
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
        "eligible_for_free_delivery": eligible_for_free_delivery,
        "amount_remaining": 35 - subtotal,
    }

    return render(request, "cart/cart.html", context)

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