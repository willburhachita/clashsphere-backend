#!/bin/bash
set -e  # Exit on any error

echo "🚀 Starting Django application..."
echo "Environment: $RAILWAY_ENVIRONMENT_NAME"

# Railway often uses PORT, but fallback to 8000
export PORT=${PORT:-8000}
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

# Test if we can start Django development server first
echo "🧪 Testing Django app startup..."
timeout 5 python manage.py runserver 0.0.0.0:$PORT &
sleep 2
pkill -f runserver || true

# Start the application with Railway-optimized gunicorn config
echo "🌐 Starting gunicorn on 0.0.0.0:$PORT..."
exec gunicorn common.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --worker-class sync \
    --timeout 60 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --log-level info \
    --access-logfile - \
    --error-logfile - 