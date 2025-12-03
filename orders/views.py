"""
Views for orders app.
"""
import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.utils import get_cart_items, get_cart_total, clear_cart
from products.models import Product

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout_view(request):
    """
    Display checkout page and handle order creation.
    """
    cart_items = get_cart_items(request)
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart')
    
    cart_total = get_cart_total(request)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.total_amount = cart_total
            order.save()
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    quantity=item['quantity'],
                    price=item['price']
                )
            
            # Create Stripe payment intent
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(cart_total * 100),  # Convert to cents
                    currency='usd',
                    metadata={
                        'order_number': order.order_number,
                        'user_id': str(order.user.id) if order.user else 'guest',
                    }
                )
                order.stripe_payment_intent_id = intent.id
                order.save()
                
                return render(request, 'orders/payment.html', {
                    'order': order,
                    'client_secret': intent.client_secret,
                    'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                })
            except stripe.error.StripeError as e:
                messages.error(request, f'Payment error: {str(e)}')
                order.delete()  # Delete order if payment setup fails
                return redirect('cart:cart')
    else:
        form = CheckoutForm(user=request.user)
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    
    return render(request, 'orders/checkout.html', context)


def payment_success_view(request, order_number):
    """
    Handle successful payment and clear cart.
    """
    order = get_object_or_404(Order, order_number=order_number)
    
    # Verify payment intent was successful
    if order.stripe_payment_intent_id:
        try:
            intent = stripe.PaymentIntent.retrieve(order.stripe_payment_intent_id)
            if intent.status == 'succeeded':
                order.status = 'processing'
                order.save()
                
                # Clear cart
                clear_cart(request)
                
                # Send confirmation email (implement email sending)
                # send_order_confirmation_email(order)
                
                messages.success(request, f'Order {order.order_number} placed successfully!')
                return render(request, 'orders/order_success.html', {'order': order})
        except stripe.error.StripeError:
            pass
    
    messages.error(request, 'Payment verification failed.')
    return redirect('orders:order_detail', order_number=order_number)


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



