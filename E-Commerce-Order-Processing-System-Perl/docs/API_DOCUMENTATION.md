# API Documentation

## E-Commerce Order Processing System - Perl

Complete API reference for all models and controllers.

## Models API

### ECommerce::Models::User

#### new()

```perl
my $user_model = ECommerce::Models::User->new();
```

Creates new User model instance.

#### create_user($username, $email, $password, $role)

```perl
my $result = $user_model->create_user('john', 'john@example.com', 'password123', 'customer');
# Returns: {success => 1, user_id => 4} or {success => 0, message => 'error'}
```

#### get_user_by_username($username)

```perl
my $user = $user_model->get_user_by_username('john');
# Returns: hashref with user data or undef
```

#### get_user_by_id($user_id)

```perl
my $user = $user_model->get_user_by_id(1);
```

#### verify_password($username, $password)

```perl
my $valid = $user_model->verify_password('john', 'password123');
# Returns: 1 (valid) or 0 (invalid)
```

#### update_last_login($user_id)

```perl
$user_model->update_last_login(1);
```

#### get_all_users()

```perl
my $users = $user_model->get_all_users();
# Returns: arrayref of hashrefs
```

#### update_user_role($user_id, $new_role)

```perl
$user_model->update_user_role(1, 'admin');
```

---

### ECommerce::Models::Product

#### new()

```perl
my $product_model = ECommerce::Models::Product->new();
```

#### create_product(%params)

```perl
my $result = $product_model->create_product(
    name => 'Laptop',
    description => 'High-performance laptop',
    sku => 'LAP001',
    category => 'Electronics',
    price => 999.99,
    cost => 600.00,
    stock_quantity => 50,
    reorder_level => 10
);
```

#### get_all_products($active_only)

```perl
my $products = $product_model->get_all_products(1);  # Active only
my $all = $product_model->get_all_products(0);        # Including inactive
```

#### get_product_by_id($product_id)

```perl
my $product = $product_model->get_product_by_id(1);
```

#### get_product_by_sku($sku)

```perl
my $product = $product_model->get_product_by_sku('LAP001');
```

#### update_product($product_id, %params)

```perl
$product_model->update_product(1, price => 899.99, stock_quantity => 45);
```

#### delete_product($product_id)

```perl
$product_model->delete_product(1);  # Soft delete (sets is_active = 0)
```

#### update_stock($product_id, $quantity_change, $transaction_type, $reference_id, $notes)

```perl
$product_model->update_stock(1, -5, 'sale', $order_id, 'Order #12345');
```

#### get_low_stock_products()

```perl
my $low_stock = $product_model->get_low_stock_products();
```

#### search_products($search_term)

```perl
my $results = $product_model->search_products('laptop');
```

#### get_products_by_category($category)

```perl
my $electronics = $product_model->get_products_by_category('Electronics');
```

#### get_categories()

```perl
my $categories = $product_model->get_categories();
# Returns: arrayref of category names
```

---

### ECommerce::Models::Order

#### new()

```perl
my $order_model = ECommerce::Models::Order->new();
```

#### generate_order_number()

```perl
my $order_number = $order_model->generate_order_number();
# Returns: 'ORD-20251202-12345'
```

#### create_order(%params)

```perl
my $result = $order_model->create_order(
    customer_id => 1,
    subtotal => 100.00,
    tax => 8.00,
    shipping => 5.00,
    total => 113.00,
    payment_method => 'credit_card',
    shipping_address => '123 Main St, City, State 12345',
    items => [
        {
            product_id => 1,
            product_name => 'Laptop',
            product_sku => 'LAP001',
            quantity => 1,
            unit_price => 100.00,
            subtotal => 100.00
        }
    ]
);
```

#### create_order_from_cart($customer_id, $cart, $params)

```perl
my $cart = [
    {product_id => 1, quantity => 2},
    {product_id => 2, quantity => 1}
];

my $result = $order_model->create_order_from_cart(1, $cart, {
    payment_method => 'credit_card',
    shipping_address => '123 Main St'
});
```

#### get_all_orders()

```perl
my $orders = $order_model->get_all_orders();
```

#### get_order_by_id($order_id)

```perl
my $order = $order_model->get_order_by_id(1);
```

#### get_order_items($order_id)

```perl
my $items = $order_model->get_order_items(1);
```

#### update_order_status($order_id, $status)

```perl
$order_model->update_order_status(1, 'shipped');
```

#### get_orders_by_customer($customer_id)

```perl
my $orders = $order_model->get_orders_by_customer(1);
```

#### get_orders_by_status($status)

```perl
my $pending = $order_model->get_orders_by_status('pending');
```

#### get_recent_orders($limit)

```perl
my $recent = $order_model->get_recent_orders(10);
```

#### get_order_stats()

```perl
my $stats = $order_model->get_order_stats();
# Returns: {
#   total_revenue => 5000.00,
#   total_orders => 50,
#   average_order_value => 100.00,
#   by_status => {...}
# }
```

#### search_orders($search_term)

```perl
my $results = $order_model->search_orders('ORD-20251202');
```

---

### ECommerce::Models::Customer

#### new()

```perl
my $customer_model = ECommerce::Models::Customer->new();
```

#### create_customer(%params)

```perl
my $result = $customer_model->create_customer(
    user_id => 3,
    first_name => 'John',
    last_name => 'Doe',
    phone => '555-0101',
    address => '123 Main St',
    city => 'New York',
    state => 'NY',
    zip_code => '10001',
    country => 'USA'
);
```

#### get_all_customers()

```perl
my $customers = $customer_model->get_all_customers();
```

#### get_customer_by_id($customer_id)

```perl
my $customer = $customer_model->get_customer_by_id(1);
```

#### get_customer_by_user_id($user_id)

```perl
my $customer = $customer_model->get_customer_by_user_id(3);
```

#### update_customer($customer_id, %params)

```perl
$customer_model->update_customer(1, phone => '555-9999', city => 'Boston');
```

#### delete_customer($customer_id)

```perl
$customer_model->delete_customer(1);
```

#### search_customers($search_term)

```perl
my $results = $customer_model->search_customers('John');
```

#### get_customer_stats($customer_id)

```perl
my $stats = $customer_model->get_customer_stats(1);
# Returns: {
#   total_orders => 5,
#   total_spent => 500.00,
#   average_order_value => 100.00,
#   last_order_date => '2025-12-01 10:30:00'
# }
```

#### get_top_customers($limit)

```perl
my $top = $customer_model->get_top_customers(10);
```

---

## Controllers API

### ECommerce::Controllers::Auth

#### new()

```perl
my $auth = ECommerce::Controllers::Auth->new();
```

#### login($username, $password)

```perl
my $user = $auth->login('admin', 'admin123');
# Returns: {
#   id => 1,
#   username => 'admin',
#   email => 'admin@example.com',
#   role => 'admin',
#   customer_id => undef
# } or undef if invalid
```

#### register($username, $email, $password, $role)

```perl
my $result = $auth->register('newuser', 'new@example.com', 'password123', 'customer');
# Returns: {success => 1, user_id => 4} or {success => 0, message => 'error'}
```

#### is_admin($role)

```perl
my $is_admin = $auth->is_admin('admin');  # Returns: 1
```

#### is_staff($role)

```perl
my $is_staff = $auth->is_staff('staff');  # Returns: 1
my $is_staff = $auth->is_staff('admin');  # Returns: 1 (admin is also staff)
```

#### is_customer($role)

```perl
my $is_customer = $auth->is_customer('customer');  # Returns: 1
```

---

## Configuration (ECommerce::Config)

### Constants

```perl
use ECommerce::Config;

# Database path
my $db_path = $ECommerce::Config::DB_PATH;

# Application config
my $app_name = $ECommerce::Config::APP_CONFIG{app_name};
my $tax_rate = $ECommerce::Config::APP_CONFIG{tax_rate};  # 0.08
my $shipping = $ECommerce::Config::APP_CONFIG{shipping_rate};  # 5.00
my $free_threshold = $ECommerce::Config::APP_CONFIG{free_shipping_threshold};  # 100.00

# Order statuses
my @statuses = @ECommerce::Config::ORDER_STATUS;
# ('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded')

# Payment methods
my @payments = @ECommerce::Config::PAYMENT_METHODS;
# ('credit_card', 'debit_card', 'paypal', 'cash_on_delivery', 'bank_transfer')

# Product categories
my @categories = @ECommerce::Config::PRODUCT_CATEGORIES;
# ('Electronics', 'Clothing', 'Books', ...)

# User roles
my @roles = @ECommerce::Config::USER_ROLES;
# ('admin', 'staff', 'customer')

# Colors
my $primary = $ECommerce::Config::COLORS{primary};    # #2E86AB
my $success = $ECommerce::Config::COLORS{success};    # #06A77D
my $danger = $ECommerce::Config::COLORS{danger};      # #C73E1D
```

---

## Mojolicious Helpers

### is_logged_in()

```perl
if ($c->is_logged_in()) {
    # User is authenticated
}
```

### current_user()

```perl
my $user = $c->current_user();
# Returns: {id, username, email, role, customer_id}
```

### has_role($role)

```perl
if ($c->has_role('admin')) {
    # User is admin
}
```

### get_cart()

```perl
my $cart = $c->get_cart();
# Returns: arrayref of cart items
```

### add_to_cart($item)

```perl
$c->add_to_cart({
    product_id => 1,
    name => 'Laptop',
    price => 999.99,
    quantity => 1
});
```

### clear_cart()

```perl
$c->clear_cart();
```

---

## Error Handling

All methods return structured responses:

### Success Response

```perl
{
    success => 1,
    data_field => $value
}
```

### Error Response

```perl
{
    success => 0,
    message => 'Error description'
}
```

---

## Usage Examples

### Complete Order Flow

```perl
# 1. Get product
my $product_model = ECommerce::Models::Product->new();
my $product = $product_model->get_product_by_id(1);

# 2. Create cart
my $cart = [{
    product_id => $product->{id},
    quantity => 2
}];

# 3. Create order
my $order_model = ECommerce::Models::Order->new();
my $result = $order_model->create_order_from_cart(1, $cart, {
    payment_method => 'credit_card',
    shipping_address => '123 Main St'
});

# 4. Check result
if ($result->{success}) {
    print "Order created: " . $result->{order_number};
} else {
    print "Error: " . $result->{message};
}
```

### User Registration and Login

```perl
use ECommerce::Controllers::Auth;

my $auth = ECommerce::Controllers::Auth->new();

# Register
my $reg_result = $auth->register('john', 'john@example.com', 'password123', 'customer');

if ($reg_result->{success}) {
    # Login
    my $user = $auth->login('john', 'password123');

    if ($user) {
        print "Logged in as: " . $user->{username};
    }
}
```

---

**API Version**: 1.0.0  
**Last Updated**: December 2, 2025
