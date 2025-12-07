#!/usr/bin/env perl
# Customer Routes - Customer only routes

use strict;
use warnings;

use ECommerce::Controllers::Customer::DashboardController;
use ECommerce::Controllers::Customer::ProductController;
use ECommerce::Controllers::Customer::CartController;
use ECommerce::Controllers::Customer::OrderController;
use ECommerce::Controllers::Customer::AccountController;

sub setup_customer_routes {
    my $app = shift;
    
    my $dashboard_ctrl = ECommerce::Controllers::Customer::DashboardController->new();
    my $product_ctrl = ECommerce::Controllers::Customer::ProductController->new();
    my $cart_ctrl = ECommerce::Controllers::Customer::CartController->new();
    my $order_ctrl = ECommerce::Controllers::Customer::OrderController->new();
    my $account_ctrl = ECommerce::Controllers::Customer::AccountController->new();
    
    # Cart - Customer
    $app->routes->get('/cart' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        $cart_ctrl->view_cart($c);
    });
    
    $app->routes->post('/cart/add' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        $cart_ctrl->add_to_cart($c);
    });
    
    $app->routes->post('/cart/remove' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        $cart_ctrl->remove_from_cart($c);
    });
    
    # Checkout - Customer
    $app->routes->post('/checkout' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        $order_ctrl->checkout($c);
    });
    
    # Cancel Order - Customer
    $app->routes->post('/orders/:id/cancel' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') unless $c->has_role('customer');
        $order_ctrl->cancel_order($c);
    });
    
    # Account - Customer
    $app->routes->get('/account' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') unless $c->has_role('customer');
        $account_ctrl->show_account($c);
    });
    
    $app->routes->post('/account/update' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') unless $c->has_role('customer');
        $account_ctrl->update_account($c);
    });
    
    $app->routes->post('/account/delete' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') unless $c->has_role('customer');
        $account_ctrl->delete_account($c);
    });
}

1;
