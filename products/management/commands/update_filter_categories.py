"""
Management command to update categories for the filter sidebar.
"""
from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Update categories to match the filter list: grains, spices, fresh produce, frozen foods, beverages, snacks, cooking oils, flours, and packaged goods'

    def handle(self, *args, **options):
        self.stdout.write('Updating categories for filter...')
        
        # New category list for filters
        categories_data = [
            {
                'name': 'Grains',
                'description': 'Rice, wheat, corn, millet, and other grain products.',
            },
            {
                'name': 'Spices',
                'description': 'African spices, seasonings, and flavorings.',
            },
            {
                'name': 'Fresh Produce',
                'description': 'Fresh fruits, vegetables, and herbs.',
            },
            {
                'name': 'Frozen Foods',
                'description': 'Frozen vegetables, fruits, meats, and prepared foods.',
            },
            {
                'name': 'Beverages',
                'description': 'Drinks, juices, and beverages.',
            },
            {
                'name': 'Snacks',
                'description': 'Chips, crackers, nuts, and snack foods.',
            },
            {
                'name': 'Cooking Oils',
                'description': 'Vegetable oils, palm oil, and cooking fats.',
            },
            {
                'name': 'Flours',
                'description': 'Wheat flour, cassava flour, yam flour, and other flours.',
            },
            {
                'name': 'Packaged Goods',
                'description': 'Canned goods, packaged foods, and preserved items.',
            },
        ]
        
        created_count = 0
        updated_count = 0
        deactivated_count = 0
        
        # Get all existing categories
        all_existing_categories = Category.objects.all()
        new_category_names = [cat['name'] for cat in categories_data]
        
        # Deactivate categories that are not in the new list
        for category in all_existing_categories:
            if category.name not in new_category_names:
                if category.is_active:
                    category.is_active = False
                    category.save()
                    deactivated_count += 1
                    self.stdout.write(self.style.WARNING(f'Deactivated category: {category.name}'))
        
        # Create or update categories from the new list
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
                # Update description and ensure it's active
                if category.description != cat_data['description']:
                    category.description = cat_data['description']
                    updated_count += 1
                
                if not category.is_active:
                    category.is_active = True
                    updated_count += 1
                
                if updated_count > 0:
                    category.save()
                    self.stdout.write(self.style.WARNING(f'↻ Updated category: {category.name}'))
                else:
                    self.stdout.write(self.style.NOTICE(f'○ Category already exists: {category.name}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\n{"="*50}\n'
            f'Categories update complete!\n'
            f'Created: {created_count}\n'
            f'Updated: {updated_count}\n'
            f'Deactivated: {deactivated_count}\n'
            f'Total active categories: {len(new_category_names)}\n'
            f'{"="*50}\n'
        ))
        
        # Show the final list
        active_categories = Category.objects.filter(is_active=True).order_by('name')
        self.stdout.write(self.style.SUCCESS('\nActive categories:'))
        for cat in active_categories:
            self.stdout.write(f'  - {cat.name}')





