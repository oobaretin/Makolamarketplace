"""
Management command to update categories based on My Sasun reference.
This will add new categories without deleting existing ones.
"""
from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Update categories based on My Sasun reference structure'

    def handle(self, *args, **options):
        self.stdout.write('Updating categories...')
        
        # Categories based on My Sasun (https://mysasun.com/collections/all)
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
            {
                'name': 'Meat',
                'description': 'Fresh and frozen meats including beef, goat, chicken, and turkey.',
            },
            {
                'name': 'Seafood',
                'description': 'Fresh and frozen seafood including fish, shrimp, and other seafood.',
            },
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
        updated_count = 0
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                # Update description if category exists
                if category.description != cat_data['description']:
                    category.description = cat_data['description']
                    category.save()
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f'Updated category: {category.name}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\nCategories update complete! Created: {created_count}, Updated: {updated_count}'
        ))



