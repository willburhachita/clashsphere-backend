#!/bin/bash
set -e  # Exit on any error

echo "🚀 Starting Django application..."
echo "Environment: $RAILWAY_ENVIRONMENT_NAME"
echo "Port: ${PORT:-8000}"

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

# Get the port from Railway environment or default to 8000
PORT=${PORT:-8000}

# Test if we can start Django development server first
echo "🧪 Testing Django app startup..."
timeout 5 python manage.py runserver 0.0.0.0:$PORT &
sleep 2
pkill -f runserver || true

# Start the application with simpler gunicorn config
echo "🌐 Starting gunicorn on port $PORT..."
exec gunicorn common.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 60 \
    --log-level debug \
    --access-logfile - \
    --error-logfile - 