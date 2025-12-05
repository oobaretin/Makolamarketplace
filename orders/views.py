"""
Views for orders app.
"""
import stripe
import logging
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
if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY
else:
    logging.warning("STRIPE_SECRET_KEY is not set in settings")

logger = logging.getLogger(__name__)


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
            # Check if Stripe keys are configured
            if not settings.STRIPE_SECRET_KEY or not settings.STRIPE_PUBLIC_KEY:
                logger.error("Stripe keys not configured")
                messages.error(request, 'Payment system is not configured. Please contact support.')
                return redirect('cart:cart')
            
            # Create order
            try:
                order = form.save(commit=False)
                order.user = request.user if request.user.is_authenticated else None
                order.total_amount = cart_total
                order.save()
            except Exception as e:
                logger.error(f"Error creating order: {str(e)}")
                messages.error(request, 'Error creating order. Please try again.')
                return redirect('cart:cart')
            
            # Create order items
            try:
                from decimal import Decimal
                for item in cart_items:
                    # Ensure price is a Decimal
                    price = Decimal(str(item['price']))
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        product_name=item['product'].name,
                        quantity=item['quantity'],
                        price=price
                    )
            except Exception as e:
                logger.error(f"Error creating order items: {str(e)}", exc_info=True)
                order.delete()
                messages.error(request, f'Error processing order items: {str(e)}. Please try again.')
                return redirect('cart:cart')
            
            # Validate cart total before creating payment intent
            if cart_total <= 0:
                logger.error(f"Invalid cart total: {cart_total}")
                order.delete()
                messages.error(request, 'Cart total is invalid. Please add items to your cart.')
                return redirect('cart:cart')
            
            # Create Stripe payment intent
            try:
                # Convert cart_total to cents (ensure it's a number)
                amount_cents = int(float(cart_total) * 100)
                
                if amount_cents < 50:  # Stripe minimum is $0.50
                    logger.error(f"Amount too small: {amount_cents} cents")
                    order.delete()
                    messages.error(request, 'Order total must be at least $0.50.')
                    return redirect('cart:cart')
                
                intent = stripe.PaymentIntent.create(
                    amount=amount_cents,
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
                logger.error(f"Stripe error: {str(e)}")
                messages.error(request, f'Payment error: {str(e)}')
                order.delete()  # Delete order if payment setup fails
                return redirect('cart:cart')
            except ValueError as e:
                logger.error(f"Value error in payment intent creation: {str(e)}")
                messages.error(request, f'Invalid order amount. Please try again.')
                order.delete()
                return redirect('cart:cart')
            except Exception as e:
                logger.error(f"Unexpected error in payment intent creation: {str(e)}", exc_info=True)
                messages.error(request, f'An unexpected error occurred: {str(e)}. Please try again or contact support.')
                order.delete()
                return redirect('cart:cart')
        else:
            # Form is invalid
            logger.warning(f"Checkout form validation failed: {form.errors}")
            messages.error(request, 'Please correct the errors in the form.')
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





