#!/usr/bin/env perl

# E-Commerce Order Processing System
# Main Application Entry Point
# Built with Mojolicious Framework

use strict;
use warnings;
use utf8;
use FindBin;
use lib "$FindBin::Bin/lib";

use Mojolicious::Lite -signatures;
use ECommerce::Database;
use ECommerce::Config;
use Mojo::JSON qw(decode_json encode_json);

# Initialize database
my $db = ECommerce::Database->new();
$db->initialize_database();

# Enable sessions
app->secrets(['e-commerce-secret-key-change-in-production']);
app->sessions->default_expiration(3600); # 1 hour

# Helper to check if user is logged in
helper is_logged_in => sub {
    my $c = shift;
    return $c->session('user_id') ? 1 : 0;
};

# Helper to get current user
helper current_user => sub {
    my $c = shift;
    return {
        id => $c->session('user_id'),
        username => $c->session('username'),
        email => $c->session('email'),
        role => $c->session('role'),
        customer_id => $c->session('customer_id')
    };
};

# Helper to check role
helper has_role => sub {
    my ($c, $role) = @_;
    return ($c->session('role') // '') eq $role;
};

# Helper to get cart
helper get_cart => sub {
    my $c = shift;
    return $c->session('cart') // [];
};

# Helper to add to cart
helper add_to_cart => sub {
    my ($c, $item) = @_;
    my $cart = $c->session('cart') // [];
    push @$cart, $item;
    $c->session(cart => $cart);
};

# Helper to clear cart
helper clear_cart => sub {
    my $c = shift;
    $c->session(cart => []);
};

# Routes

# Home / Login page
get '/' => sub ($c) {
    if ($c->is_logged_in) {
        return $c->redirect_to('/dashboard');
    }
    $c->render(template => 'login');
};

# Login POST
post '/login' => sub ($c) {
    my $username = $c->param('username');
    my $password = $c->param('password');
    
    use ECommerce::Controllers::Auth;
    my $auth = ECommerce::Controllers::Auth->new();
    my $user = $auth->login($username, $password);
    
    if ($user) {
        $c->session(user_id => $user->{id});
        $c->session(username => $user->{username});
        $c->session(email => $user->{email});
        $c->session(role => $user->{role});
        $c->session(customer_id => $user->{customer_id}) if $user->{customer_id};
        $c->flash(success => 'Login successful!');
        return $c->redirect_to('/dashboard');
    } else {
        $c->flash(error => 'Invalid username or password');
        return $c->redirect_to('/');
    }
};

# Logout
get '/logout' => sub ($c) {
    $c->session(expires => 1);
    $c->flash(success => 'Logged out successfully');
    $c->redirect_to('/');
};

# Register page
get '/register' => sub ($c) {
    $c->render(template => 'register');
};

# Register POST
post '/register' => sub ($c) {
    my $username = $c->param('username');
    my $email = $c->param('email');
    my $password = $c->param('password');
    my $confirm_password = $c->param('confirm_password');
    
    if ($password ne $confirm_password) {
        $c->flash(error => 'Passwords do not match');
        return $c->redirect_to('/register');
    }
    
    use ECommerce::Controllers::Auth;
    my $auth = ECommerce::Controllers::Auth->new();
    my $result = $auth->register($username, $email, $password, 'customer');
    
    if ($result->{success}) {
        $c->flash(success => 'Registration successful! Please login.');
        return $c->redirect_to('/');
    } else {
        $c->flash(error => $result->{message});
        return $c->redirect_to('/register');
    }
};

# Dashboard
get '/dashboard' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    use ECommerce::Models::Product;
    use ECommerce::Models::Order;
    use ECommerce::Models::Customer;
    
    my $product_model = ECommerce::Models::Product->new();
    my $order_model = ECommerce::Models::Order->new();
    my $customer_model = ECommerce::Models::Customer->new();
    
    my $stats = {
        total_products => scalar @{$product_model->get_all_products()},
        low_stock => scalar @{$product_model->get_low_stock_products()},
        total_orders => scalar @{$order_model->get_all_orders()},
        recent_orders => $order_model->get_recent_orders(5)
    };
    
    $c->stash(stats => $stats);
    $c->render(template => 'dashboard');
};

# Products
get '/products' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    use ECommerce::Models::Product;
    my $product_model = ECommerce::Models::Product->new();
    
    my $search = $c->param('search') // '';
    my $category = $c->param('category') // '';
    
    my $products;
    if ($search) {
        $products = $product_model->search_products($search);
    } elsif ($category) {
        $products = $product_model->get_products_by_category($category);
    } else {
        $products = $product_model->get_all_products();
    }
    
    my $categories = $product_model->get_categories();
    
    $c->stash(products => $products, categories => $categories);
    $c->render(template => 'products');
};

# Product detail
get '/products/:id' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    my $id = $c->param('id');
    use ECommerce::Models::Product;
    my $product_model = ECommerce::Models::Product->new();
    my $product = $product_model->get_product_by_id($id);
    
    $c->stash(product => $product);
    $c->render(template => 'product_detail');
};

# Add to cart
post '/cart/add' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    my $product_id = $c->param('product_id');
    my $quantity = $c->param('quantity') // 1;
    
    use ECommerce::Models::Product;
    my $product_model = ECommerce::Models::Product->new();
    my $product = $product_model->get_product_by_id($product_id);
    
    if ($product) {
        my $cart = $c->session('cart') // [];
        my $found = 0;
        
        foreach my $item (@$cart) {
            if ($item->{product_id} eq $product_id) {
                $item->{quantity} += $quantity;
                $found = 1;
                last;
            }
        }
        
        unless ($found) {
            push @$cart, {
                product_id => $product_id,
                name => $product->{name},
                price => $product->{price},
                quantity => $quantity
            };
        }
        
        $c->session(cart => $cart);
        $c->flash(success => 'Product added to cart!');
    }
    
    $c->redirect_to('/products');
};

# View cart
get '/cart' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    my $cart = $c->get_cart();
    $c->stash(cart => $cart);
    $c->render(template => 'cart');
};

# Checkout
post '/checkout' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    my $cart = $c->get_cart();
    return $c->redirect_to('/cart') unless @$cart;
    
    use ECommerce::Models::Order;
    my $order_model = ECommerce::Models::Order->new();
    
    my $customer_id = $c->session('customer_id');
    my $payment_method = $c->param('payment_method');
    my $shipping_address = $c->param('shipping_address');
    
    my $result = $order_model->create_order_from_cart($customer_id, $cart, {
        payment_method => $payment_method,
        shipping_address => $shipping_address
    });
    
    if ($result->{success}) {
        $c->clear_cart();
        $c->flash(success => 'Order placed successfully!');
        $c->redirect_to('/orders/' . $result->{order_id});
    } else {
        $c->flash(error => $result->{message});
        $c->redirect_to('/cart');
    }
};

# Orders
get '/orders' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    use ECommerce::Models::Order;
    my $order_model = ECommerce::Models::Order->new();
    
    my $orders;
    if ($c->has_role('customer')) {
        my $customer_id = $c->session('customer_id');
        $orders = $order_model->get_orders_by_customer($customer_id);
    } else {
        $orders = $order_model->get_all_orders();
    }
    
    $c->stash(orders => $orders);
    $c->render(template => 'orders');
};

# Order detail
get '/orders/:id' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    my $id = $c->param('id');
    use ECommerce::Models::Order;
    my $order_model = ECommerce::Models::Order->new();
    my $order = $order_model->get_order_by_id($id);
    my $items = $order_model->get_order_items($id);
    
    $c->stash(order => $order, items => $items);
    $c->render(template => 'order_detail');
};

# Customers (staff/admin only)
get '/customers' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') if $c->has_role('customer');
    
    use ECommerce::Models::Customer;
    my $customer_model = ECommerce::Models::Customer->new();
    my $customers = $customer_model->get_all_customers();
    
    $c->stash(customers => $customers);
    $c->render(template => 'customers');
};

# Reports (staff/admin only)
get '/reports' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') if $c->has_role('customer');
    
    use ECommerce::Models::Order;
    use ECommerce::Models::Product;
    use ECommerce::Models::Customer;
    
    my $order_model = ECommerce::Models::Order->new();
    my $product_model = ECommerce::Models::Product->new();
    my $customer_model = ECommerce::Models::Customer->new();
    
    my $stats = $order_model->get_order_stats();
    my $top_customers = $customer_model->get_top_customers(10);
    
    $c->stash(stats => $stats, top_customers => $top_customers);
    $c->render(template => 'reports');
};

# API endpoint for AJAX requests
get '/api/products' => sub ($c) {
    return $c->render(json => {error => 'Unauthorized'}, status => 401) unless $c->is_logged_in;
    
    use ECommerce::Models::Product;
    my $product_model = ECommerce::Models::Product->new();
    my $products = $product_model->get_all_products();
    
    $c->render(json => $products);
};

# Start the application
app->config(hypnotoad => {
    listen => ['http://*:3000'],
    workers => 4,
    pid_file => 'app.pid'
});

app->start;



