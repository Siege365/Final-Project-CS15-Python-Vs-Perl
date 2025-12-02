"""
Order Model - Handles order data operations
"""

import sqlite3
from datetime import datetime
import random
import string
from config.config import DATABASE_PATH

class OrderModel:
    def __init__(self):
        self.db_path = DATABASE_PATH
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def generate_order_number(self):
        """Generate unique order number"""
        timestamp = datetime.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.digits, k=4))
        return f"ORD-{timestamp}-{random_part}"
    
    def create_order(self, customer_id, items, payment_method, subtotal, tax, shipping_cost, 
                     total, shipping_address=None, shipping_city=None, shipping_state=None, 
                     shipping_zip=None, notes=None, created_by=None):
        """Create a new order with items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Generate unique order number
            order_number = self.generate_order_number()
            
            # Create order
            cursor.execute('''
                INSERT INTO orders (customer_id, order_number, payment_method, subtotal, tax, 
                                  shipping_cost, total, shipping_address, shipping_city, 
                                  shipping_state, shipping_zip, notes, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (customer_id, order_number, payment_method, subtotal, tax, shipping_cost, 
                  total, shipping_address, shipping_city, shipping_state, shipping_zip, 
                  notes, created_by))
            
            order_id = cursor.lastrowid
            
            # Create order items and update stock
            for item in items:
                cursor.execute('''
                    INSERT INTO order_items (order_id, product_id, product_name, quantity, 
                                            unit_price, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (order_id, item['product_id'], item['product_name'], item['quantity'], 
                      item['unit_price'], item['subtotal']))
                
                # Update product stock
                cursor.execute('''
                    UPDATE products 
                    SET stock_quantity = stock_quantity - ?
                    WHERE id = ?
                ''', (item['quantity'], item['product_id']))
                
                # Record inventory transaction
                cursor.execute('''
                    INSERT INTO inventory_transactions (product_id, transaction_type, quantity, 
                                                       notes, created_by)
                    VALUES (?, 'Sale', ?, ?, ?)
                ''', (item['product_id'], -item['quantity'], f"Order {order_number}", created_by))
            
            conn.commit()
            conn.close()
            return order_id, order_number
        
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def get_all_orders(self):
        """Get all orders"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.*, c.first_name, c.last_name, c.phone
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.id
            ORDER BY o.order_date DESC
        ''')
        orders = cursor.fetchall()
        conn.close()
        return [dict(order) for order in orders]
    
    def get_order_by_id(self, order_id):
        """Get order by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.*, c.first_name, c.last_name, c.phone, c.email
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.id
            WHERE o.id = ?
        ''', (order_id,))
        order = cursor.fetchone()
        conn.close()
        return dict(order) if order else None
    
    def get_order_items(self, order_id):
        """Get items for an order"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT oi.*, p.sku, p.category
            FROM order_items oi
            LEFT JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        items = cursor.fetchall()
        conn.close()
        return [dict(item) for item in items]
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE orders 
            SET status = ?, updated_at = ?
            WHERE id = ?
        ''', (status, datetime.now(), order_id))
        conn.commit()
        conn.close()
        return True
    
    def get_orders_by_customer(self, customer_id):
        """Get orders for a specific customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM orders
            WHERE customer_id = ?
            ORDER BY order_date DESC
        ''', (customer_id,))
        orders = cursor.fetchall()
        conn.close()
        return [dict(order) for order in orders]
    
    def get_orders_by_status(self, status):
        """Get orders by status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.*, c.first_name, c.last_name
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.id
            WHERE o.status = ?
            ORDER BY o.order_date DESC
        ''', (status,))
        orders = cursor.fetchall()
        conn.close()
        return [dict(order) for order in orders]
    
    def get_recent_orders(self, limit=10):
        """Get recent orders"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.*, c.first_name, c.last_name
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.id
            ORDER BY o.order_date DESC
            LIMIT ?
        ''', (limit,))
        orders = cursor.fetchall()
        conn.close()
        return [dict(order) for order in orders]
    
    def get_order_stats(self):
        """Get order statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total orders
        cursor.execute('SELECT COUNT(*) as total FROM orders')
        total_orders = cursor.fetchone()['total']
        
        # Total revenue
        cursor.execute('SELECT SUM(total) as revenue FROM orders WHERE status != "Cancelled"')
        total_revenue = cursor.fetchone()['revenue'] or 0
        
        # Orders by status
        cursor.execute('''
            SELECT status, COUNT(*) as count 
            FROM orders 
            GROUP BY status
        ''')
        status_counts = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # Average order value
        cursor.execute('''
            SELECT AVG(total) as avg_value 
            FROM orders 
            WHERE status != "Cancelled"
        ''')
        avg_order_value = cursor.fetchone()['avg_value'] or 0
        
        conn.close()
        
        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'status_counts': status_counts,
            'avg_order_value': avg_order_value
        }
    
    def search_orders(self, search_term):
        """Search orders by order number or customer name"""
        conn = self.get_connection()
        cursor = conn.cursor()
        search_pattern = f"%{search_term}%"
        cursor.execute('''
            SELECT o.*, c.first_name, c.last_name
            FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.id
            WHERE o.order_number LIKE ? 
               OR c.first_name LIKE ? 
               OR c.last_name LIKE ?
            ORDER BY o.order_date DESC
        ''', (search_pattern, search_pattern, search_pattern))
        orders = cursor.fetchall()
        conn.close()
        return [dict(order) for order in orders]
