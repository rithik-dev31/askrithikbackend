#!/usr/bin/env bash
# Exit immediately if any command fails
set -o errexit

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Applying database migrations..."
python manage.py migrate

echo "==> Ensuring superuser exists..."
python manage.py createsuperuser --noinput || true

echo "==> Build complete."