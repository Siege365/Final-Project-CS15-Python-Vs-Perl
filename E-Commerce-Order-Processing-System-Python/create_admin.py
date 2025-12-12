"""
Create initial admin superuser for ShopPy
"""
import os
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lib.ECommerce.Config')
django.setup()

from lib.ECommerce.Models.User import User
from lib.ECommerce.Models.Customer import Customer

# Get credentials from environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@shoppy.com')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Check if password is provided
if not ADMIN_PASSWORD:
    print("❌ Error: ADMIN_PASSWORD environment variable not set!")
    print("   Please set ADMIN_PASSWORD in your .env file before running this script.")
    exit(1)

# Create superuser
if not User.objects.filter(username=ADMIN_USERNAME).exists():
    user = User.objects.create_superuser(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD
    )
    print(f"✅ Created admin user")
    print(f"   Username: {ADMIN_USERNAME}")
    print(f"   Email: {ADMIN_EMAIL}")
    print(f"   ⚠️  Please change this password after first login!")
else:
    print(f"⚠️  Admin user '{ADMIN_USERNAME}' already exists")
