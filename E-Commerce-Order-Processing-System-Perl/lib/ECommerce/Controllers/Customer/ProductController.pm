package ECommerce::Controllers::Customer::ProductController;

use strict;
use warnings;
use ECommerce::Models::Product;

sub new {
    my $class = shift;
    return bless {}, $class;
}

sub list_products {
    my ($self, $c) = @_;
    
    my $product_model = ECommerce::Models::Product->new();
    
    my $search = $c->param('search') // '';
    my $category = $c->param('category') // '';
    my $per_page = 10;
    
    my $products;
    if ($search) {
        $products = $product_model->search_products($search);
    } elsif ($category) {
        $products = $product_model->get_products_by_category($category);
    } else {
        $products = $product_model->get_all_products();
    }
    
    $products = [sort { $a->{id} <=> $b->{id} } @$products];
    
    my $categories = $product_model->get_categories();
    
    # Initial load only (infinite scroll handles rest)
    my $total = scalar @$products;
    my $offset = 0;
    $products = [@$products[$offset .. ($per_page - 1 > $total - 1 ? $total - 1 : $per_page - 1)]];
    
    $c->stash(
        products => $products,
        categories => $categories,
        search => $search,
        category => $category
    );
    $c->render(template => 'customer/products_customer');
}

1;
