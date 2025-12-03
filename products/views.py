"""
Views for products app.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Max
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Review
from .forms import ReviewForm


def product_list_view(request):
    """
    Display list of products with filtering and search.
    """
    import os
    from django.conf import settings
    
    products = Product.objects.filter(is_available=True).select_related('category').prefetch_related('images')
    
    # Get hero images for carousel
    hero_images = []
    try:
        # Use STATICFILES_DIRS for development (where files actually are)
        logo_dir = os.path.join(settings.STATICFILES_DIRS[0], 'logo')
        
        if os.path.exists(logo_dir):
            import glob
            from django.templatetags.static import static
            image_files = sorted(glob.glob(os.path.join(logo_dir, '*.jpg')))
            for img_file in image_files[:10]:  # Limit to 10 images
                filename = os.path.basename(img_file)
                # Use Django's static function to generate proper URLs
                static_path = f'logo/{filename}'
                hero_images.append(static(static_path))
    except Exception as e:
        # If there's any error, just use empty list
        import traceback
        print(f"Error loading hero images: {e}")
        print(traceback.format_exc())
        hero_images = []
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(country_of_origin__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Price range filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Availability filter
    in_stock_only = request.GET.get('in_stock', '')
    if in_stock_only:
        products = products.filter(stock_quantity__gt=0)
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter sidebar
    categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count('products', filter=Q(products__is_available=True))
    )
    
    # Calculate max price for filter
    max_product_price = Product.objects.filter(is_available=True).aggregate(
        max_price=Max('price')
    )['max_price'] or 0
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
        'min_price': min_price,
        'max_price': max_price,
        'max_product_price': max_product_price,
        'in_stock_only': in_stock_only,
        'sort_by': sort_by,
        'hero_images': hero_images,
    }
    
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, slug):
    """
    Display product detail page with reviews.
    """
    product = get_object_or_404(Product, slug=slug, is_available=True)
    
    # Get related products (same category)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]
    
    # Get reviews with pagination
    reviews = Review.objects.filter(product=product).select_related('user')
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    reviews_page = paginator.get_page(page_number)
    
    # Check if user has already reviewed this product
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews_page': reviews_page,
        'user_review': user_review,
        'average_rating': product.get_average_rating(),
        'review_count': product.get_review_count(),
    }
    
    return render(request, 'products/product_detail.html', context)


def category_detail_view(request, slug):
    """
    Display products in a specific category.
    """
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(
        category=category,
        is_available=True
    ).select_related('category').prefetch_related('images')
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'sort_by': sort_by,
    }
    
    return render(request, 'products/category_detail.html', context)


@login_required
def add_review_view(request, slug):
    """
    Add or update a product review.
    """
    product = get_object_or_404(Product, slug=slug, is_available=True)
    
    # Check if user has already reviewed
    review, created = Review.objects.get_or_create(
        product=product,
        user=request.user,
        defaults={'rating': 5, 'comment': ''}
    )
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            if created:
                messages.success(request, 'Thank you for your review!')
            else:
                messages.success(request, 'Your review has been updated!')
            return redirect('products:product_detail', slug=slug)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'product': product,
        'form': form,
        'review': review,
    }
    
    return render(request, 'products/add_review.html', context)

