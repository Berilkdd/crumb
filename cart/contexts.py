def cart_contents(request):

    cart = request.session.get("cart", {})

    product_count = sum(cart.values())

    context = {
        "product_count": product_count,        
    }

    return context