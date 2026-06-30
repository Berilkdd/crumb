from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from cart.contexts import cart_contents
from .forms import OrderForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
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
    request.session["after_signup_redirect"] = "checkout"
    print(request.session.get("after_signup_redirect"))

    return render(request, "checkout/checkout_gate.html")

def checkout_success(request):
    return render(request, "checkout/checkout_success.html")

