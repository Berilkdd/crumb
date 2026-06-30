from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from cart.contexts import cart_contents
from products.models import Product
from .forms import OrderForm
from .models import Order, OrderLineItem
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    
    cart = request.session.get("cart", {})

    if request.method == "POST":        
        order_form = OrderForm(request.POST)
        if order_form.is_valid():

            order = order_form.save(commit=False)
            order.user = request.user
            order.save_delivery_info = (
                "save_delivery_info" in request.POST
            )
            order.save()
            
            for item_id, quantity in cart.items():

                product = Product.objects.get(pk=item_id)

                OrderLineItem.objects.create(
                    order=order,
                    product=product,
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

    

