!/usr/bin/env bash

set -e  
PROJECT_DIR="$pwd"

pip install -r "$PROJECT_DIR/requirements.txt"

python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$django_admin_username', '$django_admin_email', '$django_admin_password')" | python manage.py shell

echo "Setup completed"