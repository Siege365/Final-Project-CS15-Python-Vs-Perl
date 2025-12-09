"""
Create initial admin superuser for ShopPy
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lib.ECommerce.Config')
django.setup()

from lib.ECommerce.Models.User import User
from lib.ECommerce.Models.Customer import Customer

# Create superuser
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@shoppy.com',
        password='admin123'
    )
    print(f"✅ Created admin user")
    print(f"   Username: admin")
    print(f"   Email: admin@shoppy.com")
    print(f"   Password: admin123")
    print(f"   Please change this password after first login!")
else:
    print("⚠️  Admin user already exists")
