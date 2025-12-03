"""
Management command to automatically create a superuser.
Uses environment variables for credentials.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser automatically using environment variables'

    def handle(self, *args, **options):
        # Get credentials from environment variables
        username = config('SUPERUSER_USERNAME', default='admin')
        email = config('SUPERUSER_EMAIL', default='admin@makolamarketplace.com')
        password = config('SUPERUSER_PASSWORD', default='')
        
        # If no password is set, generate a random one
        if not password:
            from django.core.management.utils import get_random_secret_key
            password = get_random_secret_key()[:20]
            self.stdout.write(
                self.style.WARNING(
                    f'No SUPERUSER_PASSWORD set. Generated password: {password}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'Please save this password and set SUPERUSER_PASSWORD in Railway for future use.'
                )
            )
        
        # Check if superuser already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists. Skipping creation.')
            )
            return
        
        # Create superuser
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser "{username}" with email "{email}"'
                )
            )
            if not config('SUPERUSER_PASSWORD', default=''):
                self.stdout.write(
                    self.style.SUCCESS(f'Password: {password}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )

