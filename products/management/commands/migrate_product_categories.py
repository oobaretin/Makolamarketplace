"""
Management command to migrate products from old categories to new categories.
"""
from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Migrate products from old categories to new category structure'

    def handle(self, *args, **options):
        self.stdout.write('Migrating products to new categories...')
        
        # Mapping from old category names to new category names
        category_mapping = {
            'Grains & Cereals': 'Grains & Flour',
            'Spices & Seasonings': 'Seasonings',
            'Fresh Produce': 'Produce',
            'Frozen Foods': 'Frozen',
            'Beverages': 'Drinks',
            'Palm Oil & Cooking Oils': 'Oils',
            'Flours & Starches': 'Flour',
            'Canned & Packaged Goods': 'Canned Goods',
        }
        
        migrated_count = 0
        
        for old_name, new_name in category_mapping.items():
            try:
                old_category = Category.objects.get(name=old_name)
                new_category = Category.objects.get(name=new_name)
                
                products = Product.objects.filter(category=old_category)
                count = products.count()
                
                if count > 0:
                    products.update(category=new_category)
                    migrated_count += count
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Migrated {count} products from "{old_name}" to "{new_name}"'
                        )
                    )
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Category "{old_name}" or "{new_name}" not found, skipping...')
                )
        
        self.stdout.write(self.style.SUCCESS(f'\nMigration complete! Migrated {migrated_count} products.'))







