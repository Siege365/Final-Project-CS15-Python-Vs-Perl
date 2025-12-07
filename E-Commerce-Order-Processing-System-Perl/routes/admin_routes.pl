#!/usr/bin/env perl
# Admin Routes - Staff and Admin only routes

use strict;
use warnings;

use ECommerce::Controllers::Admin::DashboardController;
use ECommerce::Controllers::Admin::ProductController;
use ECommerce::Controllers::Admin::OrderController;
use ECommerce::Controllers::Admin::CustomerController;
use ECommerce::Controllers::Admin::ReportController;

sub setup_admin_routes {
    my $app = shift;
    
    my $dashboard_ctrl = ECommerce::Controllers::Admin::DashboardController->new();
    my $product_ctrl = ECommerce::Controllers::Admin::ProductController->new();
    my $order_ctrl = ECommerce::Controllers::Admin::OrderController->new();
    my $customer_ctrl = ECommerce::Controllers::Admin::CustomerController->new();
    my $report_ctrl = ECommerce::Controllers::Admin::ReportController->new();
    
    # Products - Admin
    $app->routes->get('/products/add' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') if $c->has_role('customer');
        $product_ctrl->show_add_form($c);
    });
    
    $app->routes->post('/products/add' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') if $c->has_role('customer');
        $product_ctrl->create_product($c);
    });
    
    $app->routes->get('/products/:id/edit' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') if $c->has_role('customer');
        $product_ctrl->show_edit_form($c);
    });
    
    $app->routes->post('/products/:id/edit' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') if $c->has_role('customer');
        $product_ctrl->update_product($c);
    });
    
    $app->routes->post('/products/:id/delete' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') if $c->has_role('customer');
        $product_ctrl->delete_product($c);
    });
    
    # Orders - Admin
    $app->routes->post('/orders/:id/update-status' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') if $c->has_role('customer');
        $order_ctrl->update_status($c);
    });
    
    $app->routes->post('/orders/:id/delete' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') if $c->has_role('customer');
        $order_ctrl->delete_order($c);
    });
    
    # Customers - Admin
    $app->routes->get('/customers' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') if $c->has_role('customer');
        $customer_ctrl->list_customers($c);
    });
    
    $app->routes->post('/customers/:id/delete' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') if $c->has_role('customer');
        $customer_ctrl->delete_customer($c);
    });
    
    # Reports - Admin
    $app->routes->get('/reports' => sub {
        my $c = shift;
        return $c->redirect_to('/') unless $c->is_logged_in;
        return $c->redirect_to('/dashboard') if $c->has_role('customer');
        $report_ctrl->show_reports($c);
    });
}

1;
