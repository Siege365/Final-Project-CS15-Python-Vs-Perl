"""
Product Model - Handles product data operations
"""

import sqlite3
from datetime import datetime
from config.config import DATABASE_PATH

class ProductModel:
    def __init__(self):
        self.db_path = DATABASE_PATH
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_product(self, name, description, category, price, cost, sku, stock_quantity, reorder_level=10):
        """Create a new product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO products (name, description, category, price, cost, sku, stock_quantity, reorder_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, description, category, price, cost, sku, stock_quantity, reorder_level))
            conn.commit()
            product_id = cursor.lastrowid
            conn.close()
            return product_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def get_all_products(self, active_only=True):
        """Get all products"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if active_only:
            cursor.execute('SELECT * FROM products WHERE is_active = 1 ORDER BY name')
        else:
            cursor.execute('SELECT * FROM products ORDER BY name')
        
        products = cursor.fetchall()
        conn.close()
        return [dict(product) for product in products]
    
    def get_product_by_id(self, product_id):
        """Get product by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        conn.close()
        return dict(product) if product else None
    
    def get_product_by_sku(self, sku):
        """Get product by SKU"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE sku = ?', (sku,))
        product = cursor.fetchone()
        conn.close()
        return dict(product) if product else None
    
    def update_product(self, product_id, **kwargs):
        """Update product details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        allowed_fields = ['name', 'description', 'category', 'price', 'cost', 'sku', 
                         'stock_quantity', 'reorder_level', 'is_active']
        
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if updates:
            values.append(datetime.now())
            values.append(product_id)
            query = f"UPDATE products SET {', '.join(updates)}, updated_at = ? WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return True
    
    def delete_product(self, product_id):
        """Soft delete product (set is_active to 0)"""
        return self.update_product(product_id, is_active=0)
    
    def update_stock(self, product_id, quantity_change):
        """Update product stock quantity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE products 
            SET stock_quantity = stock_quantity + ?, updated_at = ?
            WHERE id = ?
        ''', (quantity_change, datetime.now(), product_id))
        conn.commit()
        conn.close()
        return True
    
    def get_low_stock_products(self):
        """Get products with stock below reorder level"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM products 
            WHERE stock_quantity <= reorder_level AND is_active = 1
            ORDER BY stock_quantity ASC
        ''')
        products = cursor.fetchall()
        conn.close()
        return [dict(product) for product in products]
    
    def search_products(self, search_term):
        """Search products by name, description, or SKU"""
        conn = self.get_connection()
        cursor = conn.cursor()
        search_pattern = f"%{search_term}%"
        cursor.execute('''
            SELECT * FROM products 
            WHERE (name LIKE ? OR description LIKE ? OR sku LIKE ?) AND is_active = 1
            ORDER BY name
        ''', (search_pattern, search_pattern, search_pattern))
        products = cursor.fetchall()
        conn.close()
        return [dict(product) for product in products]
    
    def get_products_by_category(self, category):
        """Get products by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM products 
            WHERE category = ? AND is_active = 1
            ORDER BY name
        ''', (category,))
        products = cursor.fetchall()
        conn.close()
        return [dict(product) for product in products]
    
    def get_categories(self):
        """Get all product categories"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT category FROM products 
            WHERE is_active = 1 AND category IS NOT NULL
            ORDER BY category
        ''')
        categories = cursor.fetchall()
        conn.close()
        return [cat['category'] for cat in categories]
