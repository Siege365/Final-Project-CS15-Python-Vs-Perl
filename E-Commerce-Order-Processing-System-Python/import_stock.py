#!/usr/bin/env python
"""
Import stock quantities for products.
Usage: python import_stock.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lib.ECommerce.Config')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from lib.ECommerce.Models.Product import Product

# Stock data - map product names to stock quantities
# These are realistic stock quantities for various product categories
STOCK_DATA = {
    'Badminton Racket': 45,
    'Blender Pro': 38,
    'Bluetooth Speaker': 52,
    'Board Game Classic': 48,
    'Car Phone Mount': 75,
    'Coffee Maker': 32,
    'Cookbook Deluxe': 55,
    'Dumbbells Set': 28,
    'Face Cream': 85,
    'Hoodie Comfort': 40,
    'Jeans Denim': 65,
    'Laptop Pro 15"': 18,
    'Mechanical Keyboard': 42,
    'Programming Python': 35,
    'Puzzle 1000pc': 50,
    'Shampoo Premium': 95,
    'T-Shirt Classic': 120,
    'Tire Pressure Gauge': 58,
    'USB-C Hub': 62,
    'Webcam HD': 45,
    'Wireless Headphones': 48,
    'Wireless Mouse': 85,
    'Yoga Mat': 55,
}

def import_stock():
    """Import stock quantities for products."""
    total = 0
    updated = 0
    failed = 0
    
    print("=" * 60)
    print("IMPORTING PRODUCT STOCK")
    print("=" * 60)
    
    for product_name, stock_qty in STOCK_DATA.items():
        try:
            product = Product.objects.get(name__iexact=product_name)
            old_stock = product.stock_quantity
            product.stock_quantity = stock_qty
            product.save()
            
            print(f"✓ {product.name}")
            print(f"  SKU: {product.sku}")
            print(f"  Stock: {old_stock} → {stock_qty}")
            print()
            
            updated += 1
            total += stock_qty
            
        except Product.DoesNotExist:
            print(f"✗ Product not found: {product_name}")
            failed += 1
            print()
    
    # Also update any remaining products with random stock
    remaining = Product.objects.filter(stock_quantity=0)
    for product in remaining:
        import random
        stock_qty = random.randint(10, 100)
        product.stock_quantity = stock_qty
        product.save()
        print(f"+ {product.name}")
        print(f"  SKU: {product.sku}")
        print(f"  Stock: {stock_qty} (auto-assigned)")
        print()
        updated += 1
        total += stock_qty
    
    print("=" * 60)
    print("IMPORT SUMMARY")
    print("=" * 60)
    print(f"Total products updated: {updated}")
    print(f"Total stock quantity: {total}")
    print(f"Failed: {failed}")
    print()
    
    # Show final inventory
    products = Product.objects.all()
    print("FINAL INVENTORY:")
    print(f"Total products: {products.count()}")
    total_stock = sum(p.stock_quantity for p in products)
    print(f"Total stock items: {total_stock}")
    print()
    
    # Show low stock items
    low_stock = products.filter(stock_quantity__lte=10)
    if low_stock.exists():
        print("LOW STOCK ITEMS:")
        for product in low_stock:
            status = "⚠️ " if product.stock_quantity <= 5 else "⏱️ "
            print(f"{status} {product.name}: {product.stock_quantity} units")
        print()

if __name__ == '__main__':
    import_stock()
