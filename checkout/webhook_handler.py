import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product
from decimal import Decimal

User = get_user_model()


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Handle a generic/unknown webhook event"""
        return HttpResponse(
            content=f"Unhandled webhook received: {event['type']}",
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook"""

        intent = event.data.object
        pid = intent.id

        try:
            order = Order.objects.get(stripe_pid=pid)

            return HttpResponse(
                content=(
                    f"Webhook received: {event['type']} | "
                    "Order already exists."
                ),
                status=200,
            )

        except Order.DoesNotExist:      
            if not getattr(intent.metadata, "cart", None):
                return HttpResponse(
                    content=(
                        f"Webhook received: {event['type']} | "
                        "No checkout metadata found."
                    ),
                    status=200,
                )   
           
            cart = json.loads(intent.metadata.cart)
            user_id = int(intent.metadata.user_id)
            user = User.objects.get(pk=user_id)
            save_delivery_info = (
                intent.metadata.save_delivery_info == "true"
            )

            full_name = intent.metadata.full_name
            address_line1 = intent.metadata.address_line1
            address_line2 = intent.metadata.address_line2
            town_or_city = intent.metadata.town_or_city
            postcode = intent.metadata.postcode
            phone_number = intent.metadata.phone_number

            order = Order.objects.create(
                user=user,
                full_name=full_name,
                address_line1=address_line1,
                address_line2=address_line2,
                town_or_city=town_or_city,
                postcode=postcode,
                phone_number=phone_number,
                stripe_pid=pid,
                save_delivery_info=save_delivery_info,
            )
            subtotal = Decimal("0.00")

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

                subtotal += product.price * quantity

            if subtotal >= Decimal("35.00"):
                shipping = Decimal("0.00")
            else:
                shipping = Decimal("3.50")

            order.order_total = subtotal
            order.delivery_cost = shipping
            order.grand_total = subtotal + shipping

            order.save()

            return HttpResponse(
                content=(
                    f"Webhook received: {event['type']} | "
                    "PaymentIntent was successful."
                ),
                status=200,
            )