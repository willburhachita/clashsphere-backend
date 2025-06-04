#!/bin/bash
set -e  # Exit on any error

echo "🚀 Starting Django application..."
echo "Environment: $RAILWAY_ENVIRONMENT_NAME"

# Railway often uses PORT, but fallback to 8000
export PORT=${PORT:-8080}
echo "Port: $PORT"

# Check if we can import Django
echo "🐍 Testing Python and Django..."
python -c "import django; print(f'Django version: {django.get_version()}')"

# Test WSGI application
echo "🧪 Testing WSGI application..."
python test_wsgi.py

# Check Django configuration
echo "🔍 Testing Django configuration..."
python manage.py check

# Wait for database to be ready
echo "⏳ Waiting for database..."
sleep 3

# Test database connection (but don't fail if it doesn't work yet)
echo "🔍 Testing database connection..."
python manage.py check --database default || echo "Database check failed, but continuing..."

# Try to run migrations (but don't fail the startup if this fails)
echo "🔄 Running migrations..."
python manage.py migrate || echo "Migration failed, but continuing..."

# Try to collect static files (but don't fail if this fails)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput || echo "Static files collection failed, but continuing..."

# Test Django app with a simple command
echo "🧪 Testing Django app can load URLs..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'environment.main')
import django
django.setup()
from django.urls import reverse
from django.test import Client
client = Client()
try:
    response = client.get('/health/')
    print(f'Health check response: {response.status_code}')
except Exception as e:
    print(f'Health check failed: {e}')
"

# Start the application with Railway-optimized gunicorn config
echo "🌐 Starting gunicorn on 0.0.0.0:$PORT..."
echo "🔧 Gunicorn command:"
echo "gunicorn common.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --log-level debug"

# Use simpler config with more verbose logging
exec gunicorn common.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --worker-class sync \
    --timeout 300 \
    --graceful-timeout 30 \
    --log-level debug \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance 