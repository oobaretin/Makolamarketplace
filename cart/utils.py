"""
Utility functions for cart management.
"""
from .models import Cart, CartItem
from products.models import Product


def get_cart(request):
    """
    Get or create cart for user (logged-in) or session (guest).
    Returns Cart object or None for guest sessions.
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    return None


def get_or_create_session_cart(request):
    """
    Get cart items from session for guest users.
    Returns a dictionary of {product_id: {'quantity': int, 'price': float}}.
    """
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


def add_to_cart(request, product_id, quantity=1):
    """
    Add product to cart (works for both authenticated and guest users).
    """
    try:
        product = Product.objects.get(id=product_id, is_available=True)
    except Product.DoesNotExist:
        return False, "Product not found or unavailable"
    
    if product.stock_quantity < quantity:
        return False, f"Only {product.stock_quantity} items available in stock"
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity, 'price_at_addition': product.price}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return True, "Product added to cart"
    else:
        # Session-based cart for guests
        session_cart = get_or_create_session_cart(request)
        product_key = str(product_id)
        
        if product_key in session_cart:
            session_cart[product_key]['quantity'] += quantity
        else:
            session_cart[product_key] = {
                'quantity': quantity,
                'price': str(product.price)
            }
        
        request.session.modified = True
        return True, "Product added to cart"


def update_cart_item(request, product_id, quantity):
    """
    Update quantity of cart item.
    """
    if quantity <= 0:
        return remove_from_cart(request, product_id)
    
    try:
        product = Product.objects.get(id=product_id, is_available=True)
    except Product.DoesNotExist:
        return False, "Product not found"
    
    if product.stock_quantity < quantity:
        return False, f"Only {product.stock_quantity} items available in stock"
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
            return True, "Cart updated"
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return False, "Cart item not found"
    else:
        session_cart = get_or_create_session_cart(request)
        product_key = str(product_id)
        
        if product_key in session_cart:
            session_cart[product_key]['quantity'] = quantity
            request.session.modified = True
            return True, "Cart updated"
        return False, "Cart item not found"


def remove_from_cart(request, product_id):
    """
    Remove product from cart.
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return True, "Product removed from cart"
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return False, "Cart item not found"
    else:
        session_cart = get_or_create_session_cart(request)
        product_key = str(product_id)
        
        if product_key in session_cart:
            del session_cart[product_key]
            request.session.modified = True
            return True, "Product removed from cart"
        return False, "Cart item not found"


def get_cart_items(request):
    """
    Get all cart items as a list of dictionaries.
    Works for both authenticated and guest users.
    """
    items = []
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            for cart_item in cart.items.select_related('product').all():
                items.append({
                    'product': cart_item.product,
                    'quantity': cart_item.quantity,
                    'price': cart_item.price_at_addition,
                    'subtotal': cart_item.get_subtotal(),
                })
        except Cart.DoesNotExist:
            pass
    else:
        session_cart = get_or_create_session_cart(request)
        for product_id, item_data in session_cart.items():
            try:
                product = Product.objects.get(id=int(product_id), is_available=True)
                quantity = item_data['quantity']
                price = float(item_data['price'])
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price,
                    'subtotal': price * quantity,
                })
            except (Product.DoesNotExist, ValueError, KeyError):
                continue
    
    return items


def get_cart_total(request):
    """
    Calculate total cart value.
    """
    items = get_cart_items(request)
    return sum(item['subtotal'] for item in items)


def clear_cart(request):
    """
    Clear all items from cart.
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            return True
        except Cart.DoesNotExist:
            return True
    else:
        request.session['cart'] = {}
        request.session.modified = True
        return True

