# Makola Marketplace - Django E-commerce Website

A complete Django e-commerce website for Makola Marketplace, an African grocery store located in Houston, Texas.

## Features

- **User Authentication**: Custom user model with email verification and password reset
- **Product Catalog**: Comprehensive product management with categories, images, and reviews
- **Shopping Cart**: Session-based cart for guests and database cart for authenticated users
- **Order Management**: Complete order processing with Stripe payment integration
- **Store Information**: About, Contact pages with Google Maps integration
- **Newsletter**: Subscription management for marketing
- **Admin Dashboard**: Customized Django admin for easy management
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **SEO Optimized**: Meta tags and sitemap support

## Technology Stack

- Django 5.x
- PostgreSQL
- Tailwind CSS
- Alpine.js
- Stripe (Payment Processing)
- Python 3.11+

## Project Structure

```
makola_marketplace/
├── manage.py
├── requirements.txt
├── .env.example
├── makola/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/            # User authentication app
├── products/            # Product catalog app
├── cart/                # Shopping cart app
├── orders/              # Order management app
├── store/               # Store info & pages app
├── static/              # CSS, JS, images
└── templates/           # HTML templates
```

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Africanstore
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy `.env.example` to `.env` and fill in your configuration:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
- Database credentials
- Secret key
- Stripe API keys
- Email configuration

### 5. Set Up PostgreSQL Database

Create a PostgreSQL database:

```sql
CREATE DATABASE makola_marketplace;
```

Update your `.env` file with database credentials.

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Seed Sample Products (Optional)

```bash
python manage.py seed_products
```

### 9. Collect Static Files

```bash
python manage.py collectstatic
```

### 10. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the website.

## Configuration

### Database

The project uses PostgreSQL. Make sure PostgreSQL is installed and running, then update the database settings in `.env`:

```
DB_NAME=makola_marketplace
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Stripe Integration

1. Sign up for a Stripe account at https://stripe.com
2. Get your API keys from the Stripe Dashboard
3. Add them to your `.env` file:
   ```
   STRIPE_PUBLIC_KEY=pk_test_...
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_WEBHOOK_SECRET=whsec_...
   ```

### Email Configuration

For development, emails are sent to the console. For production, configure SMTP settings in `.env`:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## Apps Overview

### Accounts App
- Custom User model with additional fields
- Email verification
- Password reset functionality
- User profile management

### Products App
- Category management
- Product catalog with images
- Product reviews and ratings
- Search and filtering

### Cart App
- Session-based cart for guests
- Database cart for authenticated users
- Cart persistence

### Orders App
- Order creation and management
- Stripe payment integration
- Order tracking
- Order history

### Store App
- About page
- Contact page with Google Maps
- Newsletter subscription

## Admin Panel

Access the admin panel at `/admin/` with your superuser credentials.

The admin panel includes:
- Product and category management
- Order management with status updates
- User management
- Newsletter subscriber management
- Sales analytics (can be extended)

## Testing

Run tests with:

```bash
python manage.py test
```

## Production Deployment

### Security Checklist

1. Set `DEBUG=False` in production
2. Update `ALLOWED_HOSTS` in settings
3. Use a secure secret key
4. Enable HTTPS
5. Configure proper email backend
6. Set up proper database backups
7. Use environment variables for sensitive data

### Deployment Steps

1. Set up a production server (e.g., AWS, DigitalOcean, Heroku)
2. Install PostgreSQL
3. Configure environment variables
4. Run migrations
5. Collect static files
6. Set up a web server (Nginx + Gunicorn)
7. Configure SSL certificate
8. Set up domain and DNS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is proprietary software for Makola Marketplace.

## Support

For support, contact the development team or visit the store at:
- Location: Houston, Texas
- Coordinates: 29.6556701, -95.5355849

## Acknowledgments

- Django Framework
- Tailwind CSS
- Stripe for payment processing
- All contributors and testers







# Redeploy trigger: Wed Dec 10 01:16:21 CST 2025
