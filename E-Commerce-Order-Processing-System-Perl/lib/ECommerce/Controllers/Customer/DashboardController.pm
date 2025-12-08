package ECommerce::Controllers::Customer::DashboardController;

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
    
    my $customer_id = $c->session('customer_id');
    my $customer_orders = $customer_id ? $order_model->get_orders_by_customer($customer_id) : [];
    my $shipped_orders = scalar(grep { $_->{status} eq 'shipped' } @$customer_orders);
    my $pending_orders = scalar(grep { $_->{status} eq 'pending' || $_->{status} eq 'processing' } @$customer_orders);
    my $delivered_orders = scalar(grep { $_->{status} eq 'delivered' } @$customer_orders);
    
    # Calculate total spent
    my $total_spent = 0;
    for my $order (@$customer_orders) {
        $total_spent += $order->{total_amount} || 0 if $order->{status} ne 'cancelled' && $order->{status} ne 'refunded';
    }
    
    # Pagination
    my $page = $c->param('page') // 1;
    my $per_page = 10;
    my $total = scalar @$customer_orders;
    my $total_pages = int(($total + $per_page - 1) / $per_page);
    my $offset = ($page - 1) * $per_page;
    my $recent_orders = [@$customer_orders[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
    
    my $stats = {
        total_orders => $total,
        shipped_orders => $shipped_orders,
        pending_orders => $pending_orders,
        delivered_orders => $delivered_orders,
        total_spent => $total_spent,
        recent_orders => $recent_orders,
        page => $page,
        total_pages => $total_pages
    };
    
    $c->stash(stats => $stats, role => $c->session('role'));
    $c->render(template => 'customer/dashboard_customer');
}

1;
