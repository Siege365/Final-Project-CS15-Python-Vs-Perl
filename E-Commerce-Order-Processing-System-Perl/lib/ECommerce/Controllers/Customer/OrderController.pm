package ECommerce::Controllers::Customer::OrderController;

use strict;
use warnings;
use ECommerce::Models::Order;
use ECommerce::Models::Product;
use ECommerce::Models::Customer;

sub new {
    my $class = shift;
    return bless {}, $class;
}

sub checkout {
    my ($self, $c) = @_;
    
    my $cart = $c->get_cart();
    return $c->redirect_to('/cart') unless @$cart;
    
    # Get or create customer record
    my $customer_id = $c->session('customer_id');
    
    if (!$customer_id) {
        my $customer_model = ECommerce::Models::Customer->new();
        my $user_id = $c->session('user_id');
        my $existing_customer = $customer_model->get_customer_by_user_id($user_id);
        
        if ($existing_customer) {
            $customer_id = $existing_customer->{id};
            $c->session(customer_id => $customer_id);
        } else {
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
}

sub list_orders {
    my ($self, $c) = @_;
    
    my $order_model = ECommerce::Models::Order->new();
    
    my $sort = $c->param('sort') // '';
    my $search = $c->param('search') // '';
    my $page = $c->param('page') // 1;
    my $per_page = 10;
    
    my $customer_id = $c->session('customer_id');
    my $orders = $order_model->get_orders_by_customer($customer_id);
    
    # Search filter
    if ($search) {
        $orders = [grep {
            (lc($_->{order_number} // '') =~ /\Q$search\E/i) ||
            (lc($_->{status} // '') =~ /\Q$search\E/i) ||
            (lc($_->{payment_method} // '') =~ /\Q$search\E/i)
        } @$orders];
    }
    
    # Sort orders
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
        $orders = [sort { $b->{id} <=> $a->{id} } @$orders];
    }
    
    # Pagination
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
    $c->render(template => 'customer/orders_customer');
}

sub show_order_detail {
    my ($self, $c) = @_;
    
    my $id = $c->param('id');
    my $order_model = ECommerce::Models::Order->new();
    my $order = $order_model->get_order_by_id($id);
    my $items = $order_model->get_order_items($id);
    
    $c->stash(order => $order, items => $items, role => $c->session('role'));
    $c->render(template => 'customer/order_detail_customer');
}

sub cancel_order {
    my ($self, $c) = @_;
    
    my $id = $c->param('id');
    
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
}

1;
