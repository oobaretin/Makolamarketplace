#!/usr/bin/env python
"""Script to create a superuser non-interactively."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'makola.settings')
django.setup()

from accounts.models import User

# Create superuser if it doesn't exist
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        email='admin@makola.com',
        username='admin',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print("Superuser created successfully!")
    print("Email: admin@makola.com")
    print("Password: admin123")
    print("\n⚠️  IMPORTANT: Change this password in production!")
else:
    print("Superuser already exists.")



