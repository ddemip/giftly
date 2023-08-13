#!/bin/bash

# Check if the superuser already exists
if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(not User.objects.filter(username='admin').exists())"; then
  # Create the superuser
  python manage.py createsuperuser --username admin --no-input
fi

# Run the Django server
python manage.py migrate
python manage.py runserver 0.0.0.0:8000