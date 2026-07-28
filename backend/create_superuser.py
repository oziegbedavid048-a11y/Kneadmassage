import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knead_backend.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get('ADMIN_USER', 'Knead')
email = os.environ.get('ADMIN_EMAIL', 'hello@kneadhushedmassage.com')
password = os.environ.get('ADMIN_PASS', 'Knead@768')

user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True})
user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()

if created:
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' updated with new password successfully!")
