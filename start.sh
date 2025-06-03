#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
sleep 5

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Start the application
echo "Starting application..."
exec gunicorn common.wsgi:application --bind 0.0.0.0:8000 