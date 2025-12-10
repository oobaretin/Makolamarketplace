"""
Context processors for products app.
"""
from django.db.models import Count, Q
from .models import Category


def categories(request):
    """
    Add all active categories to the template context.
    """
    categories_list = Category.objects.filter(is_active=True).annotate(
        product_count=Count('products', filter=Q(products__is_available=True))
    ).order_by('name')
    
    return {
        'all_categories': categories_list,
    }






