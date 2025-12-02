# API Documentation

## Overview

This document provides complete API reference for the E-Commerce Order Processing System models and controllers.

## Table of Contents

1. [Models API](#models-api)
   - [UserModel](#usermodel)
   - [ProductModel](#productmodel)
   - [OrderModel](#ordermodel)
   - [CustomerModel](#customermodel)
2. [Controllers API](#controllers-api)
   - [AuthController](#authcontroller)
3. [Utilities API](#utilities-api)
   - [Session Management](#session-management)
   - [Formatters](#formatters)

---

## Models API

### UserModel

Location: `models/user.py`

#### `create_user(username, email, password, role='customer')`

Create a new user account.

**Parameters:**

- `username` (str): Unique username
- `email` (str): Unique email address
- `password` (str): Plain text password (will be hashed)
- `role` (str, optional): User role. Default: 'customer'
  - Options: 'admin', 'staff', 'customer'

**Returns:**

- `int`: User ID if successful
- `None`: If username/email already exists

**Example:**

```python
user_model = UserModel()
user_id = user_model.create_user(
    username="john_doe",
    email="john@example.com",
    password="secure123",
    role="customer"
)
```

#### `get_user_by_username(username)`

Retrieve user by username.

**Parameters:**

- `username` (str): Username to search

**Returns:**

- `dict`: User data dictionary
- `None`: If user not found

**Example:**

```python
user = user_model.get_user_by_username("john_doe")
# {
#     'id': 1,
#     'username': 'john_doe',
#     'email': 'john@example.com',
#     'role': 'customer',
#     'created_at': '2025-01-01 00:00:00'
# }
```

#### `get_user_by_id(user_id)`

Retrieve user by ID.

**Parameters:**

- `user_id` (int): User ID

**Returns:**

- `dict`: User data
- `None`: If not found

#### `verify_password(username, password)`

Verify user password.

**Parameters:**

- `username` (str): Username
- `password` (str): Plain text password

**Returns:**

- `bool`: True if password matches, False otherwise

**Example:**

```python
if user_model.verify_password("john_doe", "secure123"):
    print("Password correct")
```

#### `update_last_login(user_id)`

Update user's last login timestamp.

**Parameters:**

- `user_id` (int): User ID

**Returns:**

- `None`

#### `get_all_users()`

Get all users.

**Returns:**

- `list[dict]`: List of user dictionaries (passwords excluded)

---

### ProductModel

Location: `models/product.py`

#### `create_product(name, description, category, price, cost, sku, stock_quantity, reorder_level=10)`

Create a new product.

**Parameters:**

- `name` (str): Product name
- `description` (str): Product description
- `category` (str): Product category
- `price` (float): Selling price
- `cost` (float): Cost price
- `sku` (str): Unique SKU
- `stock_quantity` (int): Initial stock
- `reorder_level` (int, optional): Reorder threshold. Default: 10

**Returns:**

- `int`: Product ID
- `None`: If SKU already exists

**Example:**

```python
product_model = ProductModel()
product_id = product_model.create_product(
    name="Wireless Mouse",
    description="Ergonomic wireless mouse",
    category="Electronics",
    price=29.99,
    cost=12.00,
    sku="MOU-001",
    stock_quantity=100,
    reorder_level=20
)
```

#### `get_all_products(active_only=True)`

Get all products.

**Parameters:**

- `active_only` (bool, optional): Only active products. Default: True

**Returns:**

- `list[dict]`: List of product dictionaries

#### `get_product_by_id(product_id)`

Get product by ID.

**Parameters:**

- `product_id` (int): Product ID

**Returns:**

- `dict`: Product data
- `None`: If not found

#### `get_product_by_sku(sku)`

Get product by SKU.

**Parameters:**

- `sku` (str): Product SKU

**Returns:**

- `dict`: Product data
- `None`: If not found

#### `update_product(product_id, **kwargs)`

Update product details.

**Parameters:**

- `product_id` (int): Product ID
- `**kwargs`: Fields to update
  - Allowed: name, description, category, price, cost, sku, stock_quantity, reorder_level, is_active

**Returns:**

- `bool`: True if successful

**Example:**

```python
product_model.update_product(
    1,
    price=24.99,
    stock_quantity=150
)
```

#### `delete_product(product_id)`

Soft delete product (sets is_active=0).

**Parameters:**

- `product_id` (int): Product ID

**Returns:**

- `bool`: True if successful

#### `update_stock(product_id, quantity_change)`

Update product stock quantity.

**Parameters:**

- `product_id` (int): Product ID
- `quantity_change` (int): Positive or negative change

**Returns:**

- `bool`: True if successful

**Example:**

```python
# Add 50 units
product_model.update_stock(1, 50)

# Remove 10 units
product_model.update_stock(1, -10)
```

#### `get_low_stock_products()`

Get products below reorder level.

**Returns:**

- `list[dict]`: List of low stock products

#### `search_products(search_term)`

Search products by name, description, or SKU.

**Parameters:**

- `search_term` (str): Search query

**Returns:**

- `list[dict]`: Matching products

#### `get_products_by_category(category)`

Get products by category.

**Parameters:**

- `category` (str): Category name

**Returns:**

- `list[dict]`: Products in category

#### `get_categories()`

Get all product categories.

**Returns:**

- `list[str]`: List of category names

---

### OrderModel

Location: `models/order.py`

#### `create_order(customer_id, items, payment_method, subtotal, tax, shipping_cost, total, **kwargs)`

Create a new order.

**Parameters:**

- `customer_id` (int): Customer ID
- `items` (list[dict]): Order items
  ```python
  [
      {
          'product_id': 1,
          'product_name': 'Mouse',
          'quantity': 2,
          'unit_price': 29.99,
          'subtotal': 59.98
      }
  ]
  ```
- `payment_method` (str): Payment method
- `subtotal` (float): Order subtotal
- `tax` (float): Tax amount
- `shipping_cost` (float): Shipping cost
- `total` (float): Total amount
- `**kwargs`: Optional parameters
  - `shipping_address` (str)
  - `shipping_city` (str)
  - `shipping_state` (str)
  - `shipping_zip` (str)
  - `notes` (str)
  - `created_by` (int): User ID

**Returns:**

- `tuple`: (order_id, order_number)

**Raises:**

- `Exception`: If order creation fails

**Example:**

```python
order_model = OrderModel()
items = [
    {
        'product_id': 1,
        'product_name': 'Mouse',
        'quantity': 1,
        'unit_price': 29.99,
        'subtotal': 29.99
    }
]

order_id, order_number = order_model.create_order(
    customer_id=1,
    items=items,
    payment_method="Credit Card",
    subtotal=29.99,
    tax=2.40,
    shipping_cost=10.00,
    total=42.39,
    shipping_address="123 Main St",
    shipping_city="New York",
    shipping_state="NY",
    shipping_zip="10001",
    created_by=1
)
```

#### `get_all_orders()`

Get all orders with customer information.

**Returns:**

- `list[dict]`: List of orders

#### `get_order_by_id(order_id)`

Get order by ID with customer details.

**Parameters:**

- `order_id` (int): Order ID

**Returns:**

- `dict`: Order data
- `None`: If not found

#### `get_order_items(order_id)`

Get items for an order.

**Parameters:**

- `order_id` (int): Order ID

**Returns:**

- `list[dict]`: Order items

#### `update_order_status(order_id, status)`

Update order status.

**Parameters:**

- `order_id` (int): Order ID
- `status` (str): New status
  - Options: 'Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Refunded'

**Returns:**

- `bool`: True if successful

**Example:**

```python
order_model.update_order_status(1, 'Shipped')
```

#### `get_orders_by_customer(customer_id)`

Get orders for specific customer.

**Parameters:**

- `customer_id` (int): Customer ID

**Returns:**

- `list[dict]`: Customer's orders

#### `get_orders_by_status(status)`

Get orders by status.

**Parameters:**

- `status` (str): Order status

**Returns:**

- `list[dict]`: Orders with status

#### `get_recent_orders(limit=10)`

Get recent orders.

**Parameters:**

- `limit` (int, optional): Number of orders. Default: 10

**Returns:**

- `list[dict]`: Recent orders

#### `get_order_stats()`

Get order statistics.

**Returns:**

- `dict`: Statistics
  ```python
  {
      'total_orders': 100,
      'total_revenue': 5000.00,
      'status_counts': {'Pending': 10, 'Delivered': 80, ...},
      'avg_order_value': 50.00
  }
  ```

#### `search_orders(search_term)`

Search orders by number or customer name.

**Parameters:**

- `search_term` (str): Search query

**Returns:**

- `list[dict]`: Matching orders

---

### CustomerModel

Location: `models/customer.py`

#### `create_customer(first_name, last_name, phone, email=None, address=None, city=None, state=None, zip_code=None, user_id=None)`

Create a new customer.

**Parameters:**

- `first_name` (str): First name
- `last_name` (str): Last name
- `phone` (str): Phone number
- `email` (str, optional): Email address
- `address` (str, optional): Street address
- `city` (str, optional): City
- `state` (str, optional): State
- `zip_code` (str, optional): ZIP code
- `user_id` (int, optional): Associated user ID

**Returns:**

- `int`: Customer ID

**Example:**

```python
customer_model = CustomerModel()
customer_id = customer_model.create_customer(
    first_name="John",
    last_name="Doe",
    phone="555-0123",
    email="john@example.com",
    address="123 Main St",
    city="New York",
    state="NY",
    zip_code="10001"
)
```

#### `get_all_customers()`

Get all customers with email.

**Returns:**

- `list[dict]`: List of customers

#### `get_customer_by_id(customer_id)`

Get customer by ID.

**Parameters:**

- `customer_id` (int): Customer ID

**Returns:**

- `dict`: Customer data
- `None`: If not found

#### `get_customer_by_user_id(user_id)`

Get customer by user ID.

**Parameters:**

- `user_id` (int): User ID

**Returns:**

- `dict`: Customer data
- `None`: If not found

#### `update_customer(customer_id, **kwargs)`

Update customer details.

**Parameters:**

- `customer_id` (int): Customer ID
- `**kwargs`: Fields to update

**Returns:**

- `bool`: True if successful

#### `delete_customer(customer_id)`

Delete customer.

**Parameters:**

- `customer_id` (int): Customer ID

**Returns:**

- `bool`: True if successful

#### `search_customers(search_term)`

Search customers by name, phone, or email.

**Parameters:**

- `search_term` (str): Search query

**Returns:**

- `list[dict]`: Matching customers

#### `get_customer_stats(customer_id)`

Get customer statistics.

**Parameters:**

- `customer_id` (int): Customer ID

**Returns:**

- `dict`: Statistics
  ```python
  {
      'total_orders': 5,
      'total_spent': 250.00,
      'avg_order_value': 50.00,
      'last_order': '2025-01-01'
  }
  ```

#### `get_top_customers(limit=10)`

Get top customers by spending.

**Parameters:**

- `limit` (int, optional): Number of customers. Default: 10

**Returns:**

- `list[dict]`: Top customers with order count and total spent

---

## Controllers API

### AuthController

Location: `controllers/auth.py`

#### `login(username, password)`

Authenticate user and create session.

**Parameters:**

- `username` (str): Username
- `password` (str): Password

**Returns:**

- `bool`: True if login successful

**Side Effects:**

- Sets session state variables:
  - `logged_in`
  - `user_id`
  - `username`
  - `email`
  - `role`
  - `customer_id` (if customer)

**Example:**

```python
auth = AuthController()
if auth.login("admin", "admin123"):
    print("Login successful")
```

#### `register(username, email, password, role='customer')`

Register new user.

**Parameters:**

- `username` (str): Unique username
- `email` (str): Unique email
- `password` (str): Password
- `role` (str, optional): User role. Default: 'customer'

**Returns:**

- `bool`: True if registration successful

**Example:**

```python
if auth.register("newuser", "user@example.com", "pass123"):
    print("Registration successful")
```

#### `logout()`

Logout user and clear session.

**Returns:**

- `None`

**Side Effects:**

- Clears all session state variables

#### `is_admin()`

Check if current user is admin.

**Returns:**

- `bool`: True if admin

#### `is_staff()`

Check if current user is staff or admin.

**Returns:**

- `bool`: True if staff/admin

#### `is_customer()`

Check if current user is customer.

**Returns:**

- `bool`: True if customer

---

## Utilities API

### Session Management

Location: `utils/session.py`

#### `init_session_state()`

Initialize all session state variables.

**Returns:**

- `None`

**Side Effects:**

- Creates session variables if not exist

#### `add_to_cart(product_id, product_name, price, quantity=1)`

Add item to shopping cart.

**Parameters:**

- `product_id` (int): Product ID
- `product_name` (str): Product name
- `price` (float): Unit price
- `quantity` (int, optional): Quantity. Default: 1

**Returns:**

- `None`

**Example:**

```python
add_to_cart(1, "Mouse", 29.99, 2)
```

#### `remove_from_cart(product_id)`

Remove item from cart.

**Parameters:**

- `product_id` (int): Product ID

**Returns:**

- `None`

#### `update_cart_quantity(product_id, quantity)`

Update item quantity in cart.

**Parameters:**

- `product_id` (int): Product ID
- `quantity` (int): New quantity

**Returns:**

- `None`

#### `clear_cart()`

Clear all items from cart.

**Returns:**

- `None`

#### `get_cart_total()`

Calculate cart total.

**Returns:**

- `float`: Total amount

#### `get_cart_count()`

Get total items in cart.

**Returns:**

- `int`: Total quantity

---

### Formatters

Location: `utils/formatters.py`

#### `format_currency(amount)`

Format number as currency.

**Parameters:**

- `amount` (float): Amount to format

**Returns:**

- `str`: Formatted currency (e.g., "$29.99")

**Example:**

```python
formatted = format_currency(29.99)  # "$29.99"
```

#### `format_date(date_str)`

Format date string.

**Parameters:**

- `date_str` (str|datetime): Date to format

**Returns:**

- `str`: Formatted date (e.g., "January 15, 2025")

#### `format_datetime(date_str)`

Format datetime string.

**Parameters:**

- `date_str` (str|datetime): Datetime to format

**Returns:**

- `str`: Formatted datetime (e.g., "January 15, 2025 03:45 PM")

#### `format_phone(phone)`

Format phone number.

**Parameters:**

- `phone` (str): Phone number

**Returns:**

- `str`: Formatted phone (e.g., "(555) 123-4567")

#### `get_status_color(status)`

Get color for order status.

**Parameters:**

- `status` (str): Order status

**Returns:**

- `str`: Color name

#### `calculate_tax(subtotal, tax_rate=None)`

Calculate tax amount.

**Parameters:**

- `subtotal` (float): Subtotal amount
- `tax_rate` (float, optional): Tax rate. Default: from config

**Returns:**

- `float`: Tax amount

#### `calculate_shipping(subtotal, shipping_cost=None, free_threshold=None)`

Calculate shipping cost.

**Parameters:**

- `subtotal` (float): Order subtotal
- `shipping_cost` (float, optional): Shipping cost. Default: from config
- `free_threshold` (float, optional): Free shipping threshold. Default: from config

**Returns:**

- `float`: Shipping cost (0 if over threshold)

#### `truncate_text(text, max_length=50)`

Truncate text to max length.

**Parameters:**

- `text` (str): Text to truncate
- `max_length` (int, optional): Max length. Default: 50

**Returns:**

- `str`: Truncated text with "..." if needed

---

## Configuration Constants

Location: `config/config.py`

### APP_CONFIG

```python
{
    'app_name': 'E-Commerce Order Processing System',
    'version': '1.0.0',
    'currency': 'USD',
    'currency_symbol': '$',
    'tax_rate': 0.08,
    'shipping_cost': 10.00,
    'free_shipping_threshold': 100.00
}
```

### ORDER_STATUS

```python
['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Refunded']
```

### PAYMENT_METHODS

```python
['Credit Card', 'Debit Card', 'PayPal', 'Cash on Delivery', 'Bank Transfer']
```

### PRODUCT_CATEGORIES

```python
['Electronics', 'Clothing', 'Home & Garden', 'Sports & Outdoors',
 'Books', 'Toys & Games', 'Health & Beauty', 'Food & Beverages',
 'Automotive', 'Other']
```

---

**API Documentation Version:** 1.0.0  
**Last Updated:** 2025-12-02
