package ECommerce::Models::Order;

# Order Model
# Handles all order-related database operations

use strict;
use warnings;
use utf8;
use ECommerce::Database;
use ECommerce::Models::Product;
use Time::Piece;

sub new {
    my $class = shift;
    my $self = {
        db => ECommerce::Database->new(),
        product_model => ECommerce::Models::Product->new(),
    };
    return bless $self, $class;
}

sub generate_order_number {
    my $self = shift;
    my $t = localtime;
    return sprintf("ORD-%s-%05d", $t->strftime('%Y%m%d'), int(rand(99999)));
}

sub create_order {
    my ($self, %params) = @_;
    
    my $dbh = $self->{db}->connect();
    
    my $order_id;
    my $order_number;
    
    $dbh->begin_work();
    
    eval {
        # Create order
        $order_number = $self->generate_order_number();
        
        $dbh->do(
            "INSERT INTO orders (order_number, customer_id, status, subtotal, tax, shipping, total, 
             payment_method, payment_status, shipping_address, billing_address, notes) 
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            undef,
            $order_number, $params{customer_id}, $params{status} // 'pending',
            $params{subtotal}, $params{tax} // 0, $params{shipping} // 0, $params{total},
            $params{payment_method}, $params{payment_status} // 'pending',
            $params{shipping_address}, $params{billing_address}, $params{notes}
        );
        
        $order_id = $dbh->last_insert_id(undef, undef, 'orders', 'id');
        
        # Create order items
        foreach my $item (@{$params{items}}) {
            $dbh->do(
                "INSERT INTO order_items (order_id, product_id, product_name, product_sku, quantity, unit_price, subtotal) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)",
                undef,
                $order_id, $item->{product_id}, $item->{product_name}, $item->{product_sku},
                $item->{quantity}, $item->{unit_price}, $item->{subtotal}
            );
            
            # Update product stock directly (avoid nested transactions)
            $dbh->do(
                "UPDATE products SET stock_quantity = stock_quantity - ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                undef,
                $item->{quantity}, $item->{product_id}
            );
            
            # Record inventory transaction
            $dbh->do(
                "INSERT INTO inventory_transactions (product_id, quantity_change, transaction_type, reference_id, notes) 
                 VALUES (?, ?, ?, ?, ?)",
                undef,
                $item->{product_id}, -$item->{quantity}, 'sale', $order_id, "Order $order_number"
            );
        }
        
        $dbh->commit();
    };
    
    if ($@) {
        $dbh->rollback();
        $dbh->disconnect();
        return {success => 0, message => "Failed to create order: $@"};
    }
    
    $dbh->disconnect();
    
    return {success => 1, order_id => $order_id, order_number => $order_number};
}

sub create_order_from_cart {
    my ($self, $customer_id, $cart, $params) = @_;
    
    return {success => 0, message => 'Customer ID is required'} unless $customer_id;
    return {success => 0, message => 'Cart is empty'} unless @$cart;
    
    my $subtotal = 0;
    my @items;
    
    foreach my $cart_item (@$cart) {
        my $product = $self->{product_model}->get_product_by_id($cart_item->{product_id});
        
        unless ($product) {
            return {success => 0, message => "Product not found: " . $cart_item->{product_id}};
        }
        
        if ($product->{stock_quantity} < $cart_item->{quantity}) {
            return {success => 0, message => "Insufficient stock for: " . $product->{name}};
        }
        
        my $item_subtotal = $product->{price} * $cart_item->{quantity};
        $subtotal += $item_subtotal;
        
        push @items, {
            product_id => $product->{id},
            product_name => $product->{name},
            product_sku => $product->{sku},
            quantity => $cart_item->{quantity},
            unit_price => $product->{price},
            subtotal => $item_subtotal,
        };
    }
    
    use ECommerce::Config;
    my $tax = $subtotal * $ECommerce::Config::APP_CONFIG{tax_rate};
    my $shipping = $subtotal >= $ECommerce::Config::APP_CONFIG{free_shipping_threshold} 
        ? 0 
        : $ECommerce::Config::APP_CONFIG{shipping_rate};
    my $total = $subtotal + $tax + $shipping;
    
    return $self->create_order(
        customer_id => $customer_id,
        subtotal => $subtotal,
        tax => $tax,
        shipping => $shipping,
        total => $total,
        payment_method => $params->{payment_method},
        shipping_address => $params->{shipping_address},
        billing_address => $params->{billing_address} // $params->{shipping_address},
        notes => $params->{notes},
        items => \@items,
    );
}

sub get_all_orders {
    my $self = shift;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT o.*, c.first_name, c.last_name 
         FROM orders o 
         LEFT JOIN customers c ON o.customer_id = c.id 
         ORDER BY o.created_at DESC"
    );
    $sth->execute();
    my $orders = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $orders;
}

sub get_order_by_id {
    my ($self, $order_id) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT o.*, c.first_name, c.last_name, u.email 
         FROM orders o 
         LEFT JOIN customers c ON o.customer_id = c.id 
         LEFT JOIN users u ON c.user_id = u.id 
         WHERE o.id = ?"
    );
    $sth->execute($order_id);
    my $order = $sth->fetchrow_hashref();
    $sth->finish();
    $dbh->disconnect();
    
    return $order;
}

sub get_order_items {
    my ($self, $order_id) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT * FROM order_items WHERE order_id = ? ORDER BY id"
    );
    $sth->execute($order_id);
    my $items = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $items;
}

sub update_order_status {
    my ($self, $order_id, $status) = @_;
    
    my $dbh = $self->{db}->connect();
    $dbh->do(
        "UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        undef,
        $status, $order_id
    );
    $dbh->disconnect();
    
    return {success => 1};
}

sub delete_order {
    my ($self, $order_id) = @_;
    
    my $dbh = $self->{db}->connect();
    
    # First delete order items
    $dbh->do("DELETE FROM order_items WHERE order_id = ?", undef, $order_id);
    
    # Then delete the order
    $dbh->do("DELETE FROM orders WHERE id = ?", undef, $order_id);
    
    $dbh->disconnect();
    
    return {success => 1, message => 'Order deleted successfully'};
}

sub get_orders_by_customer {
    my ($self, $customer_id) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT * FROM orders WHERE customer_id = ? ORDER BY created_at DESC"
    );
    $sth->execute($customer_id);
    my $orders = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $orders;
}

sub get_orders_by_status {
    my ($self, $status) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT o.*, c.first_name, c.last_name 
         FROM orders o 
         LEFT JOIN customers c ON o.customer_id = c.id 
         WHERE o.status = ? 
         ORDER BY o.created_at DESC"
    );
    $sth->execute($status);
    my $orders = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $orders;
}

sub get_recent_orders {
    my ($self, $limit) = @_;
    
    $limit //= 10;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT o.*, c.first_name, c.last_name 
         FROM orders o 
         LEFT JOIN customers c ON o.customer_id = c.id 
         ORDER BY o.created_at DESC 
         LIMIT ?"
    );
    $sth->execute($limit);
    my $orders = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $orders;
}

sub get_order_stats {
    my $self = shift;
    
    my $dbh = $self->{db}->connect();
    
    my $stats = {};
    
    # Total revenue
    my ($total_revenue) = $dbh->selectrow_array(
        "SELECT COALESCE(SUM(total), 0) FROM orders WHERE status != 'cancelled'"
    );
    $stats->{total_revenue} = $total_revenue;
    
    # Total orders (exclude delivered, cancelled, refunded)
    my ($total_orders) = $dbh->selectrow_array(
        "SELECT COUNT(*) FROM orders WHERE status NOT IN ('delivered', 'cancelled', 'refunded')"
    );
    $stats->{total_orders} = $total_orders;
    
    # Orders by status
    my $sth = $dbh->prepare("SELECT status, COUNT(*) as count FROM orders GROUP BY status");
    $sth->execute();
    my $status_counts = $sth->fetchall_hashref('status');
    $stats->{by_status} = $status_counts;
    
    # Average order value
    my ($avg_order) = $dbh->selectrow_array(
        "SELECT COALESCE(AVG(total), 0) FROM orders WHERE status != 'cancelled'"
    );
    $stats->{average_order_value} = $avg_order;
    
    $dbh->disconnect();
    
    return $stats;
}

sub search_orders {
    my ($self, $search_term) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT o.*, c.first_name, c.last_name 
         FROM orders o 
         LEFT JOIN customers c ON o.customer_id = c.id 
         WHERE o.order_number LIKE ? OR c.first_name LIKE ? OR c.last_name LIKE ? 
         ORDER BY o.created_at DESC"
    );
    my $pattern = "%$search_term%";
    $sth->execute($pattern, $pattern, $pattern);
    my $orders = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $orders;
}

1;

__END__

=head1 NAME

ECommerce::Models::Order - Order model for order processing

=head1 SYNOPSIS

    use ECommerce::Models::Order;
    
    my $order_model = ECommerce::Models::Order->new();
    my $result = $order_model->create_order_from_cart($customer_id, $cart, \%params);
    my $orders = $order_model->get_all_orders();
    my $order = $order_model->get_order_by_id(1);

=head1 DESCRIPTION

This module provides order management functionality including order creation,
status tracking, and order analytics.

=head1 METHODS

=head2 new()

Creates a new Order model instance.

=head2 generate_order_number()

Generates a unique order number.

=head2 create_order(%params)

Creates a new order with items.

=head2 create_order_from_cart($customer_id, $cart, $params)

Creates an order from shopping cart items.

=head2 get_all_orders()

Returns all orders with customer information.

=head2 get_order_by_id($order_id)

Retrieves an order by ID.

=head2 get_order_items($order_id)

Returns all items for an order.

=head2 update_order_status($order_id, $status)

Updates order status.

=head2 get_orders_by_customer($customer_id)

Returns all orders for a customer.

=head2 get_orders_by_status($status)

Returns orders with specific status.

=head2 get_recent_orders($limit)

Returns recent orders.

=head2 get_order_stats()

Returns order statistics.

=head2 search_orders($search_term)

Searches orders by order number or customer name.

=head1 AUTHOR

E-Commerce System Team

=cut
