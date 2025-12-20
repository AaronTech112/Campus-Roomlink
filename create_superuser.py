import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roomlink.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@roomlink.com').exists():
    User.objects.create_superuser('admin@roomlink.com', 'admin123', full_name='Admin User', phone_number='0000000000')
    print("Superuser created: admin@roomlink.com / admin123")
else:
    print("Superuser already exists")
