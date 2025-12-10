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
from .models import Order, OrderItem
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


@login_required
def order_detail_view(request, order_number):
    """
    Display order details.
    """
    if request.user.is_staff:
        order = get_object_or_404(Order, order_number=order_number)
    else:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_list_view(request):
    """
    Display user's order history.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'orders/order_list.html', context)


@csrf_exempt
def stripe_webhook(request):
    """
    Handle Stripe webhook events.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_number = payment_intent['metadata'].get('order_number')
        
        try:
            order = Order.objects.get(order_number=order_number)
            order.status = 'processing'
            order.save()
        except Order.DoesNotExist:
            pass
    
    return HttpResponse(status=200)





