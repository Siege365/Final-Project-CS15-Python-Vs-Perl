package ECommerce::Controllers::Customer::CartController;

use strict;
use warnings;
use ECommerce::Models::Product;
use ECommerce::Models::Customer;

sub new {
    my $class = shift;
    return bless {}, $class;
}

sub view_cart {
    my ($self, $c) = @_;
    
    my $cart = $c->get_cart();
    
    # Fetch customer's address
    my $customer_id = $c->session('customer_id');
    my $customer_address = '';
    
    if ($customer_id) {
        my $customer_model = ECommerce::Models::Customer->new();
        my $customer = $customer_model->get_customer_by_id($customer_id);
        $customer_address = $customer->{address} if $customer;
    }
    
    $c->stash(cart => $cart, customer_address => $customer_address);
    $c->render(template => 'customer/cart');
}

sub add_to_cart {
    my ($self, $c) = @_;
    
    my $product_id = $c->param('product_id');
    my $quantity = $c->param('quantity') // 1;
    
    my $product_model = ECommerce::Models::Product->new();
    my $product = $product_model->get_product_by_id($product_id);
    
    if ($product) {
        my $cart = $c->session('cart') // [];
        my $found = 0;
        
        foreach my $item (@$cart) {
            if ($item->{product_id} eq $product_id) {
                $item->{quantity} += $quantity;
                $found = 1;
                last;
            }
        }
        
        unless ($found) {
            push @$cart, {
                product_id => $product_id,
                name => $product->{name},
                price => $product->{price},
                quantity => $quantity
            };
        }
        
        $c->session(cart => $cart);
        $c->flash(success => 'Product added to cart!');
    }
    
    $c->redirect_to('/products');
}

sub remove_from_cart {
    my ($self, $c) = @_;
    
    my $product_id = $c->param('product_id');
    my $cart = $c->session('cart') // [];
    
    # Filter out the product to remove
    $cart = [grep { $_->{product_id} ne $product_id } @$cart];
    
    $c->session(cart => $cart);
    $c->flash(success => 'Product removed from cart');
    $c->redirect_to('/cart');
}

1;
