import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knead_backend.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get('ADMIN_USER', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@kneadmassage.com')
password = os.environ.get('ADMIN_PASS', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")
