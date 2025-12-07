package ECommerce::Controllers::Admin::OrderController;

use strict;
use warnings;
use ECommerce::Models::Order;

sub new {
    my $class = shift;
    return bless {}, $class;
}

sub list_orders {
    my ($self, $c) = @_;
    
    my $order_model = ECommerce::Models::Order->new();
    
    my $sort = $c->param('sort') // '';
    my $search = $c->param('search') // '';
    my $page = $c->param('page') // 1;
    my $per_page = 10;
    
    my $orders = $order_model->get_all_orders();
    
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
    
    # Sort orders
    if ($sort eq 'recent') {
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
    } else {
        $orders = [sort { $a->{id} <=> $b->{id} } @$orders];
    }
    
    # Pagination
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
    $c->render(template => 'admin/orders_admin');
}

sub show_order_detail {
    my ($self, $c) = @_;
    
    my $id = $c->param('id');
    my $order_model = ECommerce::Models::Order->new();
    my $order = $order_model->get_order_by_id($id);
    my $items = $order_model->get_order_items($id);
    
    $c->stash(order => $order, items => $items, role => $c->session('role'));
    $c->render(template => 'admin/order_detail_admin');
}

sub update_status {
    my ($self, $c) = @_;
    
    my $id = $c->param('id');
    my $status = $c->param('status');
    
    my $order_model = ECommerce::Models::Order->new();
    $order_model->update_order_status($id, $status);
    
    $c->flash(success => "Order status updated to $status");
    $c->redirect_to('/orders/' . $id);
}

sub delete_order {
    my ($self, $c) = @_;
    
    my $id = $c->param('id');
    my $order_model = ECommerce::Models::Order->new();
    
    my $result = $order_model->delete_order($id);
    
    if ($result->{success}) {
        $c->flash(success => 'Order deleted successfully');
    } else {
        $c->flash(error => $result->{message});
    }
    $c->redirect_to('/orders');
}

1;
