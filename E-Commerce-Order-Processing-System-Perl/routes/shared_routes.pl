#!/usr/bin/env perl
# Shared Routes - Routes accessible by both admin and customer

use strict;
use warnings;

use ECommerce::Controllers::Auth;
use ECommerce::Controllers::Admin::DashboardController;
use ECommerce::Controllers::Customer::DashboardController;
use ECommerce::Controllers::Admin::ProductController;
use ECommerce::Controllers::Customer::ProductController;
use ECommerce::Controllers::Admin::OrderController;
use ECommerce::Controllers::Customer::OrderController;
use ECommerce::Models::Product;

sub setup_shared_routes {
    my $app = shift;
    
    my $admin_dashboard_ctrl = ECommerce::Controllers::Admin::DashboardController->new();
    my $customer_dashboard_ctrl = ECommerce::Controllers::Customer::DashboardController->new();
    my $admin_product_ctrl = ECommerce::Controllers::Admin::ProductController->new();
    my $customer_product_ctrl = ECommerce::Controllers::Customer::ProductController->new();
    my $admin_order_ctrl = ECommerce::Controllers::Admin::OrderController->new();
    my $customer_order_ctrl = ECommerce::Controllers::Customer::OrderController->new();
    
    # Home / Login
    $app->routes->get('/' => sub {
        my $c = shift;
        if ($c->is_logged_in) {
            return $c->redirect_to('/dashboard');
        }
        $c->render(template => 'login');
    });
    
    # Login POST
    $app->routes->post('/login' => sub {
        my $c = shift;
        my $username = $c->param('username');
        my $password = $c->param('password');
        
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
    });
    
    # Logout
    $app->routes->get('/logout' => sub {
        my $c = shift;
        $c->session(expires => 1);
        $c->flash(success => 'Logged out successfully');
        $c->redirect_to('/');
    });
    
    # Register
    $app->routes->get('/register' => sub {
        my $c = shift;
        $c->render(template => 'customer/register');
    });
    
    $app->routes->post('/register' => sub {
        my $c = shift;
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
        
        my $auth = ECommerce::Controllers::Auth->new();
        my $result = $auth->register($username, $email, $password, 'customer', $phone, $address, $first_name, $last_name);
        
        if ($result->{success}) {
            $c->flash(success => 'Registration successful! Please login.');
            return $c->redirect_to('/');
        } else {
            $c->flash(error => $result->{message});
            return $c->redirect_to('/register');
        }
    });
    
    # Dashboard - Role-based
    $app->routes->get('/dashboard' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        
        my $role = $c->session('role');
        if ($role eq 'admin' || $role eq 'staff') {
            $admin_dashboard_ctrl->show_dashboard($c);
        } else {
            $customer_dashboard_ctrl->show_dashboard($c);
        }
    });
    
    # Products - Role-based
    $app->routes->get('/products' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        
        if ($c->has_role('customer')) {
            $customer_product_ctrl->list_products($c);
        } else {
            $admin_product_ctrl->list_products($c);
        }
    });
    
    # Orders - Role-based
    $app->routes->get('/orders' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        
        if ($c->has_role('customer')) {
            $customer_order_ctrl->list_orders($c);
        } else {
            $admin_order_ctrl->list_orders($c);
        }
    });
    
    # Order Detail - Role-based
    $app->routes->get('/orders/:id' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        
        my $role = $c->session('role') // 'customer';
        if ($role eq 'admin' || $role eq 'staff') {
            $admin_order_ctrl->show_order_detail($c);
        } else {
            $customer_order_ctrl->show_order_detail($c);
        }
    });
    
    # API endpoint for infinite scroll
    $app->routes->get('/api/products' => sub {
        my $c = shift;
        return $c->render(json => {error => 'Unauthorized'}, status => 401) unless $c->is_logged_in;
        
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
        
        # Sort by id to match initial page load order
        $products = [sort { $a->{id} <=> $b->{id} } @$products];
        
        # Pagination
        my $total = scalar @$products;
        my $offset = ($page - 1) * $per_page;
        $products = [@$products[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
        
        $c->render(json => {
            products => $products,
            has_more => ($offset + $per_page) < $total
        });
    });
}

1;
