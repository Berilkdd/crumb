from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from cart.contexts import cart_contents
from products.models import Product
from .forms import OrderForm
from .models import Order, OrderLineItem
import stripe
from .webhook_handler import StripeWH_Handler
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def cache_checkout_data(request):
    if request.method == "POST":
        try:
            pid = request.POST.get("client_secret").split("_secret")[0]

            stripe.PaymentIntent.modify(
                pid,
                metadata={
                    "cart": json.dumps(request.session.get("cart", {})),
                    "save_delivery_info": request.POST.get(
                        "save_delivery_info"
                    ),
                    "user": request.user.username,
                    "full_name": request.POST.get("full_name"),
                    "address_line1": request.POST.get("address_line1"),
                    "address_line2": request.POST.get("address_line2"),
                    "town_or_city": request.POST.get("town_or_city"),
                    "postcode": request.POST.get("postcode"),
                    "phone_number": request.POST.get("phone_number"),
                },
            )

            return HttpResponse(status=200)

        except Exception as e:
            messages.error(request, "Sorry, your payment cannot be processed.")
            return HttpResponse(content=e, status=400)

def checkout(request):
    
    cart = request.session.get("cart", {})

    if request.method == "POST":

        pid = request.POST.get("client_secret").split("_secret")[0]

        order_form = OrderForm(request.POST)

        if order_form.is_valid():

            order = order_form.save(commit=False)
            order.user = request.user
            order.stripe_pid = pid
            order.save_delivery_info = (
                "save_delivery_info" in request.POST
            )
            cart_data = cart_contents(request)

            order.order_total = cart_data["subtotal"]
            order.delivery_cost = cart_data["shipping"]
            order.grand_total = cart_data["total"]
            order.save()
            
            for item_id, quantity in cart.items():

                product = Product.objects.get(pk=item_id)

                OrderLineItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_image=product.image,
                quantity=quantity,
                product_price=product.price,
            )

            return redirect("checkout_success", order.id)

        else:
            messages.error(
                request,
                "Please check your form."
            )        

    # Prevent direct URL access to checkout when the cart is empty.
    if not cart:
        messages.info(request, "Cart is empty.")
        return redirect("products")

    # Redirect unauthenticated users to the checkout gate.
    if not request.user.is_authenticated:
        return redirect("checkout_gate")
    
    # If user is authenticated and cart is not empty
    # Pre-fill the form if there is a saved address 

    initial = {}

    saved_order = (
        Order.objects
        .filter(
            user=request.user,
            save_delivery_info=True,
        )
        .order_by("-date")
        .first()
    )

    if saved_order:
        initial = {
            "full_name": saved_order.full_name,
            "address_line1": saved_order.address_line1,
            "address_line2": saved_order.address_line2,
            "town_or_city": saved_order.town_or_city,
            "postcode": saved_order.postcode,
            "phone_number": saved_order.phone_number,
    }
        

    order_form = OrderForm(initial=initial)

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

    cart = request.session.get("cart", {})

    # Prevent direct URL access to the checkout gate when the cart is empty.
    if not cart:
        messages.info(request, "Cart is empty.")
        return redirect("products")

    # Authenticated users should continue directly to checkout.
    if request.user.is_authenticated:
        return redirect("checkout")

    request.session["after_signup_redirect"] = "checkout"

    return render(request, "checkout/checkout_gate.html")

def checkout_success(request, order_id):

    order = get_object_or_404(Order, pk=order_id)

    if "cart" in request.session:
        del request.session["cart"]

    return render(
        request,
        "checkout/checkout_success.html",
        {
            "order": order,
        },
    )

@csrf_exempt
def webhook(request):
    """Handle Stripe webhooks."""

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WH_SECRET,
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    handler = StripeWH_Handler(request)

    event_map = {
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
        "payment_intent.payment_failed": handler.handle_event,
    }

    event_type = event["type"]
    event_handler = event_map.get(event_type, handler.handle_event)

    return event_handler(event)

