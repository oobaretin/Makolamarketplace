"""
Views for cart app.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .utils import (
    get_cart_items,
    get_cart_total,
    add_to_cart,
    update_cart_item,
    remove_from_cart,
    clear_cart
)


def cart_view(request):
    """
    Display shopping cart.
    """
    cart_items = get_cart_items(request)
    cart_total = get_cart_total(request)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    
    return render(request, 'cart/cart.html', context)


def add_to_cart_view(request, product_id):
    """
    Add product to cart (AJAX or regular request).
    """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        success, message = add_to_cart(request, product_id, quantity)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request
            return JsonResponse({
                'success': success,
                'message': message,
                'cart_total': get_cart_total(request),
                'cart_item_count': sum(item['quantity'] for item in get_cart_items(request))
            })
        else:
            # Regular request
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            
            # Determine redirect destination
            redirect_to = request.POST.get('redirect_to', 'products:product_list')
            slug = request.POST.get('slug', '')
            
            # If slug is provided and redirect is to product detail, go there
            if slug and redirect_to == 'products:product_detail':
                try:
                    from products.models import Product
                    product = Product.objects.get(id=product_id)
                    return redirect('products:product_detail', slug=product.slug)
                except Product.DoesNotExist:
                    pass
            
            # If redirect is to category detail, get category slug from referrer or product
            if redirect_to == 'products:category_detail' and slug:
                try:
                    from products.models import Product
                    product = Product.objects.get(id=product_id)
                    if product.category:
                        return redirect('products:category_detail', slug=product.category.slug)
                except Product.DoesNotExist:
                    pass
            
            # Fallback: redirect to product list
            return redirect('products:product_list')
    
    return redirect('products:product_list')


def update_cart_view(request, product_id):
    """
    Update cart item quantity.
    """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        success, message = update_cart_item(request, product_id, quantity)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': success,
                'message': message,
                'cart_total': get_cart_total(request),
                'cart_item_count': sum(item['quantity'] for item in get_cart_items(request))
            })
        else:
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
    
    return redirect('cart:cart')


def remove_from_cart_view(request, product_id):
    """
    Remove product from cart.
    """
    if request.method == 'POST':
        success, message = remove_from_cart(request, product_id)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': success,
                'message': message,
                'cart_total': get_cart_total(request),
                'cart_item_count': sum(item['quantity'] for item in get_cart_items(request))
            })
        else:
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
    
    return redirect('cart:cart')

