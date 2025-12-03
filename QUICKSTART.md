# Quick Start Guide - Makola Marketplace

## Immediate Next Steps

### 1. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit `.env` and update at minimum:
- `SECRET_KEY` - Generate a new one: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Database credentials (if using PostgreSQL) OR switch to SQLite for quick testing

### 4. Set Up Database

**Option A: Quick Start with SQLite (for testing)**
- No setup needed! SQLite works out of the box
- Just skip database configuration in `.env`

**Option B: PostgreSQL (recommended for production)**
```bash
# Install PostgreSQL, then:
createdb makola_marketplace
# Update .env with your DB credentials
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Seed Sample Products (Optional)

```bash
python manage.py seed_products
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

## Testing Checklist

- [ ] Homepage loads
- [ ] Can view products
- [ ] Can register new account
- [ ] Can login
- [ ] Can add products to cart
- [ ] Can view cart
- [ ] Can access admin panel at /admin/
- [ ] Can view product details
- [ ] Can search products

## Common Issues & Solutions

### Issue: ModuleNotFoundError
**Solution:** Make sure virtual environment is activated and dependencies are installed

### Issue: Database connection error
**Solution:** 
- For quick testing: Use SQLite (remove DB config from .env)
- For PostgreSQL: Check database exists and credentials are correct

### Issue: Static files not loading
**Solution:** Run `python manage.py collectstatic` (not needed in development with DEBUG=True)

### Issue: Stripe payment not working
**Solution:** Add your Stripe test keys to `.env` (get from https://dashboard.stripe.com/test/apikeys)

## What to Do After Setup

1. **Explore Admin Panel**
   - Go to http://localhost:8000/admin/
   - Login with superuser credentials
   - Add/edit products, categories
   - View orders

2. **Test User Flow**
   - Register a new account
   - Browse products
   - Add items to cart
   - Complete checkout (use Stripe test card: 4242 4242 4242 4242)

3. **Customize**
   - Update store information in templates
   - Add your own product images
   - Customize colors/styling in templates
   - Configure email settings

4. **Prepare for Production**
   - Read DEPLOYMENT.md
   - Set up production database
   - Configure production email
   - Set up SSL certificate
   - Configure production Stripe keys

## Need Help?

- Check README.md for detailed documentation
- Check DEPLOYMENT.md for production setup
- Review Django documentation: https://docs.djangoproject.com/



