#!/bin/bash
# Railway startup script - runs migrations and starts the server

set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating categories (if not exists)..."
python manage.py create_categories || echo "Categories already exist or error occurred"

echo "Seeding products (if database is empty)..."
python manage.py seed_products || echo "Products already exist or error occurred"

echo "Creating superuser (if not exists)..."
python manage.py create_superuser_auto

echo "Starting Gunicorn..."
exec gunicorn makola.wsgi:application --bind 0.0.0.0:$PORT

