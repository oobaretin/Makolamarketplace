"""
Context processors for cart app.
"""
from .utils import get_cart


def cart(request):
    """
    Add cart information to template context.
    """
    cart_obj = get_cart(request)
    return {
        'cart': cart_obj,
        'cart_total': cart_obj.get_total() if cart_obj else 0,
        'cart_item_count': cart_obj.get_item_count() if cart_obj else 0,
    }

