"""
Customer Model - Handles customer data operations
"""

import sqlite3
from datetime import datetime
from config.config import DATABASE_PATH

class CustomerModel:
    def __init__(self):
        self.db_path = DATABASE_PATH
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_customer(self, first_name, last_name, phone, email=None, address=None, 
                       city=None, state=None, zip_code=None, user_id=None):
        """Create a new customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO customers (user_id, first_name, last_name, phone, address, 
                                      city, state, zip_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, first_name, last_name, phone, address, city, state, zip_code))
            conn.commit()
            customer_id = cursor.lastrowid
            conn.close()
            return customer_id
        except Exception as e:
            conn.close()
            raise e
    
    def get_all_customers(self):
        """Get all customers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, u.email 
            FROM customers c
            LEFT JOIN users u ON c.user_id = u.id
            ORDER BY c.last_name, c.first_name
        ''')
        customers = cursor.fetchall()
        conn.close()
        return [dict(customer) for customer in customers]
    
    def get_customer_by_id(self, customer_id):
        """Get customer by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, u.email 
            FROM customers c
            LEFT JOIN users u ON c.user_id = u.id
            WHERE c.id = ?
        ''', (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        return dict(customer) if customer else None
    
    def get_customer_by_user_id(self, user_id):
        """Get customer by user ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, u.email 
            FROM customers c
            LEFT JOIN users u ON c.user_id = u.id
            WHERE c.user_id = ?
        ''', (user_id,))
        customer = cursor.fetchone()
        conn.close()
        return dict(customer) if customer else None
    
    def update_customer(self, customer_id, **kwargs):
        """Update customer details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        allowed_fields = ['first_name', 'last_name', 'phone', 'address', 
                         'city', 'state', 'zip_code']
        
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if updates:
            values.append(customer_id)
            query = f"UPDATE customers SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return True
    
    def delete_customer(self, customer_id):
        """Delete customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        conn.commit()
        conn.close()
        return True
    
    def search_customers(self, search_term):
        """Search customers by name, phone, or email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        search_pattern = f"%{search_term}%"
        cursor.execute('''
            SELECT c.*, u.email 
            FROM customers c
            LEFT JOIN users u ON c.user_id = u.id
            WHERE c.first_name LIKE ? 
               OR c.last_name LIKE ? 
               OR c.phone LIKE ?
               OR u.email LIKE ?
            ORDER BY c.last_name, c.first_name
        ''', (search_pattern, search_pattern, search_pattern, search_pattern))
        customers = cursor.fetchall()
        conn.close()
        return [dict(customer) for customer in customers]
    
    def get_customer_stats(self, customer_id):
        """Get statistics for a customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total orders
        cursor.execute('''
            SELECT COUNT(*) as total 
            FROM orders 
            WHERE customer_id = ?
        ''', (customer_id,))
        total_orders = cursor.fetchone()['total']
        
        # Total spent
        cursor.execute('''
            SELECT SUM(total) as spent 
            FROM orders 
            WHERE customer_id = ? AND status != "Cancelled"
        ''', (customer_id,))
        total_spent = cursor.fetchone()['spent'] or 0
        
        # Average order value
        cursor.execute('''
            SELECT AVG(total) as avg_value 
            FROM orders 
            WHERE customer_id = ? AND status != "Cancelled"
        ''', (customer_id,))
        avg_order_value = cursor.fetchone()['avg_value'] or 0
        
        # Last order date
        cursor.execute('''
            SELECT MAX(order_date) as last_order 
            FROM orders 
            WHERE customer_id = ?
        ''', (customer_id,))
        last_order = cursor.fetchone()['last_order']
        
        conn.close()
        
        return {
            'total_orders': total_orders,
            'total_spent': total_spent,
            'avg_order_value': avg_order_value,
            'last_order': last_order
        }
    
    def get_top_customers(self, limit=10):
        """Get top customers by total spending"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, u.email,
                   COUNT(o.id) as order_count,
                   SUM(o.total) as total_spent
            FROM customers c
            LEFT JOIN users u ON c.user_id = u.id
            LEFT JOIN orders o ON c.id = o.customer_id AND o.status != "Cancelled"
            GROUP BY c.id
            ORDER BY total_spent DESC
            LIMIT ?
        ''', (limit,))
        customers = cursor.fetchall()
        conn.close()
        return [dict(customer) for customer in customers]
