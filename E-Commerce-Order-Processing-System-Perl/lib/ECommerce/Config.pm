package ECommerce::Config;

# Configuration Module
# Contains all application settings and constants

use strict;
use warnings;
use utf8;
use File::Spec;
use File::Basename;

our $VERSION = '1.0.0';

# Base directory
our $BASE_DIR = dirname(dirname(dirname(__FILE__)));

# Database configuration
our $DB_PATH = File::Spec->catfile($BASE_DIR, 'data', 'ecommerce.db');

# Application configuration
our %APP_CONFIG = (
    app_name => 'E-Commerce Order Processing System',
    version => '1.0.0',
    currency => 'USD',
    currency_symbol => '$',
    tax_rate => 0.08,  # 8%
    shipping_rate => 5.00,
    free_shipping_threshold => 100.00,
    items_per_page => 20,
);

# Order status values
our @ORDER_STATUS = qw(
    pending
    processing
    shipped
    delivered
    cancelled
    refunded
);

# Payment methods
our @PAYMENT_METHODS = qw(
    credit_card
    debit_card
    paypal
    cash_on_delivery
    bank_transfer
);

# Product categories
our @PRODUCT_CATEGORIES = qw(
    Electronics
    Clothing
    Books
    Home
    Sports
    Toys
    Food
    Beauty
    Automotive
    Other
);

# User roles
our @USER_ROLES = qw(
    admin
    staff
    customer
);

# Color scheme (no gradients!)
our %COLORS = (
    primary => '#2E86AB',
    secondary => '#A23B72',
    success => '#06A77D',
    warning => '#F18F01',
    danger => '#C73E1D',
    info => '#4A90E2',
    light => '#F5F5F5',
    dark => '#333333',
);

1;

__END__

=head1 NAME

ECommerce::Config - Configuration module for E-Commerce application

=head1 DESCRIPTION

This module contains all configuration settings, constants, and application-wide
parameters for the E-Commerce Order Processing System.

=head1 CONFIGURATION

=head2 Database

Database path is configured via $DB_PATH variable.

=head2 Application Settings

Available in %APP_CONFIG hash:
- app_name
- version
- currency settings
- tax_rate
- shipping_rate
- items_per_page

=head1 AUTHOR

E-Commerce System Team

=head1 LICENSE

This is free software; you can redistribute it and/or modify it under
the same terms as Perl itself.

=cut
