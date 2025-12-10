"""
Management command to clean up duplicate categories and keep only My Sasun structure.
This will deactivate old/duplicate categories and keep only the correct ones.
"""
from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Clean up duplicate categories and keep only My Sasun structure'

    def handle(self, *args, **options):
        self.stdout.write('Cleaning up categories...\n')
        
        # Categories to KEEP (from My Sasun reference)
        keep_categories = [
            'Frozen',
            'Grains & Flour',
            'Oils',
            'Baby',
            'Snacks',
            'Drinks',
            'Produce',
            'Breakfast',
            'Seasonings',
            'Condiments',
            'Health & Beauty',
            'Household',
            'Canned Goods',
            'Pasta & Noodles',
            'Meat',
            'Seafood',
            'Rice',
            'Beans',
            'Flour',
        ]
        
        # Mapping old categories to new ones (for migrating products)
        category_mapping = {
            'Beverages': 'Drinks',
            'Grains & Cereals': 'Grains & Flour',
            'Flours & Starches': 'Flour',
            'Canned & Packaged Goods': 'Canned Goods',
            'Fresh Produce': 'Produce',
            'Frozen Foods': 'Frozen',
            'Palm Oil & Cooking Oils': 'Oils',
            'Spices & Seasonings': 'Seasonings',
        }
        
        # Get all categories
        all_categories = Category.objects.all()
        deactivated_count = 0
        migrated_count = 0
        
        for category in all_categories:
            if category.name not in keep_categories:
                # Check if this category should be mapped to a new one
                if category.name in category_mapping:
                    new_category_name = category_mapping[category.name]
                    try:
                        new_category = Category.objects.get(name=new_category_name)
                        
                        # Migrate products to new category
                        products = Product.objects.filter(category=category)
                        product_count = products.count()
                        if product_count > 0:
                            products.update(category=new_category)
                            migrated_count += product_count
                            self.stdout.write(
                                self.style.WARNING(
                                    f'↻ Migrated {product_count} products from "{category.name}" to "{new_category_name}"'
                                )
                            )
                        
                        # Deactivate old category
                        category.is_active = False
                        category.save()
                        deactivated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'✗ Deactivated duplicate category: {category.name} → {new_category_name}')
                        )
                    except Category.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f'✗ Target category "{new_category_name}" not found for "{category.name}"')
                        )
                else:
                    # Deactivate unknown/old categories
                    product_count = category.products.count()
                    if product_count > 0:
                        self.stdout.write(
                            self.style.WARNING(
                                f'⚠ Category "{category.name}" has {product_count} products. Please migrate manually before deactivating.'
                            )
                        )
                    else:
                        category.is_active = False
                        category.save()
                        deactivated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'✗ Deactivated old category: {category.name}')
                        )
        
        # Ensure all keep categories are active
        activated_count = 0
        for cat_name in keep_categories:
            try:
                category = Category.objects.get(name=cat_name)
                if not category.is_active:
                    category.is_active = True
                    category.save()
                    activated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Activated category: {category.name}'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'✗ Required category "{cat_name}" not found!'))
        
        # Summary
        active_categories = Category.objects.filter(is_active=True).count()
        
        self.stdout.write(self.style.SUCCESS(
            f'\n{"="*50}\n'
            f'Category cleanup complete!\n'
            f'Deactivated: {deactivated_count} old/duplicate categories\n'
            f'Activated: {activated_count} categories\n'
            f'Products migrated: {migrated_count}\n'
            f'Active categories: {active_categories}\n'
            f'{"="*50}\n'
        ))
        
        # List final categories
        self.stdout.write(self.style.SUCCESS('\nFinal active categories:'))
        for cat in Category.objects.filter(is_active=True).order_by('name'):
            product_count = cat.products.count()
            self.stdout.write(f'  • {cat.name} ({product_count} products)')






