#!/bin/bash
# Railway startup script - runs migrations and starts the server

set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn makola.wsgi:application --bind 0.0.0.0:$PORT

