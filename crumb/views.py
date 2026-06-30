from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse


def custom_logout(request):

    cart = request.session.get("cart", {})

    next_url = request.GET.get("next", "/")

    logout(request)

    request.session["cart"] = cart

    return redirect(next_url)


def signup_redirect(request):

    next_page = request.GET.get("next", "/")

    request.session["after_signup_redirect"] = next_page

    return redirect("account_signup")

def cart_redirect(request):
    messages.success(request, "cart is empty")
    return redirect("home")