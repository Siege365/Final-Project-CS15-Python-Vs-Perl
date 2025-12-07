package ECommerce::Controllers::Admin::DashboardController;

use strict;
use warnings;
use ECommerce::Models::Product;
use ECommerce::Models::Order;
use ECommerce::Models::Customer;

sub new {
    my $class = shift;
    return bless {}, $class;
}

sub show_dashboard {
    my ($self, $c) = @_;
    
    my $product_model = ECommerce::Models::Product->new();
    my $order_model = ECommerce::Models::Order->new();
    my $customer_model = ECommerce::Models::Customer->new();
    
    my $all_orders = $order_model->get_all_orders();
    my $active_orders = [grep { $_->{status} ne 'delivered' && $_->{status} ne 'cancelled' && $_->{status} ne 'refunded' } @$all_orders];
    
    # Get only 5 most recent orders for dashboard
    my $recent = $order_model->get_recent_orders(5);
    
    my $stats = {
        total_products => scalar @{$product_model->get_all_products()},
        low_stock => scalar @{$product_model->get_low_stock_products()},
        total_orders => scalar @$active_orders,
        recent_orders => $recent
    };
    
    $c->stash(stats => $stats, role => $c->session('role'));
    $c->render(template => 'admin/dashboard_admin');
}

1;
