"""
ShopPy - E-Commerce Order Processing System
Django Configuration (Settings)

This module contains all Django configuration settings for the ShopPy application.
Equivalent to the Perl ECommerce::Config module.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Load from environment variable, use a default only for development
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'dev-secret-key-change-in-production'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lib.ECommerce',  # Our main e-commerce application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lib.ECommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'lib.ECommerce.context_processors.cart_context',
                'lib.ECommerce.context_processors.app_config',
            ],
        },
    },
]

WSGI_APPLICATION = 'lib.ECommerce.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data' / 'ecommerce.db',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]

# Custom User Model
AUTH_USER_MODEL = 'ECommerce.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'public']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/Logout URLs
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Session settings (1 hour expiration like Perl version)
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Message settings
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# =============================================================================
# APPLICATION CONFIGURATION (Equivalent to Perl %APP_CONFIG)
# =============================================================================

APP_CONFIG = {
    'app_name': 'ShopPy',
    'slogan': 'Wrapped in code, packed with deals',
    'version': '1.0.0',
    'currency': 'USD',
    'currency_symbol': '$',
    'tax_rate': 0.08,  # 8%
    'shipping_rate': 5.00,
    'free_shipping_threshold': 100.00,
    'items_per_page': 20,
}

# Order status values
ORDER_STATUS = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
    ('refunded', 'Refunded'),
]

# Payment methods
PAYMENT_METHODS = [
    ('credit_card', 'Credit Card'),
    ('debit_card', 'Debit Card'),
    ('paypal', 'PayPal'),
    ('cash_on_delivery', 'Cash on Delivery'),
    ('bank_transfer', 'Bank Transfer'),
]

# Product categories
PRODUCT_CATEGORIES = [
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing'),
    ('Books', 'Books'),
    ('Home', 'Home'),
    ('Sports', 'Sports'),
    ('Toys', 'Toys'),
    ('Food', 'Food'),
    ('Beauty', 'Beauty'),
    ('Automotive', 'Automotive'),
    ('Other', 'Other'),
]

# User roles
USER_ROLES = [
    ('admin', 'Admin'),
    ('staff', 'Staff'),
    ('customer', 'Customer'),
]

# Color scheme (matching Perl version)
COLORS = {
    'primary': '#3776AB',      # Python blue
    'secondary': '#FFD43B',    # Python yellow
    'success': '#06A77D',
    'warning': '#F18F01',
    'danger': '#C73E1D',
    'info': '#4A90E2',
    'light': '#F5F5F5',
    'dark': '#333333',
}
