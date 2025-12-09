#!/usr/bin/env python
"""
Import products from Perl database with correct image URLs
"""
import os
import django
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lib.ECommerce.Config')
django.setup()

from lib.ECommerce.Models.Product import Product

# Product data from update_images.pl with image URLs
products_data = [
    # Electronics
    {'id': 1, 'name': 'Laptop Pro 15"', 'sku': 'ELEC-001', 'category': 'Electronics', 'description': 'High-performance laptop with 15" display', 'price': 1299.99, 'cost': 900.00, 'stock_quantity': 25, 'reorder_level': 5, 'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop'},
    {'id': 2, 'name': 'Wireless Mouse', 'sku': 'ELEC-002', 'category': 'Electronics', 'description': 'Ergonomic wireless mouse', 'price': 29.99, 'cost': 15.00, 'stock_quantity': 100, 'reorder_level': 20, 'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop'},
    {'id': 3, 'name': 'Mechanical Keyboard', 'sku': 'ELEC-003', 'category': 'Electronics', 'description': 'RGB mechanical gaming keyboard', 'price': 89.99, 'cost': 50.00, 'stock_quantity': 50, 'reorder_level': 10, 'image_url': 'https://www.popsci.com/wp-content/uploads/2022/02/12/mechanical-keyboard-with-rbg.jpg?quality=85'},
    {'id': 4, 'name': 'USB-C Hub', 'sku': 'ELEC-004', 'category': 'Electronics', 'description': '7-in-1 USB-C hub adapter', 'price': 49.99, 'cost': 25.00, 'stock_quantity': 75, 'reorder_level': 15, 'image_url': 'https://m.media-amazon.com/images/I/513AvAPJgXL._AC_UF894,1000_QL80_.jpg'},
    {'id': 5, 'name': 'Webcam HD', 'sku': 'ELEC-005', 'category': 'Electronics', 'description': '1080p HD webcam with microphone', 'price': 79.99, 'cost': 45.00, 'stock_quantity': 60, 'reorder_level': 10, 'image_url': 'https://cdn.mos.cms.futurecdn.net/NeyiJFuPXVSzH5JRp5X8H5-1200-80.jpg'},
    {'id': 21, 'name': 'Wireless Headphones', 'sku': 'ELEC-021', 'category': 'Electronics', 'description': 'Premium noise-cancelling headphones', 'price': 199.99, 'cost': 120.00, 'stock_quantity': 40, 'reorder_level': 8, 'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop'},
    {'id': 23, 'name': 'Bluetooth Speaker', 'sku': 'ELEC-023', 'category': 'Electronics', 'description': 'Portable waterproof bluetooth speaker', 'price': 59.99, 'cost': 30.00, 'stock_quantity': 80, 'reorder_level': 15, 'image_url': 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=300&fit=crop'},
    
    # Clothing
    {'id': 6, 'name': 'T-Shirt Classic', 'sku': 'CLTH-001', 'category': 'Clothing', 'description': 'Comfortable cotton t-shirt', 'price': 19.99, 'cost': 8.00, 'stock_quantity': 200, 'reorder_level': 30, 'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop'},
    {'id': 7, 'name': 'Jeans Denim', 'sku': 'CLTH-002', 'category': 'Clothing', 'description': 'Classic blue denim jeans', 'price': 59.99, 'cost': 30.00, 'stock_quantity': 120, 'reorder_level': 20, 'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=300&fit=crop'},
    {'id': 8, 'name': 'Hoodie Comfort', 'sku': 'CLTH-003', 'category': 'Clothing', 'description': 'Cozy fleece hoodie', 'price': 39.99, 'cost': 20.00, 'stock_quantity': 90, 'reorder_level': 15, 'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=300&fit=crop'},
    
    # Books
    {'id': 9, 'name': 'Programming Python', 'sku': 'BOOK-001', 'category': 'Books', 'description': 'Complete guide to Python programming', 'price': 49.99, 'cost': 25.00, 'stock_quantity': 45, 'reorder_level': 10, 'image_url': 'https://m.media-amazon.com/images/I/81YWUlX6J4L._AC_UF1000,1000_QL80_.jpg'},
    {'id': 10, 'name': 'Cookbook Deluxe', 'sku': 'BOOK-002', 'category': 'Books', 'description': 'Gourmet recipes cookbook', 'price': 34.99, 'cost': 18.00, 'stock_quantity': 55, 'reorder_level': 10, 'image_url': 'https://www.lordandlion.com/cdn/shop/products/serendip.jpg?v=1627902766&width=1445'},
    
    # Home
    {'id': 11, 'name': 'Coffee Maker', 'sku': 'HOME-001', 'category': 'Home', 'description': '5-cup programmable coffee maker', 'price': 49.99, 'cost': 25.00, 'stock_quantity': 35, 'reorder_level': 8, 'image_url': 'https://www.bhg.com/thmb/sog5eX8qb6bk4JIWdMnM4qAbQVo=/4000x0/filters:no_upscale():strip_icc()/bhg-product-mr-coffee-5-cup-mini-brew-switch-coffee-maker-14-rkilgore-1410-1-7365d15ab5594daeb983c081502ba0c4.jpeg'},
    {'id': 12, 'name': 'Blender Pro', 'sku': 'HOME-002', 'category': 'Home', 'description': 'High-speed blender 1000W', 'price': 89.99, 'cost': 50.00, 'stock_quantity': 40, 'reorder_level': 8, 'image_url': 'https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400&h=300&fit=crop'},
    
    # Sports
    {'id': 13, 'name': 'Yoga Mat', 'sku': 'SPRT-001', 'category': 'Sports', 'description': 'Non-slip yoga mat', 'price': 29.99, 'cost': 12.00, 'stock_quantity': 70, 'reorder_level': 15, 'image_url': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=300&fit=crop'},
    {'id': 14, 'name': 'Dumbbells Set', 'sku': 'SPRT-002', 'category': 'Sports', 'description': 'Adjustable dumbbell set 20kg', 'price': 79.99, 'cost': 40.00, 'stock_quantity': 30, 'reorder_level': 5, 'image_url': 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=400&h=300&fit=crop'},
    {'id': 22, 'name': 'Badminton Racket', 'sku': 'SPRT-022', 'category': 'Sports', 'description': 'Professional badminton racket', 'price': 69.99, 'cost': 35.00, 'stock_quantity': 25, 'reorder_level': 5, 'image_url': 'https://images.unsplash.com/photo-1617083934555-ac7b4d0c8be9?w=400&h=300&fit=crop'},
    
    # Toys
    {'id': 15, 'name': 'Board Game Classic', 'sku': 'TOYS-001', 'category': 'Toys', 'description': 'Classic family board game', 'price': 24.99, 'cost': 12.00, 'stock_quantity': 60, 'reorder_level': 10, 'image_url': 'https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400&h=300&fit=crop'},
    {'id': 16, 'name': 'Puzzle 1000pc', 'sku': 'TOYS-002', 'category': 'Toys', 'description': '1000-piece jigsaw puzzle', 'price': 19.99, 'cost': 8.00, 'stock_quantity': 50, 'reorder_level': 10, 'image_url': 'https://images.unsplash.com/photo-1494059980473-813e73ee784b?w=400&h=300&fit=crop'},
    
    # Beauty
    {'id': 17, 'name': 'Shampoo Premium', 'sku': 'BEAU-001', 'category': 'Beauty', 'description': 'Organic herbal shampoo', 'price': 14.99, 'cost': 6.00, 'stock_quantity': 100, 'reorder_level': 20, 'image_url': 'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=400&h=300&fit=crop'},
    {'id': 18, 'name': 'Face Cream', 'sku': 'BEAU-002', 'category': 'Beauty', 'description': 'Anti-aging face cream', 'price': 29.99, 'cost': 12.00, 'stock_quantity': 80, 'reorder_level': 15, 'image_url': 'https://www.tyoemcosmetic.com/wp-content/uploads/face-creams-manufacturer-1-1-1-768x576.jpg'},
    
    # Automotive
    {'id': 19, 'name': 'Car Phone Mount', 'sku': 'AUTO-001', 'category': 'Automotive', 'description': 'Universal car phone holder', 'price': 19.99, 'cost': 8.00, 'stock_quantity': 90, 'reorder_level': 15, 'image_url': 'https://m.media-amazon.com/images/I/716tH1xGrdL._AC_SL1500_.jpg'},
    {'id': 20, 'name': 'Tire Pressure Gauge', 'sku': 'AUTO-002', 'category': 'Automotive', 'description': 'Digital tire pressure gauge', 'price': 12.99, 'cost': 5.00, 'stock_quantity': 70, 'reorder_level': 15, 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/6/6a/ReifendruckPruefen.jpg'},
]

print("Importing products with image URLs...")
print("-" * 60)

# Delete existing products
Product.objects.all().delete()
print("✓ Cleared existing products")

# Import products
for product_data in products_data:
    product = Product.objects.create(**product_data)
    print(f"✓ Created: {product.name} (ID: {product.id})")

print("-" * 60)
print(f"\n✓ Successfully imported {len(products_data)} products!")
print("\nProduct Categories:")
categories = Product.get_categories()
for cat in categories:
    count = Product.objects.filter(category=cat).count()
    print(f"  • {cat}: {count} products")
