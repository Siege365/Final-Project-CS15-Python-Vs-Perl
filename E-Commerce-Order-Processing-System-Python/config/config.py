"""
Application Configuration
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Database configuration
DATABASE_PATH = BASE_DIR / 'data' / 'ecommerce.db'

# Application configuration
APP_CONFIG = {
    'app_name': 'E-Commerce Order Processing System',
    'version': '1.0.0',
    'currency': 'USD',
    'currency_symbol': '$',
    'tax_rate': 0.08,  # 8% tax
    'shipping_cost': 10.00,
    'free_shipping_threshold': 100.00,
}

# Order status options
ORDER_STATUS = [
    'Pending',
    'Processing',
    'Shipped',
    'Delivered',
    'Cancelled',
    'Refunded'
]

# Payment methods
PAYMENT_METHODS = [
    'Credit Card',
    'Debit Card',
    'PayPal',
    'Cash on Delivery',
    'Bank Transfer'
]

# Product categories
PRODUCT_CATEGORIES = [
    'Electronics',
    'Clothing',
    'Home & Garden',
    'Sports & Outdoors',
    'Books',
    'Toys & Games',
    'Health & Beauty',
    'Food & Beverages',
    'Automotive',
    'Other'
]

# User roles
USER_ROLES = ['admin', 'staff', 'customer']

# Pagination
ITEMS_PER_PAGE = 10

# Color scheme (no gradients)
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#06A77D',
    'warning': '#F18F01',
    'danger': '#C73E1D',
    'info': '#6C757D',
    'light': '#F8F9FA',
    'dark': '#212529',
    'background': '#FFFFFF',
    'sidebar': '#F0F2F6'
}
