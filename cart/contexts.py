from decimal import Decimal
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):

    cart = request.session.get("cart", {})

    cart_items = []
    product_count = 0
    subtotal = Decimal("0.00")

    for item_id, quantity in cart.items():

        product = get_object_or_404(Product, pk=item_id)

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "line_total": product.price * quantity,
        })

        product_count += quantity
        subtotal += product.price * quantity

    reward_count = min(product_count, 5)

    if subtotal >= Decimal("35.00"):
        shipping = Decimal("0.00")
    else:
        shipping = Decimal("3.50")

    total = subtotal + shipping

    eligible_for_free_delivery = shipping == 0

    amount_remaining = max(Decimal("35.00") - subtotal, Decimal("0.00"))

    return {
        "product_count": product_count,
        "cart_items": cart_items,
        "reward_count": reward_count,
        "reward_range": range(reward_count),
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
        "eligible_for_free_delivery": eligible_for_free_delivery,
        "amount_remaining": amount_remaining,
    }