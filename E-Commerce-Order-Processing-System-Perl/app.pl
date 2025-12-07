#!/usr/bin/env perl

# E-Commerce Order Processing System
# Main Application Entry Point
# Built with Mojolicious Framework
# Refactored with separated admin/customer controllers and routes

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

# Load route modules
require "$FindBin::Bin/routes/shared_routes.pl";
require "$FindBin::Bin/routes/admin_routes.pl";
require "$FindBin::Bin/routes/customer_routes.pl";

# Setup all routes
setup_shared_routes(app);
setup_admin_routes(app);
setup_customer_routes(app);

# Start the application
app->config(hypnotoad => {
    listen => ['http://*:3000'],
    workers => 4,
    pid_file => 'app.pid'
});

app->start;
