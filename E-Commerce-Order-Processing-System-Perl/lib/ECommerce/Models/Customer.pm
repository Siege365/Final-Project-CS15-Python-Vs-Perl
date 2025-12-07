package ECommerce::Models::Customer;

# Customer Model
# Handles all customer-related database operations

use strict;
use warnings;
use utf8;
use ECommerce::Database;

sub new {
    my $class = shift;
    my $self = {
        db => ECommerce::Database->new(),
    };
    return bless $self, $class;
}

sub create_customer {
    my ($self, %params) = @_;
    
    my $dbh = $self->{db}->connect();
    
    eval {
        $dbh->do(
            "INSERT INTO customers (user_id, first_name, last_name, phone, address, city, state, zip_code, country) 
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            undef,
            $params{user_id}, $params{first_name}, $params{last_name}, $params{phone},
            $params{address}, $params{city}, $params{state}, $params{zip_code}, $params{country} // 'USA'
        );
    };
    
    if ($@) {
        $dbh->disconnect();
        return {success => 0, message => "Failed to create customer: $@"};
    }
    
    my $customer_id = $dbh->last_insert_id(undef, undef, 'customers', 'id');
    $dbh->disconnect();
    
    return {success => 1, customer_id => $customer_id};
}

sub get_all_customers {
    my $self = shift;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT c.*, u.username, u.email, u.is_active, u.created_at 
         FROM customers c 
         LEFT JOIN users u ON c.user_id = u.id 
         ORDER BY c.created_at DESC"
    );
    $sth->execute();
    my $customers = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $customers;
}

sub get_customer_by_id {
    my ($self, $customer_id) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT c.*, u.username, u.email 
         FROM customers c 
         LEFT JOIN users u ON c.user_id = u.id 
         WHERE c.id = ?"
    );
    $sth->execute($customer_id);
    my $customer = $sth->fetchrow_hashref();
    $sth->finish();
    $dbh->disconnect();
    
    return $customer;
}

sub get_customer_by_user_id {
    my ($self, $user_id) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare("SELECT * FROM customers WHERE user_id = ?");
    $sth->execute($user_id);
    my $customer = $sth->fetchrow_hashref();
    $sth->finish();
    $dbh->disconnect();
    
    return $customer;
}

sub update_customer {
    my ($self, $customer_id, %params) = @_;
    
    my @fields;
    my @values;
    
    foreach my $field (qw(first_name last_name phone address city state zip_code country)) {
        if (exists $params{$field}) {
            push @fields, "$field = ?";
            push @values, $params{$field};
        }
    }
    
    return {success => 0, message => 'No fields to update'} unless @fields;
    
    push @values, $customer_id;
    
    my $dbh = $self->{db}->connect();
    my $sql = "UPDATE customers SET " . join(', ', @fields) . " WHERE id = ?";
    $dbh->do($sql, undef, @values);
    $dbh->disconnect();
    
    return {success => 1};
}

sub delete_customer {
    my ($self, $customer_id) = @_;
    
    my $dbh = $self->{db}->connect();
    $dbh->do("DELETE FROM customers WHERE id = ?", undef, $customer_id);
    $dbh->disconnect();
    
    return {success => 1};
}

sub search_customers {
    my ($self, $search_term) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT c.*, u.username, u.email 
         FROM customers c 
         LEFT JOIN users u ON c.user_id = u.id 
         WHERE c.first_name LIKE ? OR c.last_name LIKE ? OR c.phone LIKE ? OR u.email LIKE ? 
         ORDER BY c.created_at DESC"
    );
    my $pattern = "%$search_term%";
    $sth->execute($pattern, $pattern, $pattern, $pattern);
    my $customers = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $customers;
}

sub get_customer_stats {
    my ($self, $customer_id) = @_;
    
    my $dbh = $self->{db}->connect();
    
    my $stats = {};
    
    # Total orders
    my ($total_orders) = $dbh->selectrow_array(
        "SELECT COUNT(*) FROM orders WHERE customer_id = ?",
        undef, $customer_id
    );
    $stats->{total_orders} = $total_orders;
    
    # Total spent
    my ($total_spent) = $dbh->selectrow_array(
        "SELECT COALESCE(SUM(total), 0) FROM orders WHERE customer_id = ? AND status != 'cancelled'",
        undef, $customer_id
    );
    $stats->{total_spent} = $total_spent;
    
    # Average order value
    my ($avg_order) = $dbh->selectrow_array(
        "SELECT COALESCE(AVG(total), 0) FROM orders WHERE customer_id = ? AND status != 'cancelled'",
        undef, $customer_id
    );
    $stats->{average_order_value} = $avg_order;
    
    # Last order date
    my ($last_order) = $dbh->selectrow_array(
        "SELECT created_at FROM orders WHERE customer_id = ? ORDER BY created_at DESC LIMIT 1",
        undef, $customer_id
    );
    $stats->{last_order_date} = $last_order;
    
    $dbh->disconnect();
    
    return $stats;
}

sub get_top_customers {
    my ($self, $limit) = @_;
    
    $limit //= 10;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT c.*, u.email, 
                COUNT(DISTINCT o.id) as order_count, 
                COALESCE(SUM(o.total), 0) as total_spent 
         FROM customers c 
         LEFT JOIN users u ON c.user_id = u.id 
         LEFT JOIN orders o ON c.id = o.customer_id AND o.status != 'cancelled' 
         GROUP BY c.id 
         ORDER BY total_spent DESC 
         LIMIT ?"
    );
    $sth->execute($limit);
    my $customers = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $customers;
}

1;

__END__

=head1 NAME

ECommerce::Models::Customer - Customer model for customer management

=head1 SYNOPSIS

    use ECommerce::Models::Customer;
    
    my $customer_model = ECommerce::Models::Customer->new();
    my $customers = $customer_model->get_all_customers();
    my $customer = $customer_model->get_customer_by_id(1);
    my $stats = $customer_model->get_customer_stats(1);

=head1 DESCRIPTION

This module provides customer management functionality including CRUD operations,
customer analytics, and customer search.

=head1 METHODS

=head2 new()

Creates a new Customer model instance.

=head2 create_customer(%params)

Creates a new customer.

=head2 get_all_customers()

Returns all customers with user information.

=head2 get_customer_by_id($customer_id)

Retrieves a customer by ID.

=head2 get_customer_by_user_id($user_id)

Retrieves a customer by user ID.

=head2 update_customer($customer_id, %params)

Updates customer information.

=head2 delete_customer($customer_id)

Deletes a customer.

=head2 search_customers($search_term)

Searches customers by name, phone, or email.

=head2 get_customer_stats($customer_id)

Returns statistics for a customer.

=head2 get_top_customers($limit)

Returns top customers by spending.

=head1 AUTHOR

E-Commerce System Team

=cut
