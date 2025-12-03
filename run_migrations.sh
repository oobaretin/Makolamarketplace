#!/bin/bash
# Railway Migration Script
# Run this script to set up your Railway deployment

echo "Linking to Railway project..."
npx @railway/cli link

echo ""
echo "Running database migrations..."
npx @railway/cli run python manage.py migrate

echo ""
echo "Collecting static files..."
npx @railway/cli run python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next step: Create superuser"
echo "Run: npx @railway/cli run python manage.py createsuperuser"



