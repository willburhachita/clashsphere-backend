#!/bin/bash
set -e  # Exit on any error

echo "🚀 Starting Django application..."
echo "Environment: $RAILWAY_ENVIRONMENT_NAME"
echo "Port: ${PORT:-8000}"

# Wait for database to be ready
echo "⏳ Waiting for database..."
sleep 5

# Test database connection
echo "🔍 Testing database connection..."
python manage.py check --database default

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate

# Get the port from Railway environment or default to 8000
PORT=${PORT:-8000}

# Start the application
echo "🌐 Starting application on port $PORT..."
echo "Gunicorn command: gunicorn common.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120"

# Add health check endpoint test
echo "🏥 Starting gunicorn server..."
exec gunicorn common.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info 