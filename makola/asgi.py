"""
ASGI config for Makola Marketplace project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'makola.settings')

application = get_asgi_application()



