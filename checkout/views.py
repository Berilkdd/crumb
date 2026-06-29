from django.shortcuts import render, redirect
from django.conf import settings
from cart.contexts import cart_contents
from .forms import OrderForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):

    order_form = OrderForm()

    cart_data = cart_contents(request)

    stripe_total = round(cart_data["total"] * 100)

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    context = {
        "order_form": order_form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": intent.client_secret,
    }

    return render(request, "checkout/checkout.html", context)

def checkout_gate(request):

    if request.user.is_authenticated:
        return redirect("checkout")

    return render(request, "checkout/checkout_gate.html")

