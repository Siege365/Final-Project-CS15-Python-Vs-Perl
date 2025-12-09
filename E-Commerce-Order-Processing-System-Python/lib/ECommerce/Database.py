"""
ShopPy - Database Module
Handles database initialization and sample data.
Equivalent to Perl ECommerce::Database
"""

import os
from pathlib import Path
from django.conf import settings


def get_db_path():
    """Get database file path."""
    return settings.DATABASES['default']['NAME']


def initialize_database():
    """
    Initialize database and create sample data if needed.
    Called from management command or startup.
    """
    from django.core.management import call_command
    from lib.ECommerce.Models.User import User
    from lib.ECommerce.Models.Customer import Customer
    from lib.ECommerce.Models.Product import Product

    # Ensure data directory exists
    db_path = Path(get_db_path())
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Run migrations
    call_command('migrate', verbosity=0)

    # Check if we need to create sample data
    if User.objects.count() == 0:
        create_sample_data()
        print("Database initialized with sample data.")


def create_sample_data():
    """Create initial sample data for the application."""
    from lib.ECommerce.Models.User import User
    from lib.ECommerce.Models.Customer import Customer
    from lib.ECommerce.Models.Product import Product

    # Create default users
    users_data = [
        {'username': 'admin', 'email': 'admin@shoppy.com', 'password': 'admin123', 'role': 'admin'},
        {'username': 'staff', 'email': 'staff@shoppy.com', 'password': 'staff123', 'role': 'staff'},
        {'username': 'customer', 'email': 'customer@shoppy.com', 'password': 'customer123', 'role': 'customer'},
    ]

    for user_data in users_data:
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role=user_data['role']
        )

        # Create customer profile for customer user
        if user_data['role'] == 'customer':
            Customer.objects.create(
                user=user,
                first_name='John',
                last_name='Doe',
                phone='555-0101',
                address='123 Main St',
                city='New York',
                state='NY',
                zip_code='10001'
            )

    # Create additional sample customers
    customers_data = [
        {'first_name': 'Jane', 'last_name': 'Smith', 'phone': '555-0102',
         'address': '456 Oak Ave', 'city': 'Los Angeles', 'state': 'CA', 'zip_code': '90001'},
        {'first_name': 'Bob', 'last_name': 'Johnson', 'phone': '555-0103',
         'address': '789 Pine Rd', 'city': 'Chicago', 'state': 'IL', 'zip_code': '60601'},
        {'first_name': 'Alice', 'last_name': 'Williams', 'phone': '555-0104',
         'address': '321 Elm St', 'city': 'Houston', 'state': 'TX', 'zip_code': '77001'},
    ]

    for cust_data in customers_data:
        Customer.objects.create(**cust_data)

    # Create sample products
    products_data = [
        {'name': 'Wireless Bluetooth Headphones', 'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life.',
         'sku': 'ELEC-001', 'category': 'Electronics', 'price': 149.99, 'cost': 75.00, 'stock_quantity': 50,
         'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop'},
        {'name': 'Smart Watch Pro', 'description': 'Feature-rich smartwatch with health monitoring, GPS, and water resistance.',
         'sku': 'ELEC-002', 'category': 'Electronics', 'price': 299.99, 'cost': 150.00, 'stock_quantity': 30,
         'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop'},
        {'name': 'Portable Bluetooth Speaker', 'description': 'Compact speaker with powerful bass and 12-hour playtime.',
         'sku': 'ELEC-003', 'category': 'Electronics', 'price': 79.99, 'cost': 35.00, 'stock_quantity': 75,
         'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=300&fit=crop'},
        {'name': 'Classic Denim Jacket', 'description': 'Timeless denim jacket with comfortable fit and stylish design.',
         'sku': 'CLOTH-001', 'category': 'Clothing', 'price': 89.99, 'cost': 40.00, 'stock_quantity': 40,
         'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=300&fit=crop'},
        {'name': 'Running Sneakers', 'description': 'Lightweight running shoes with responsive cushioning.',
         'sku': 'CLOTH-002', 'category': 'Clothing', 'price': 129.99, 'cost': 55.00, 'stock_quantity': 60,
         'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop'},
        {'name': 'Python Programming Book', 'description': 'Comprehensive guide to Python programming for beginners and experts.',
         'sku': 'BOOK-001', 'category': 'Books', 'price': 49.99, 'cost': 20.00, 'stock_quantity': 100,
         'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=300&fit=crop'},
        {'name': 'Yoga Mat Premium', 'description': 'Extra thick, non-slip yoga mat with carrying strap.',
         'sku': 'SPORT-001', 'category': 'Sports', 'price': 39.99, 'cost': 15.00, 'stock_quantity': 80,
         'image_url': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=300&fit=crop'},
        {'name': 'Ceramic Coffee Mug Set', 'description': 'Set of 4 elegant ceramic mugs, microwave and dishwasher safe.',
         'sku': 'HOME-001', 'category': 'Home', 'price': 34.99, 'cost': 12.00, 'stock_quantity': 45,
         'image_url': 'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400&h=300&fit=crop'},
        {'name': 'LED Desk Lamp', 'description': 'Adjustable LED lamp with multiple brightness levels and USB charging port.',
         'sku': 'HOME-002', 'category': 'Home', 'price': 59.99, 'cost': 25.00, 'stock_quantity': 35,
         'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=300&fit=crop'},
        {'name': 'Building Blocks Set', 'description': 'Creative building blocks set with 500 pieces for endless fun.',
         'sku': 'TOY-001', 'category': 'Toys', 'price': 44.99, 'cost': 18.00, 'stock_quantity': 55,
         'image_url': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=300&fit=crop'},
        {'name': 'Organic Skincare Set', 'description': 'All-natural skincare collection with cleanser, toner, and moisturizer.',
         'sku': 'BEAUTY-001', 'category': 'Beauty', 'price': 69.99, 'cost': 30.00, 'stock_quantity': 25,
         'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=300&fit=crop'},
        {'name': 'Car Phone Mount', 'description': 'Universal magnetic phone mount with 360-degree rotation.',
         'sku': 'AUTO-001', 'category': 'Automotive', 'price': 24.99, 'cost': 8.00, 'stock_quantity': 90,
         'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop'},
        {'name': 'Gourmet Coffee Beans', 'description': 'Premium arabica coffee beans, medium roast, 1kg bag.',
         'sku': 'FOOD-001', 'category': 'Food', 'price': 29.99, 'cost': 12.00, 'stock_quantity': 0,
         'image_url': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=300&fit=crop'},
        {'name': 'Wireless Charging Pad', 'description': 'Fast wireless charger compatible with all Qi-enabled devices.',
         'sku': 'ELEC-004', 'category': 'Electronics', 'price': 34.99, 'cost': 12.00, 'stock_quantity': 5,
         'image_url': 'https://images.unsplash.com/photo-1586816879360-004f5b0c51e5?w=400&h=300&fit=crop'},
        {'name': 'Mechanical Keyboard', 'description': 'RGB mechanical keyboard with customizable keys and wrist rest.',
         'sku': 'ELEC-005', 'category': 'Electronics', 'price': 119.99, 'cost': 50.00, 'stock_quantity': 20,
         'image_url': 'https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=400&h=300&fit=crop'},
    ]

    for prod_data in products_data:
        Product.objects.create(**prod_data)

    print(f"Created {len(users_data)} users, {len(customers_data) + 1} customers, {len(products_data)} products")
