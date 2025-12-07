package ECommerce::Models::Product;

# Product Model
# Handles all product-related database operations

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

sub create_product {
    my ($self, %params) = @_;
    
    my $dbh = $self->{db}->connect();
    
    # Check for duplicate SKU
    my $sth = $dbh->prepare("SELECT id FROM products WHERE sku = ?");
    $sth->execute($params{sku});
    if ($sth->fetchrow_array()) {
        $sth->finish();
        $dbh->disconnect();
        return {success => 0, message => "Product with SKU '$params{sku}' already exists"};
    }
    $sth->finish();
    
    eval {
        $dbh->do(
            "INSERT INTO products (name, description, sku, category, price, cost, stock_quantity, reorder_level, image_url) 
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            undef,
            $params{name}, $params{description}, $params{sku}, $params{category},
            $params{price}, $params{cost} // 0, $params{stock_quantity} // 0,
            $params{reorder_level} // 10, $params{image_url} // ''
        );
    };
    
    if ($@) {
        $dbh->disconnect();
        return {success => 0, message => "Failed to create product: $@"};
    }
    
    my $product_id = $dbh->last_insert_id(undef, undef, 'products', 'id');
    $dbh->disconnect();
    
    return {success => 1, product_id => $product_id};
}

sub get_all_products {
    my ($self, $active_only) = @_;
    
    $active_only //= 1;
    
    my $dbh = $self->{db}->connect();
    my $sql = "SELECT * FROM products";
    $sql .= " WHERE is_active = 1" if $active_only;
    $sql .= " ORDER BY name";
    
    my $sth = $dbh->prepare($sql);
    $sth->execute();
    my $products = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $products;
}

sub get_product_by_id {
    my ($self, $product_id) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare("SELECT * FROM products WHERE id = ?");
    $sth->execute($product_id);
    my $product = $sth->fetchrow_hashref();
    $sth->finish();
    $dbh->disconnect();
    
    return $product;
}

sub get_product_by_sku {
    my ($self, $sku) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare("SELECT * FROM products WHERE sku = ?");
    $sth->execute($sku);
    my $product = $sth->fetchrow_hashref();
    $sth->finish();
    $dbh->disconnect();
    
    return $product;
}

sub update_product {
    my ($self, $product_id, %params) = @_;
    
    my $dbh = $self->{db}->connect();
    
    # Check for duplicate SKU if SKU is being updated
    if (exists $params{sku}) {
        my $sth = $dbh->prepare("SELECT id FROM products WHERE sku = ? AND id != ?");
        $sth->execute($params{sku}, $product_id);
        if ($sth->fetchrow_array()) {
            $sth->finish();
            $dbh->disconnect();
            return {success => 0, message => "Product with SKU '$params{sku}' already exists"};
        }
        $sth->finish();
    }
    
    my @fields;
    my @values;
    
    foreach my $field (qw(name description sku category price cost stock_quantity reorder_level image_url is_active)) {
        if (exists $params{$field}) {
            push @fields, "$field = ?";
            push @values, $params{$field};
        }
    }
    
    return {success => 0, message => 'No fields to update'} unless @fields;
    
    push @fields, "updated_at = CURRENT_TIMESTAMP";
    push @values, $product_id;
    
    my $dbh = $self->{db}->connect();
    my $sql = "UPDATE products SET " . join(', ', @fields) . " WHERE id = ?";
    $dbh->do($sql, undef, @values);
    $dbh->disconnect();
    
    return {success => 1};
}

sub delete_product {
    my ($self, $product_id) = @_;
    
    # Soft delete
    return $self->update_product($product_id, is_active => 0);
}

sub update_stock {
    my ($self, $product_id, $quantity_change, $transaction_type, $reference_id, $notes) = @_;
    
    my $dbh = $self->{db}->connect();
    
    $dbh->begin_work();
    
    eval {
        # Update product stock
        $dbh->do(
            "UPDATE products SET stock_quantity = stock_quantity + ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            undef,
            $quantity_change, $product_id
        );
        
        # Record transaction
        $dbh->do(
            "INSERT INTO inventory_transactions (product_id, quantity_change, transaction_type, reference_id, notes) 
             VALUES (?, ?, ?, ?, ?)",
            undef,
            $product_id, $quantity_change, $transaction_type, $reference_id, $notes
        );
        
        $dbh->commit();
    };
    
    if ($@) {
        $dbh->rollback();
        $dbh->disconnect();
        return {success => 0, message => "Failed to update stock: $@"};
    }
    
    $dbh->disconnect();
    return {success => 1};
}

sub get_low_stock_products {
    my $self = shift;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT * FROM products 
         WHERE is_active = 1 AND stock_quantity <= reorder_level 
         ORDER BY stock_quantity ASC"
    );
    $sth->execute();
    my $products = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $products;
}

sub search_products {
    my ($self, $search_term) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT * FROM products 
         WHERE is_active = 1 AND (name LIKE ? OR description LIKE ? OR sku LIKE ?) 
         ORDER BY name"
    );
    my $pattern = "%$search_term%";
    $sth->execute($pattern, $pattern, $pattern);
    my $products = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $products;
}

sub get_products_by_category {
    my ($self, $category) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT * FROM products 
         WHERE is_active = 1 AND category = ? 
         ORDER BY name"
    );
    $sth->execute($category);
    my $products = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return $products;
}

sub get_categories {
    my $self = shift;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare(
        "SELECT DISTINCT category FROM products 
         WHERE is_active = 1 
         ORDER BY category"
    );
    $sth->execute();
    my $categories = $sth->fetchall_arrayref({});
    $sth->finish();
    $dbh->disconnect();
    
    return [map { $_->{category} } @$categories];
}

1;

__END__

=head1 NAME

ECommerce::Models::Product - Product model for inventory management

=head1 SYNOPSIS

    use ECommerce::Models::Product;
    
    my $product_model = ECommerce::Models::Product->new();
    my $products = $product_model->get_all_products();
    my $product = $product_model->get_product_by_id(1);
    my $result = $product_model->update_stock(1, -5, 'sale', $order_id, 'Order fulfillment');

=head1 DESCRIPTION

This module provides product management functionality including CRUD operations,
inventory tracking, and product search.

=head1 METHODS

=head2 new()

Creates a new Product model instance.

=head2 create_product(%params)

Creates a new product.

=head2 get_all_products($active_only)

Returns all products, optionally filtered by active status.

=head2 get_product_by_id($product_id)

Retrieves a product by ID.

=head2 get_product_by_sku($sku)

Retrieves a product by SKU.

=head2 update_product($product_id, %params)

Updates product information.

=head2 delete_product($product_id)

Soft deletes a product.

=head2 update_stock($product_id, $quantity_change, $transaction_type, $reference_id, $notes)

Updates product stock and records transaction.

=head2 get_low_stock_products()

Returns products at or below reorder level.

=head2 search_products($search_term)

Searches products by name, description, or SKU.

=head2 get_products_by_category($category)

Returns products in a specific category.

=head2 get_categories()

Returns list of all product categories.

=head1 AUTHOR

E-Commerce System Team

=cut
