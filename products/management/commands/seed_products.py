"""
Management command to seed the database with sample African products.
"""
from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Seed the database with sample African products'

    def handle(self, *args, **options):
        self.stdout.write('Seeding products...')
        
        # Create Categories (based on My Sasun reference: https://mysasun.com/collections/all)
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
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
        
        # Sample Products (updated to match new category structure)
        products_data = [
            # Flour
            {'name': 'Fufu Flour (Plantain)', 'category': 'Flour', 'price': 8.99, 'stock_quantity': 50, 'country_of_origin': 'Ghana', 'description': 'Traditional plantain fufu flour for making authentic fufu.'},
            {'name': 'Fufu Flour (Cassava)', 'category': 'Flour', 'price': 7.99, 'stock_quantity': 45, 'country_of_origin': 'Nigeria', 'description': 'Cassava-based fufu flour, perfect for traditional West African dishes.'},
            {'name': 'Fufu Flour (Yam)', 'category': 'Flour', 'price': 9.99, 'stock_quantity': 30, 'country_of_origin': 'Ghana', 'description': 'Yam fufu flour for authentic African cuisine.'},
            {'name': 'Plantain Flour', 'category': 'Flour', 'price': 8.99, 'stock_quantity': 45, 'country_of_origin': 'Ghana', 'description': 'Fine plantain flour for baking and cooking.'},
            {'name': 'Cassava Flour', 'category': 'Flour', 'price': 7.99, 'stock_quantity': 50, 'country_of_origin': 'Nigeria', 'description': 'Gluten-free cassava flour for traditional recipes.'},
            {'name': 'Yam Flour', 'category': 'Flour', 'price': 9.99, 'stock_quantity': 35, 'country_of_origin': 'Ghana', 'description': 'Traditional yam flour for authentic dishes.'},
            
            # Grains & Flour
            {'name': 'Gari (Cassava Flakes)', 'category': 'Grains & Flour', 'price': 6.99, 'stock_quantity': 60, 'country_of_origin': 'Nigeria', 'description': 'Traditional cassava flakes, a staple in West African cuisine.'},
            {'name': 'Egusi Seeds', 'category': 'Grains & Flour', 'price': 12.99, 'stock_quantity': 40, 'country_of_origin': 'Nigeria', 'description': 'Ground melon seeds for making delicious egusi soup.'},
            
            # Rice
            {'name': 'Parboiled Rice (25lbs)', 'category': 'Rice', 'price': 25.99, 'stock_quantity': 30, 'country_of_origin': 'Nigeria', 'description': 'Premium parboiled long grain rice, 25 pound bag.'},
            {'name': 'Jasmine Rice (10lbs)', 'category': 'Rice', 'price': 12.99, 'stock_quantity': 40, 'country_of_origin': 'Thailand', 'description': 'Fragrant jasmine rice for special occasions.'},
            
            # Beans
            {'name': 'Honey Beans (7lbs)', 'category': 'Beans', 'price': 9.99, 'stock_quantity': 50, 'country_of_origin': 'Nigeria', 'description': 'Premium Nigerian honey beans, perfect for traditional dishes.'},
            {'name': 'Black Eyed Peas (5lbs)', 'category': 'Beans', 'price': 7.99, 'stock_quantity': 45, 'country_of_origin': 'Nigeria', 'description': 'Quality black eyed peas for soups and stews.'},
            
            # Seasonings
            {'name': 'Suya Spice Mix', 'category': 'Seasonings', 'price': 5.99, 'stock_quantity': 80, 'country_of_origin': 'Nigeria', 'description': 'Authentic Nigerian suya spice blend for grilled meats.'},
            {'name': 'Uda (Negro Pepper)', 'category': 'Seasonings', 'price': 4.99, 'stock_quantity': 50, 'country_of_origin': 'Ghana', 'description': 'Traditional West African spice with aromatic flavor.'},
            {'name': 'Uziza Seeds', 'category': 'Seasonings', 'price': 6.99, 'stock_quantity': 35, 'country_of_origin': 'Nigeria', 'description': 'Aromatic seeds used in traditional Nigerian soups.'},
            {'name': 'Maggi Cubes (Chicken)', 'category': 'Seasonings', 'price': 3.99, 'stock_quantity': 100, 'country_of_origin': 'Nigeria', 'description': 'Popular seasoning cubes for African dishes.'},
            {'name': 'Maggi Cubes (Beef)', 'category': 'Seasonings', 'price': 3.99, 'stock_quantity': 100, 'country_of_origin': 'Nigeria', 'description': 'Beef-flavored seasoning cubes.'},
            
            # Oils
            {'name': 'Red Palm Oil', 'category': 'Oils', 'price': 11.99, 'stock_quantity': 55, 'country_of_origin': 'Ghana', 'description': 'Authentic red palm oil, essential for African cooking.'},
            {'name': 'Palm Kernel Oil', 'category': 'Oils', 'price': 10.99, 'stock_quantity': 40, 'country_of_origin': 'Nigeria', 'description': 'Traditional palm kernel oil for cooking.'},
            {'name': 'Coconut Oil', 'category': 'Oils', 'price': 12.99, 'stock_quantity': 35, 'country_of_origin': 'Ghana', 'description': 'Pure coconut oil for cooking and health.'},
            
            # Snacks
            {'name': 'Chin Chin', 'category': 'Snacks', 'price': 4.99, 'stock_quantity': 70, 'country_of_origin': 'Nigeria', 'description': 'Crispy fried snack, a favorite across West Africa.'},
            {'name': 'Plantain Chips', 'category': 'Snacks', 'price': 5.99, 'stock_quantity': 65, 'country_of_origin': 'Ghana', 'description': 'Crunchy plantain chips, perfect for snacking.'},
            {'name': 'Buns (African Donuts)', 'category': 'Snacks', 'price': 6.99, 'stock_quantity': 40, 'country_of_origin': 'Nigeria', 'description': 'Sweet African-style donuts.'},
            
            # Drinks
            {'name': 'Milo', 'category': 'Drinks', 'price': 5.99, 'stock_quantity': 90, 'country_of_origin': 'Nigeria', 'description': 'Popular chocolate malt drink.'},
            {'name': 'Malta Guinness', 'category': 'Drinks', 'price': 3.99, 'stock_quantity': 85, 'country_of_origin': 'Nigeria', 'description': 'Non-alcoholic malt beverage.'},
            {'name': 'Fanta Orange (African)', 'category': 'Drinks', 'price': 2.99, 'stock_quantity': 100, 'country_of_origin': 'Nigeria', 'description': 'Popular orange soft drink.'},
            
            # Frozen
            {'name': 'Frozen Goat Meat (1lb)', 'category': 'Frozen', 'price': 12.99, 'stock_quantity': 25, 'country_of_origin': 'USA', 'description': 'Premium frozen goat meat, cut and ready to cook.'},
            {'name': 'Frozen Turkey Wings (3lbs)', 'category': 'Frozen', 'price': 15.99, 'stock_quantity': 30, 'country_of_origin': 'USA', 'description': 'Fresh frozen turkey wings, perfect for stews.'},
            
            # Meat
            {'name': 'Beef Shank (Boneless)', 'category': 'Meat', 'price': 17.99, 'stock_quantity': 20, 'country_of_origin': 'USA', 'description': 'Premium boneless beef shank for soups and stews.'},
            {'name': 'Stewing Hen (6lbs)', 'category': 'Meat', 'price': 15.99, 'stock_quantity': 15, 'country_of_origin': 'USA', 'description': 'Whole stewing hen, perfect for traditional dishes.'},
            
            # Seafood
            {'name': 'Mackerel Fish (Titus)', 'category': 'Seafood', 'price': 24.99, 'stock_quantity': 20, 'country_of_origin': 'Nigeria', 'description': 'Fresh mackerel fish, nutritious and flavorful.'},
            {'name': 'Titus Sardine (125g)', 'category': 'Seafood', 'price': 1.99, 'stock_quantity': 100, 'country_of_origin': 'Nigeria', 'description': 'Canned sardines in vegetable oil.'},
            
            # Produce
            {'name': 'Fresh Yam', 'category': 'Produce', 'price': 12.99, 'stock_quantity': 30, 'country_of_origin': 'Ghana', 'description': 'Fresh yam tubers, perfect for traditional dishes.'},
            {'name': 'Red Bell Pepper', 'category': 'Produce', 'price': 7.99, 'stock_quantity': 40, 'country_of_origin': 'USA', 'description': 'Fresh red bell peppers, great for cooking.'},
            {'name': 'Roma Tomatoes', 'category': 'Produce', 'price': 5.99, 'stock_quantity': 50, 'country_of_origin': 'USA', 'description': 'Fresh Roma tomatoes for stews and sauces.'},
            
            # Breakfast
            {'name': 'Agege Bread', 'category': 'Breakfast', 'price': 6.99, 'stock_quantity': 60, 'country_of_origin': 'Nigeria', 'description': 'Traditional Nigerian Agege bread, soft and delicious.'},
            
            # Condiments
            {'name': 'Tomato Paste (6oz)', 'category': 'Condiments', 'price': 2.99, 'stock_quantity': 80, 'country_of_origin': 'Nigeria', 'description': 'Concentrated tomato paste for cooking.'},
            {'name': 'Soy Sauce (500ml)', 'category': 'Condiments', 'price': 4.99, 'stock_quantity': 70, 'country_of_origin': 'Nigeria', 'description': 'Traditional soy sauce for seasoning.'},
            
            # Canned Goods
            {'name': 'Stockfish Bits', 'category': 'Canned Goods', 'price': 13.99, 'stock_quantity': 30, 'country_of_origin': 'Norway', 'description': 'Dried stockfish bits for traditional soups.'},
            {'name': 'Dried Fish', 'category': 'Canned Goods', 'price': 12.99, 'stock_quantity': 40, 'country_of_origin': 'Ghana', 'description': 'Dried fish for African dishes.'},
            {'name': 'Palm Nut Cream', 'category': 'Canned Goods', 'price': 8.99, 'stock_quantity': 50, 'country_of_origin': 'Ghana', 'description': 'Creamed palm nuts for soups.'},
        ]
        
        created_count = 0
        for prod_data in products_data:
            category = categories.get(prod_data['category'])
            if category:
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    defaults={
                        'category': category,
                        'price': prod_data['price'],
                        'stock_quantity': prod_data['stock_quantity'],
                        'country_of_origin': prod_data.get('country_of_origin', ''),
                        'description': prod_data.get('description', ''),
                        'is_available': True,
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully seeded {created_count} products!'))

