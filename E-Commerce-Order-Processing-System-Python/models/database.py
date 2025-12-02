"""
Database Connection and Initialization
"""

import sqlite3
from pathlib import Path
import bcrypt
from datetime import datetime

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        return self.connection
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def init_tables(self):
        """Initialize all database tables"""
        
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'customer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Customers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zip_code TEXT,
                country TEXT DEFAULT 'USA',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Products table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                price REAL NOT NULL,
                cost REAL,
                sku TEXT UNIQUE,
                stock_quantity INTEGER DEFAULT 0,
                reorder_level INTEGER DEFAULT 10,
                image_url TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Orders table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                order_number TEXT UNIQUE NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Pending',
                payment_method TEXT,
                subtotal REAL NOT NULL,
                tax REAL DEFAULT 0,
                shipping_cost REAL DEFAULT 0,
                total REAL NOT NULL,
                shipping_address TEXT,
                shipping_city TEXT,
                shipping_state TEXT,
                shipping_zip TEXT,
                notes TEXT,
                created_by INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        ''')
        
        # Order items table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        # Inventory transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                notes TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        ''')
        
        self.connection.commit()
    
    def create_default_users(self):
        """Create default admin and demo users"""
        users = [
            ('admin', 'admin@ecommerce.com', 'admin123', 'admin'),
            ('staff', 'staff@ecommerce.com', 'staff123', 'staff'),
            ('customer', 'customer@ecommerce.com', 'customer123', 'customer')
        ]
        
        for username, email, password, role in users:
            # Check if user already exists
            self.cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if self.cursor.fetchone() is None:
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                self.cursor.execute('''
                    INSERT INTO users (username, email, password_hash, role)
                    VALUES (?, ?, ?, ?)
                ''', (username, email, password_hash, role))
        
        self.connection.commit()
    
    def create_sample_products(self):
        """Create sample products"""
        products = [
            ('Laptop Pro 15"', 'High-performance laptop with 16GB RAM and 512GB SSD', 'Electronics', 1299.99, 899.00, 'LAP-001', 25),
            ('Wireless Mouse', 'Ergonomic wireless mouse with 2.4GHz connection', 'Electronics', 29.99, 12.00, 'MOU-001', 150),
            ('Mechanical Keyboard', 'RGB mechanical keyboard with blue switches', 'Electronics', 89.99, 45.00, 'KEY-001', 80),
            ('USB-C Hub', '7-in-1 USB-C hub with HDMI and SD card reader', 'Electronics', 49.99, 20.00, 'HUB-001', 120),
            ('Desk Chair', 'Ergonomic office chair with lumbar support', 'Home & Garden', 249.99, 120.00, 'CHA-001', 40),
            ('Standing Desk', 'Adjustable height standing desk', 'Home & Garden', 399.99, 200.00, 'DSK-001', 25),
            ('Monitor 27"', '27-inch 4K monitor with HDR support', 'Electronics', 449.99, 280.00, 'MON-001', 35),
            ('Webcam HD', '1080p webcam with auto-focus', 'Electronics', 79.99, 35.00, 'WEB-001', 90),
            ('Headphones Pro', 'Noise-canceling wireless headphones', 'Electronics', 199.99, 95.00, 'HEA-001', 60),
            ('Desk Lamp', 'LED desk lamp with adjustable brightness', 'Home & Garden', 39.99, 15.00, 'LAM-001', 100),
            ('Cable Organizer', 'Desktop cable management system', 'Electronics', 19.99, 5.00, 'CAB-001', 200),
            ('Monitor Arm', 'Adjustable monitor arm mount', 'Electronics', 89.99, 40.00, 'ARM-001', 50),
            ('Laptop Stand', 'Aluminum laptop stand with cooling', 'Electronics', 49.99, 20.00, 'STA-001', 75),
            ('External SSD 1TB', 'Portable SSD with USB 3.1', 'Electronics', 129.99, 70.00, 'SSD-001', 85),
            ('Bluetooth Speaker', 'Portable waterproof Bluetooth speaker', 'Electronics', 59.99, 25.00, 'SPK-001', 110),
            ('Desk Organizer', 'Wooden desk organizer with multiple compartments', 'Home & Garden', 34.99, 12.00, 'ORG-001', 95),
            ('Phone Stand', 'Adjustable phone and tablet stand', 'Electronics', 24.99, 8.00, 'PHN-001', 140),
            ('Power Strip', '6-outlet surge protector power strip', 'Electronics', 29.99, 10.00, 'POW-001', 130),
            ('Mouse Pad XL', 'Extended gaming mouse pad', 'Electronics', 19.99, 6.00, 'PAD-001', 180),
            ('Office Plant', 'Artificial succulent plant for desk', 'Home & Garden', 14.99, 4.00, 'PLT-001', 160),
        ]
        
        for name, desc, category, price, cost, sku, stock in products:
            self.cursor.execute('SELECT id FROM products WHERE sku = ?', (sku,))
            if self.cursor.fetchone() is None:
                self.cursor.execute('''
                    INSERT INTO products (name, description, category, price, cost, sku, stock_quantity)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (name, desc, category, price, cost, sku, stock))
        
        self.connection.commit()
    
    def create_sample_customers(self):
        """Create sample customers"""
        customers = [
            (None, 'John', 'Doe', '555-0101', '123 Main St', 'New York', 'NY', '10001'),
            (None, 'Jane', 'Smith', '555-0102', '456 Oak Ave', 'Los Angeles', 'CA', '90001'),
            (None, 'Bob', 'Johnson', '555-0103', '789 Pine Rd', 'Chicago', 'IL', '60601'),
            (None, 'Alice', 'Williams', '555-0104', '321 Elm St', 'Houston', 'TX', '77001'),
            (None, 'Charlie', 'Brown', '555-0105', '654 Maple Dr', 'Phoenix', 'AZ', '85001'),
        ]
        
        for user_id, first, last, phone, address, city, state, zip_code in customers:
            self.cursor.execute('''
                SELECT id FROM customers WHERE first_name = ? AND last_name = ?
            ''', (first, last))
            if self.cursor.fetchone() is None:
                self.cursor.execute('''
                    INSERT INTO customers (user_id, first_name, last_name, phone, address, city, state, zip_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, first, last, phone, address, city, state, zip_code))
        
        self.connection.commit()
    
    def initialize_database(self):
        """Initialize database with tables and sample data"""
        self.connect()
        self.init_tables()
        self.create_default_users()
        self.create_sample_products()
        self.create_sample_customers()
        print("Database initialized successfully!")

# Initialize database on import
from config.config import DATABASE_PATH
db = Database(DATABASE_PATH)
db.initialize_database()
