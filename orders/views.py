"""
Views for orders app (Shopping List only, no online checkout/delivery).
"""
import logging
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .forms import CheckoutForm
from cart.utils import get_cart_items, get_cart_total, clear_cart
from products.models import Product

logger = logging.getLogger(__name__)


def shopping_list_view(request):
    """
    Display the user-selected shopping list (formerly cart/order overview).
    """
    shopping_list_items = get_cart_items(request)
    shopping_list_total = get_cart_total(request)

    context = {
        'shopping_list_items': shopping_list_items,
        'shopping_list_total': shopping_list_total,
    }
    return render(request, 'orders/shopping_list.html', context)





