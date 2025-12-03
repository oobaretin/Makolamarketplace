"""
Management command to create categories only (without products).
This is useful for setting up categories before adding products.
"""
from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Create all product categories based on My Sasun reference (without products)'

    def handle(self, *args, **options):
        self.stdout.write('Creating categories...')
        
        # Categories based on My Sasun (https://mysasun.com/)
        # Note: My Sasun has a hierarchical structure, but we're using flat categories for simplicity
        # Main categories from the Groceries menu
        categories_data = [
            {
                'name': 'Frozen',
                'description': 'Frozen African foods including meat, vegetables, seafood, and starches.',
            },
            {
                'name': 'Grains & Flour',
                'description': 'Rice, beans, and various flours for traditional African cooking.',
            },
            {
                'name': 'Oils',
                'description': 'Cooking oils including palm oil, coconut oil, and vegetable oils.',
            },
            {
                'name': 'Baby',
                'description': 'Baby food and products for infants.',
            },
            {
                'name': 'Snacks',
                'description': 'African snacks, chips, crackers, and snack foods.',
            },
            {
                'name': 'Drinks',
                'description': 'Beverages, soft drinks, juices, and traditional African drinks.',
            },
            {
                'name': 'Produce',
                'description': 'Fresh fruits and vegetables.',
            },
            {
                'name': 'Breakfast',
                'description': 'Breakfast items including breads, cereals, and breakfast foods.',
            },
            {
                'name': 'Seasonings',
                'description': 'Herbs, spices, and seasonings for African cuisine.',
            },
            {
                'name': 'Condiments',
                'description': 'Sauces, condiments, and flavor enhancers.',
            },
            {
                'name': 'Health & Beauty',
                'description': 'Personal care, health, and beauty products.',
            },
            {
                'name': 'Household',
                'description': 'Household cleaning products and supplies.',
            },
            {
                'name': 'Canned Goods',
                'description': 'Canned foods, preserved items, and packaged goods.',
            },
            {
                'name': 'Pasta & Noodles',
                'description': 'Pasta, noodles, and related products.',
            },
            # Subcategories from Frozen (Meat, Vegetable, Seafood, Starch) - as separate top-level for now
            {
                'name': 'Meat',
                'description': 'Fresh and frozen meats including beef, goat, chicken, and turkey.',
            },
            {
                'name': 'Seafood',
                'description': 'Fresh and frozen seafood including fish, shrimp, and other seafood.',
            },
            # Subcategories from Grains & Flour (Rice, Beans, Flour) - as separate top-level for now
            {
                'name': 'Rice',
                'description': 'Various types of rice including parboiled, jasmine, and specialty rice.',
            },
            {
                'name': 'Beans',
                'description': 'Dry beans, canned beans, and bean products.',
            },
            {
                'name': 'Flour',
                'description': 'Various flours including wheat, cassava, yam, and plantain flour.',
            },
        ]
        
        created_count = 0
        existing_count = 0
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category.name}'))
            else:
                existing_count += 1
                # Update description if it's different
                if category.description != cat_data['description']:
                    category.description = cat_data['description']
                    category.is_active = True  # Ensure it's active
                    category.save()
                    self.stdout.write(self.style.WARNING(f'↻ Updated category: {category.name}'))
                else:
                    self.stdout.write(self.style.NOTICE(f'○ Category already exists: {category.name}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\n{"="*50}\n'
            f'Categories setup complete!\n'
            f'Created: {created_count}\n'
            f'Already existed: {existing_count}\n'
            f'Total: {created_count + existing_count} categories\n'
            f'{"="*50}\n'
        ))
        
        self.stdout.write(self.style.SUCCESS(
            'You can now add products to these categories via:\n'
            '1. Django Admin (http://localhost:8000/admin)\n'
            '2. Management command: python manage.py seed_products\n'
        ))

