#!/bin/bash

# Makola Marketplace Setup Script

echo "Setting up Makola Marketplace..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your configuration!"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser (optional)
echo "Would you like to create a superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

# Seed products (optional)
echo "Would you like to seed sample products? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py seed_products
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete! Run 'python manage.py runserver' to start the development server."

