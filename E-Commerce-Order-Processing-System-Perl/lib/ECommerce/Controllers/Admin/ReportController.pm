package ECommerce::Controllers::Admin::ReportController;

use strict;
use warnings;
use ECommerce::Models::Order;
use ECommerce::Models::Product;
use ECommerce::Models::Customer;

sub new {
    my $class = shift;
    return bless {}, $class;
}

sub show_reports {
    my ($self, $c) = @_;
    
    my $order_model = ECommerce::Models::Order->new();
    my $product_model = ECommerce::Models::Product->new();
    my $customer_model = ECommerce::Models::Customer->new();
    
    my $stats = $order_model->get_order_stats();
    # Get only top 10 customers
    my $top_customers = $customer_model->get_top_customers(10);
    
    # Add total customers count
    my $all_customers = $customer_model->get_all_customers();
    $stats->{total_customers} = scalar @$all_customers;
    
    $c->stash(
        stats => $stats, 
        top_customers => $top_customers
    );
    $c->render(template => 'admin/reports');
}

1;
