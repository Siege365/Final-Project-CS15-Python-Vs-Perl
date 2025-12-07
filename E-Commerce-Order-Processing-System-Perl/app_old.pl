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

# Helper to format numbers with commas
helper format_number => sub {
    my ($c, $number) = @_;
    $number = int($number) if defined $number;
    return '' unless defined $number;
    
    # Reverse the string, add commas every 3 digits, then reverse back
    my $reversed = reverse($number);
    $reversed =~ s/(\d{3})(?=\d)/$1,/g;
    return scalar reverse($reversed);
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
    $c->render(template => 'customer/register');
};

# Register POST
post '/register' => sub ($c) {
    my $username = $c->param('username');
    my $email = $c->param('email');
    my $first_name = $c->param('first_name') // '';
    my $last_name = $c->param('last_name') // '';
    my $phone = $c->param('phone') // '';
    my $address = $c->param('address') // '';
    my $password = $c->param('password');
    my $confirm_password = $c->param('confirm_password');
    
    if ($password ne $confirm_password) {
        $c->flash(error => 'Passwords do not match');
        return $c->redirect_to('/register');
    }
    
    use ECommerce::Controllers::Auth;
    my $auth = ECommerce::Controllers::Auth->new();
    my $result = $auth->register($username, $email, $password, 'customer', $phone, $address, $first_name, $last_name);
    
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
    
    my $role = $c->session('role');
    my $user_id = $c->session('user_id');
    my $customer_id = $c->session('customer_id');
    
    my $stats;
    
    if ($role eq 'admin' || $role eq 'staff') {
        # Admin/Staff Dashboard - all orders and full stats
        my $all_orders = $order_model->get_all_orders();
        my $active_orders = [grep { $_->{status} ne 'delivered' && $_->{status} ne 'cancelled' && $_->{status} ne 'refunded' } @$all_orders];
        
        my $page = $c->param('page') // 1;
        my $per_page = 10;
        my $recent = $order_model->get_recent_orders(100); # Get more for pagination
        my $total = scalar @$recent;
        my $total_pages = int(($total + $per_page - 1) / $per_page);
        my $offset = ($page - 1) * $per_page;
        $recent = [@$recent[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
        
        $stats = {
            total_products => scalar @{$product_model->get_all_products()},
            low_stock => scalar @{$product_model->get_low_stock_products()},
            total_orders => scalar @$active_orders,
            recent_orders => $recent,
            page => $page,
            total_pages => $total_pages
        };
    } else {
        # Customer Dashboard - only their orders
        my $customer_orders = $customer_id ? $order_model->get_orders_by_customer($customer_id) : [];
        my $shipped_orders = scalar(grep { $_->{status} eq 'shipped' } @$customer_orders);
        
        # Add pagination for customer dashboard
        my $page = $c->param('page') // 1;
        my $per_page = 10;
        my $total = scalar @$customer_orders;
        my $total_pages = int(($total + $per_page - 1) / $per_page);
        my $offset = ($page - 1) * $per_page;
        my $recent_orders = [@$customer_orders[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
        
        $stats = {
            total_orders => $total,
            shipped_orders => $shipped_orders,
            recent_orders => $recent_orders,
            page => $page,
            total_pages => $total_pages
        };
    }
    
    $c->stash(stats => $stats, role => $role);
    if ($role eq 'admin' || $role eq 'staff') {
        $c->render(template => 'admin/dashboard_admin');
    } else {
        $c->render(template => 'customer/dashboard_customer');
    }
};

# Products
get '/products' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    use ECommerce::Models::Product;
    my $product_model = ECommerce::Models::Product->new();
    
    my $search = $c->param('search') // '';
    my $category = $c->param('category') // '';
    my $sort = $c->param('sort') // '';
    my $page = $c->param('page') // 1;
    my $per_page = 10;
    
    my $products;
    if ($search) {
        $products = $product_model->search_products($search);
    } elsif ($category) {
        $products = $product_model->get_products_by_category($category);
    } else {
        $products = $product_model->get_all_products();
    }
    
    # Sort products (admin/staff only)
    if ($sort eq 'in_stock') {
        $products = [sort { ($b->{is_active} && $b->{stock_quantity} >= 15) <=> ($a->{is_active} && $a->{stock_quantity} >= 15) } @$products];
    } elsif ($sort eq 'low_stock') {
        $products = [sort { 
            my $a_low = $a->{is_active} && $a->{stock_quantity} > 0 && $a->{stock_quantity} < 15;
            my $b_low = $b->{is_active} && $b->{stock_quantity} > 0 && $b->{stock_quantity} < 15;
            $b_low <=> $a_low;
        } @$products];
    } elsif ($sort eq 'out_of_stock') {
        $products = [sort { ($b->{stock_quantity} == 0 || !$b->{is_active}) <=> ($a->{stock_quantity} == 0 || !$a->{is_active}) } @$products];
    } else {
        $products = [sort { $a->{id} <=> $b->{id} } @$products];
    }
    
    my $categories = $product_model->get_categories();
    
    # For customers: initial load only (infinite scroll handles rest)
    if ($c->has_role('customer')) {
        my $total = scalar @$products;
        my $offset = 0;
        $products = [@$products[$offset .. ($per_page - 1 > $total - 1 ? $total - 1 : $per_page - 1)]];
        
        $c->stash(
            products => $products,
            categories => $categories,
            search => $search,
            category => $category
        );
    } else {
        # For admin/staff: pagination
        my $total = scalar @$products;
        my $total_pages = int(($total + $per_page - 1) / $per_page);
        my $offset = ($page - 1) * $per_page;
        $products = [@$products[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
        
        $c->stash(
            products => $products, 
            categories => $categories,
            page => $page,
            total_pages => $total_pages,
            sort => $sort
        );
        $c->render(template => 'admin/products_admin');
    } else {
        $c->render(template => 'customer/products_customer');
    }
};

# Add product (admin/staff only)
get '/products/add' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') if $c->has_role('customer');
    
    use ECommerce::Models::Product;
    my $product_model = ECommerce::Models::Product->new();
    my $categories = $product_model->get_categories();
    
    $c->stash(categories => $categories);
    $c->render(template => 'admin/product_add');
};

post '/products/add' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') if $c->has_role('customer');
    
    use ECommerce::Models::Product;
    my $product_model = ECommerce::Models::Product->new();
    
    # Auto-generate SKU based on category
    my $category = $c->param('category');
    my %category_prefixes = (
        'Electronics' => 'ELEC',
        'Clothing' => 'CLTH',
        'Books' => 'BOOK',
        'Home & Garden' => 'HOME',
        'Sports' => 'SPRT',
        'Toys' => 'TOYS',
        'Food' => 'FOOD',
        'Beauty' => 'BEAU'
    );
    
    my $prefix = $category_prefixes{$category} || uc(substr($category, 0, 4));
    
    # Generate unique SKU with retry logic to prevent duplicates
    my $dbh = ECommerce::Database->new()->connect();
    my $sku;
    my $max_attempts = 100;
    my $attempt = 0;
    
    while ($attempt < $max_attempts) {
        # Get all SKUs with this prefix and extract the highest number
        my $sth = $dbh->prepare("SELECT sku FROM products WHERE sku LIKE ? ORDER BY sku DESC");
        $sth->execute("$prefix%");
        
        my $next_number = 1;
        my @existing_numbers;
        
        while (my $row = $sth->fetchrow_hashref()) {
            if ($row->{sku} =~ /^$prefix(\d+)$/) {
                push @existing_numbers, int($1);
            }
        }
        $sth->finish();
        
        # Find the highest number and increment
        if (@existing_numbers) {
            $next_number = (sort { $b <=> $a } @existing_numbers)[0] + 1;
        }
        
        $sku = sprintf("%s%03d", $prefix, $next_number);
        
        # Verify SKU doesn't exist (double-check)
        my $check_sth = $dbh->prepare("SELECT COUNT(*) FROM products WHERE sku = ?");
        $check_sth->execute($sku);
        my ($count) = $check_sth->fetchrow_array();
        $check_sth->finish();
        
        if ($count == 0) {
            last; # SKU is unique, exit loop
        }
        
        $attempt++;
    }
    
    $dbh->disconnect();
    
    # If we couldn't generate a unique SKU after max attempts
    if ($attempt >= $max_attempts) {
        $c->flash(error => 'Failed to generate unique SKU. Please try again.');
        return $c->redirect_to('/products/add');
    }
    
    my $result = $product_model->create_product(
        name => $c->param('name'),
        description => $c->param('description'),
        sku => $sku,
        category => $category,
        price => $c->param('price'),
        cost => $c->param('cost'),
        stock_quantity => $c->param('stock_quantity'),
        reorder_level => $c->param('reorder_level'),
        image_url => $c->param('image_url')
    );
    
    if ($result->{success}) {
        $c->flash(success => 'Product added successfully');
        $c->redirect_to('/products');
    } else {
        $c->flash(error => $result->{message});
        $c->redirect_to('/products/add');
    }
};

# Edit product (admin/staff only)
get '/products/:id/edit' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') if $c->has_role('customer');
    
    my $id = $c->param('id');
    use ECommerce::Models::Product;
    my $product_model = ECommerce::Models::Product->new();
    my $product = $product_model->get_product_by_id($id);
    my $categories = $product_model->get_categories();
    
    $c->stash(product => $product, categories => $categories);
    $c->render(template => 'admin/product_edit');
};

post '/products/:id/edit' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') if $c->has_role('customer');
    
    my $id = $c->param('id');
    use ECommerce::Models::Product;
    my $product_model = ECommerce::Models::Product->new();
    
    my $result = $product_model->update_product(
        $id,
        name => $c->param('name'),
        description => $c->param('description'),
        sku => $c->param('sku'),
        category => $c->param('category'),
        price => $c->param('price'),
        cost => $c->param('cost'),
        stock_quantity => $c->param('stock_quantity'),
        reorder_level => $c->param('reorder_level'),
        image_url => $c->param('image_url'),
        is_active => $c->param('is_active')
    );
    
    if ($result->{success}) {
        $c->flash(success => 'Product updated successfully');
        $c->redirect_to('/products');
    } else {
        $c->flash(error => $result->{message});
        $c->redirect_to("/products/$id/edit");
    }
};

# Delete product (admin/staff only)
post '/products/:id/delete' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') if $c->has_role('customer');
    
    my $id = $c->param('id');
    use ECommerce::Models::Product;
    my $product_model = ECommerce::Models::Product->new();
    
    my $result = $product_model->delete_product($id);
    
    if ($result->{success}) {
        $c->flash(success => 'Product deleted successfully');
    } else {
        $c->flash(error => $result->{message});
    }
    $c->redirect_to('/products');
};

# Product detail (currently not used - products use inline cards)
# get '/products/:id' => sub ($c) {
#     return $c->redirect_to('/') unless $c->is_logged_in;
#     
#     my $id = $c->param('id');
#     use ECommerce::Models::Product;
#     my $product_model = ECommerce::Models::Product->new();
#     my $product = $product_model->get_product_by_id($id);
#     
#     $c->stash(product => $product);
#     $c->render(template => 'product_detail');
# };

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

# Remove from cart
post '/cart/remove' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    my $product_id = $c->param('product_id');
    my $cart = $c->session('cart') // [];
    
    # Filter out the product to remove
    $cart = [grep { $_->{product_id} ne $product_id } @$cart];
    
    $c->session(cart => $cart);
    $c->flash(success => 'Product removed from cart');
    $c->redirect_to('/cart');
};

# View cart
get '/cart' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    my $cart = $c->get_cart();
    $c->stash(cart => $cart);
    $c->render(template => 'customer/cart');
};

# Checkout
post '/checkout' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    my $cart = $c->get_cart();
    return $c->redirect_to('/cart') unless @$cart;
    
    # Get or create customer record
    my $customer_id = $c->session('customer_id');
    
    # If no customer_id in session, create one for this user
    if (!$customer_id) {
        use ECommerce::Models::Customer;
        my $customer_model = ECommerce::Models::Customer->new();
        
        my $user_id = $c->session('user_id');
        my $existing_customer = $customer_model->get_customer_by_user_id($user_id);
        
        if ($existing_customer) {
            $customer_id = $existing_customer->{id};
            $c->session(customer_id => $customer_id);
        } else {
            # Create new customer record
            my $result = $customer_model->create_customer(
                user_id => $user_id,
                first_name => $c->session('username'),
                last_name => '',
                phone => '',
                address => ''
            );
            
            if ($result->{success}) {
                $customer_id = $result->{customer_id};
                $c->session(customer_id => $customer_id);
            } else {
                $c->flash(error => 'Failed to create customer profile');
                return $c->redirect_to('/cart');
            }
        }
    }
    
    use ECommerce::Models::Order;
    my $order_model = ECommerce::Models::Order->new();
    
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
    
    my $sort = $c->param('sort') // '';
    my $search = $c->param('search') // '';
    my $page = $c->param('page') // 1;
    my $per_page = 10;
    
    my $orders;
    if ($c->has_role('customer')) {
        my $customer_id = $c->session('customer_id');
        $orders = $order_model->get_orders_by_customer($customer_id);
        
        # Search filter for customers
        if ($search) {
            $orders = [grep {
                (lc($_->{order_number} // '') =~ /\Q$search\E/i) ||
                (lc($_->{status} // '') =~ /\Q$search\E/i) ||
                (lc($_->{payment_method} // '') =~ /\Q$search\E/i)
            } @$orders];
        }
        
        # Sort orders for customers
        if ($sort eq 'recent') {
            $orders = [sort { $b->{id} <=> $a->{id} } @$orders];
        } elsif ($sort eq 'earliest') {
            $orders = [sort { $a->{id} <=> $b->{id} } @$orders];
        } elsif ($sort eq 'pending') {
            $orders = [sort { ($b->{status} eq 'pending') <=> ($a->{status} eq 'pending') } @$orders];
        } elsif ($sort eq 'processing') {
            $orders = [sort { ($b->{status} eq 'processing') <=> ($a->{status} eq 'processing') } @$orders];
        } elsif ($sort eq 'shipped') {
            $orders = [sort { ($b->{status} eq 'shipped') <=> ($a->{status} eq 'shipped') } @$orders];
        } elsif ($sort eq 'delivered') {
            $orders = [sort { ($b->{status} eq 'delivered') <=> ($a->{status} eq 'delivered') } @$orders];
        } elsif ($sort eq 'cancelled') {
            $orders = [sort { ($b->{status} eq 'cancelled') <=> ($a->{status} eq 'cancelled') } @$orders];
        } else {
            # Default: most recent first
            $orders = [sort { $b->{id} <=> $a->{id} } @$orders];
        }
        
        # Pagination for customers
        my $total = scalar @$orders;
        my $total_pages = int(($total + $per_page - 1) / $per_page);
        my $offset = ($page - 1) * $per_page;
        $orders = [@$orders[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
        
        $c->stash(
            orders => $orders,
            sort => $sort,
            search => $search,
            page => $page,
            total_pages => $total_pages
        );
        return $c->render(template => 'customer/orders_customer');
    } else {
        $orders = $order_model->get_all_orders();
        
        # Search filter
        if ($search) {
            $orders = [grep {
                (lc($_->{order_number} // '') =~ /\Q$search\E/i) ||
                (lc($_->{first_name} // '') =~ /\Q$search\E/i) ||
                (lc($_->{last_name} // '') =~ /\Q$search\E/i) ||
                (lc($_->{status} // '') =~ /\Q$search\E/i) ||
                (lc($_->{payment_method} // '') =~ /\Q$search\E/i)
            } @$orders];
        }
        
        # Sort orders for admin/staff
        if ($sort eq 'recent') {
            $orders = [sort { $b->{id} <=> $a->{id} } @$orders];
        } elsif ($sort eq 'cancelled') {
            $orders = [sort { $b->{id} <=> $a->{id} } @$orders];
        } elsif ($sort eq 'cancelled') {
            $orders = [sort { ($b->{status} eq 'cancelled') <=> ($a->{status} eq 'cancelled') } @$orders];
        } elsif ($sort eq 'pending') {
            $orders = [sort { ($b->{status} eq 'pending') <=> ($a->{status} eq 'pending') } @$orders];
        } elsif ($sort eq 'shipped') {
            $orders = [sort { ($b->{status} eq 'shipped') <=> ($a->{status} eq 'shipped') } @$orders];
        } elsif ($sort eq 'processing') {
            $orders = [sort { ($b->{status} eq 'processing') <=> ($a->{status} eq 'processing') } @$orders];
        } elsif ($sort eq 'delivered') {
            $orders = [sort { ($b->{status} eq 'delivered') <=> ($a->{status} eq 'delivered') } @$orders];
        } else { # earliest
            $orders = [sort { $a->{id} <=> $b->{id} } @$orders];
        }
        
        # Pagination for admin/staff only
        my $total = scalar @$orders;
        my $total_pages = int(($total + $per_page - 1) / $per_page);
        my $offset = ($page - 1) * $per_page;
        $orders = [@$orders[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
        
        $c->stash(
            orders => $orders,
            page => $page,
            total_pages => $total_pages,
            sort => $sort,
            search => $search
        );
        return $c->render(template => 'admin/orders_admin');
    }
};

# Order detail
get '/orders/:id' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    
    my $id = $c->param('id');
    use ECommerce::Models::Order;
    my $order_model = ECommerce::Models::Order->new();
    my $order = $order_model->get_order_by_id($id);
    my $items = $order_model->get_order_items($id);
    
    my $role = $c->session('role') // 'customer';
    $c->stash(order => $order, items => $items, role => $role);
    if ($role eq 'admin' || $role eq 'staff') {
        $c->render(template => 'admin/order_detail_admin');
    } else {
        $c->render(template => 'customer/order_detail_customer');
    }
};

# Update order status (admin/staff only)
post '/orders/:id/update-status' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') if $c->has_role('customer');
    
    my $id = $c->param('id');
    my $status = $c->param('status');
    
    use ECommerce::Models::Order;
    my $order_model = ECommerce::Models::Order->new();
    $order_model->update_order_status($id, $status);
    
    $c->flash(success => "Order status updated to $status");
    $c->redirect_to('/orders/' . $id);
};

# Delete order (admin/staff only)
post '/orders/:id/delete' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') if $c->has_role('customer');
    
    my $id = $c->param('id');
    use ECommerce::Models::Order;
    my $order_model = ECommerce::Models::Order->new();
    
    my $result = $order_model->delete_order($id);
    
    if ($result->{success}) {
        $c->flash(success => 'Order deleted successfully');
    } else {
        $c->flash(error => $result->{message});
    }
    $c->redirect_to('/orders');
};

# Cancel order (customer only, pending orders)
post '/orders/:id/cancel' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') unless $c->has_role('customer');
    
    my $id = $c->param('id');
    
    use ECommerce::Models::Order;
    use ECommerce::Models::Product;
    my $order_model = ECommerce::Models::Order->new();
    my $product_model = ECommerce::Models::Product->new();
    my $order = $order_model->get_order_by_id($id);
    
    # Verify order belongs to customer and is pending
    if ($order->{customer_id} ne $c->session('customer_id')) {
        $c->flash(error => 'You can only cancel your own orders');
        return $c->redirect_to('/orders');
    }
    
    if ($order->{status} ne 'pending') {
        $c->flash(error => 'Only pending orders can be cancelled');
        return $c->redirect_to('/orders/' . $id);
    }
    
    # Get order items to restore stock
    my $items = $order_model->get_order_items($id);
    
    # Restore stock for each item
    foreach my $item (@$items) {
        my $product = $product_model->get_product_by_id($item->{product_id});
        if ($product) {
            my $new_stock = $product->{stock_quantity} + $item->{quantity};
            $product_model->update_product($item->{product_id}, stock_quantity => $new_stock);
        }
    }
    
    # Update order status to cancelled
    $order_model->update_order_status($id, 'cancelled');
    $c->flash(success => 'Order cancelled successfully. Stock has been restored.');
    $c->redirect_to('/orders/' . $id);
};

# Account Settings (customer only)
get '/account' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') unless $c->has_role('customer');
    
    use ECommerce::Models::Customer;
    use ECommerce::Models::User;
    
    my $user_model = ECommerce::Models::User->new();
    my $customer_model = ECommerce::Models::Customer->new();
    
    my $user_id = $c->session('user_id');
    my $customer_id = $c->session('customer_id');
    
    my $user = $user_model->get_user_by_id($user_id);
    my $customer = $customer_id ? $customer_model->get_customer_by_id($customer_id) : undef;
    
    $c->stash(user => $user, customer => $customer);
    $c->render(template => 'customer/account');
};

# Update Account Settings
post '/account/update' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') unless $c->has_role('customer');
    
    my $phone = $c->param('phone');
    my $address = $c->param('address');
    my $first_name = $c->param('first_name');
    my $last_name = $c->param('last_name');
    
    use ECommerce::Models::Customer;
    my $customer_model = ECommerce::Models::Customer->new();
    my $customer_id = $c->session('customer_id');
    
    if ($customer_id) {
        $customer_model->update_customer($customer_id,
            first_name => $first_name,
            last_name => $last_name,
            phone => $phone,
            address => $address
        );
        $c->flash(success => 'Account updated successfully!');
    }
    
    $c->redirect_to('/account');
};

# Delete Account (customer only - deactivate)
post '/account/delete' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') unless $c->has_role('customer');
    
    use ECommerce::Models::User;
    my $user_model = ECommerce::Models::User->new();
    my $user_id = $c->session('user_id');
    
    # Deactivate user account
    $user_model->deactivate_user($user_id);
    
    # Log out the user
    $c->session(expires => 1);
    $c->flash(success => 'Your account has been deactivated');
    $c->redirect_to('/');
};

# Customers (staff/admin only)
get '/customers' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') if $c->has_role('customer');
    
    use ECommerce::Models::Customer;
    my $customer_model = ECommerce::Models::Customer->new();
    my $customers = $customer_model->get_all_customers();
    
    my $sort = $c->param('sort') // '';
    my $search = $c->param('search') // '';
    my $page = $c->param('page') // 1;
    my $per_page = 10;
    
    # Search filter
    if ($search) {
        $customers = [grep {
            (lc($_->{username} // '') =~ /\Q$search\E/i) ||
            (lc($_->{email} // '') =~ /\Q$search\E/i) ||
            (lc($_->{first_name} // '') =~ /\Q$search\E/i) ||
            (lc($_->{last_name} // '') =~ /\Q$search\E/i) ||
            (lc($_->{phone} // '') =~ /\Q$search\E/i) ||
            (lc($_->{address} // '') =~ /\Q$search\E/i)
        } @$customers];
    }
    
    # Sort customers
    if ($sort eq 'recent') {
        $customers = [sort { $b->{id} <=> $a->{id} } @$customers];
    } elsif ($sort eq 'inactive') {
        $customers = [sort { !$a->{is_active} <=> !$b->{is_active} } @$customers];
    } elsif ($sort eq 'all') {
        # Keep original order
    } else { # id
        $customers = [sort { $a->{id} <=> $b->{id} } @$customers];
    }
    
    # Pagination
    my $total = scalar @$customers;
    my $total_pages = int(($total + $per_page - 1) / $per_page);
    my $offset = ($page - 1) * $per_page;
    $customers = [@$customers[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
    
    $c->stash(
        customers => $customers,
        page => $page,
        total_pages => $total_pages,
        sort => $sort,
        search => $search
    );
    $c->render(template => 'admin/customers');
};

# Delete customer (admin/staff only)
post '/customers/:id/delete' => sub ($c) {
    return $c->redirect_to('/') unless $c->is_logged_in;
    return $c->redirect_to('/dashboard') if $c->has_role('customer');
    
    my $id = $c->param('id');
    use ECommerce::Models::Customer;
    my $customer_model = ECommerce::Models::Customer->new();
    
    my $result = $customer_model->delete_customer($id);
    
    if ($result->{success}) {
        $c->flash(success => 'Customer deleted successfully');
    } else {
        $c->flash(error => $result->{message});
    }
    $c->redirect_to('/customers');
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
    my $all_customers = $customer_model->get_top_customers(100);
    
    # Pagination for top customers
    my $page = $c->param('page') // 1;
    my $per_page = 10;
    my $total = scalar @$all_customers;
    my $total_pages = int(($total + $per_page - 1) / $per_page);
    my $offset = ($page - 1) * $per_page;
    my $top_customers = [@$all_customers[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
    
    $c->stash(
        stats => $stats, 
        top_customers => $top_customers,
        page => $page,
        total_pages => $total_pages
    );
    $c->render(template => 'admin/reports');
};

# API endpoint for AJAX requests (infinite scroll)
get '/api/products' => sub ($c) {
    return $c->render(json => {error => 'Unauthorized'}, status => 401) unless $c->is_logged_in;
    
    use ECommerce::Models::Product;
    my $product_model = ECommerce::Models::Product->new();
    
    my $search = $c->param('search') // '';
    my $category = $c->param('category') // '';
    my $page = $c->param('page') // 1;
    my $per_page = 10;
    
    my $products;
    if ($search) {
        $products = $product_model->search_products($search);
    } elsif ($category) {
        $products = $product_model->get_products_by_category($category);
    } else {
        $products = $product_model->get_all_products();
    }
    
    # Pagination
    my $total = scalar @$products;
    my $offset = ($page - 1) * $per_page;
    $products = [@$products[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
    
    $c->render(json => {
        products => $products,
        has_more => ($offset + $per_page) < $total
    });
};

# Start the application
app->config(hypnotoad => {
    listen => ['http://*:3000'],
    workers => 4,
    pid_file => 'app.pid'
});

app->start;



