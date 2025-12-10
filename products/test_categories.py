"""
Quick test script to verify categories are working.
Run: python manage.py shell < products/test_categories.py
"""
from products.models import Category
from django.db.models import Count, Q

print("=" * 50)
print("CATEGORY DEBUG TEST")
print("=" * 50)

total = Category.objects.count()
active = Category.objects.filter(is_active=True).count()

print(f"\nTotal categories in database: {total}")
print(f"Active categories: {active}")

if active > 0:
    categories = list(Category.objects.filter(is_active=True).annotate(
        product_count=Count('products', filter=Q(products__is_available=True))
    ).order_by('name'))
    
    print(f"\nCategories list length: {len(categories)}")
    print("\nFirst 5 categories:")
    for cat in categories[:5]:
        print(f"  - {cat.name} (slug: {cat.slug}) - {cat.product_count} products")
else:
    print("\n⚠️  WARNING: No active categories found!")
    print("Run: python manage.py create_categories")

print("\n" + "=" * 50)





