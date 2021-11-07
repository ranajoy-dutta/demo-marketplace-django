from django.core.exceptions import ObjectDoesNotExist
from carts.models import Cart, CartItem
from carts.views import _cart_id

def cart_details(request, quantity=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for items in cart_items:
            quantity += items.quantity
    except Cart.DoesNotExist:
        pass


    cart = {"cart_count": quantity}
    return dict(cart=cart)