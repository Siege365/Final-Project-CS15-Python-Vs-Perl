package ECommerce::Controllers::Admin::ProductController;

use strict;
use warnings;
use ECommerce::Models::Product;
use ECommerce::Database;

sub new {
    my $class = shift;
    return bless {}, $class;
}

sub list_products {
    my ($self, $c) = @_;
    
    my $product_model = ECommerce::Models::Product->new();
    
    my $search = $c->param('search') // '';
    my $category = $c->param('category') // '';
    my $sort = $c->param('sort') // '';
    my $page = $c->param('page') // 1;
    my $per_page = 10;
    
    my $products;
    if ($search) {
        $products = $product_model->search_products($search);
    } elsif ($category) {
        $products = $product_model->get_products_by_category($category);
    } else {
        $products = $product_model->get_all_products();
    }
    
    # Sort products
    if ($sort eq 'in_stock') {
        $products = [sort { ($b->{is_active} && $b->{stock_quantity} >= 15) <=> ($a->{is_active} && $a->{stock_quantity} >= 15) } @$products];
    } elsif ($sort eq 'low_stock') {
        $products = [sort { 
            my $a_low = $a->{is_active} && $a->{stock_quantity} > 0 && $a->{stock_quantity} < 15;
            my $b_low = $b->{is_active} && $b->{stock_quantity} > 0 && $b->{stock_quantity} < 15;
            $b_low <=> $a_low;
        } @$products];
    } elsif ($sort eq 'out_of_stock') {
        $products = [sort { ($b->{stock_quantity} == 0 || !$b->{is_active}) <=> ($a->{stock_quantity} == 0 || !$a->{is_active}) } @$products];
    } else {
        $products = [sort { $a->{id} <=> $b->{id} } @$products];
    }
    
    my $categories = $product_model->get_categories();
    
    # Pagination
    my $total = scalar @$products;
    my $total_pages = int(($total + $per_page - 1) / $per_page);
    my $offset = ($page - 1) * $per_page;
    $products = [@$products[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
    
    $c->stash(
        products => $products, 
        categories => $categories,
        page => $page,
        total_pages => $total_pages,
        sort => $sort
    );
    $c->render(template => 'admin/products_admin');
}

sub show_add_form {
    my ($self, $c) = @_;
    
    my $product_model = ECommerce::Models::Product->new();
    my $categories = $product_model->get_categories();
    
    $c->stash(categories => $categories);
    $c->render(template => 'admin/product_add');
}

sub create_product {
    my ($self, $c) = @_;
    
    my $product_model = ECommerce::Models::Product->new();
    
    # Auto-generate SKU based on category
    my $category = $c->param('category');
    my %category_prefixes = (
        'Electronics' => 'ELEC',
        'Clothing' => 'CLTH',
        'Books' => 'BOOK',
        'Home & Garden' => 'HOME',
        'Sports' => 'SPRT',
        'Toys' => 'TOYS',
        'Food' => 'FOOD',
        'Beauty' => 'BEAU'
    );
    
    my $prefix = $category_prefixes{$category} || uc(substr($category, 0, 4));
    
    # Generate unique SKU with retry logic
    my $dbh = ECommerce::Database->new()->connect();
    my $sku;
    my $max_attempts = 100;
    my $attempt = 0;
    
    while ($attempt < $max_attempts) {
        my $sth = $dbh->prepare("SELECT sku FROM products WHERE sku LIKE ? ORDER BY sku DESC");
        $sth->execute("$prefix%");
        
        my $next_number = 1;
        my @existing_numbers;
        
        while (my $row = $sth->fetchrow_hashref()) {
            if ($row->{sku} =~ /^$prefix(\d+)$/) {
                push @existing_numbers, int($1);
            }
        }
        $sth->finish();
        
        if (@existing_numbers) {
            $next_number = (sort { $b <=> $a } @existing_numbers)[0] + 1;
        }
        
        $sku = sprintf("%s%03d", $prefix, $next_number);
        
        my $check_sth = $dbh->prepare("SELECT COUNT(*) FROM products WHERE sku = ?");
        $check_sth->execute($sku);
        my ($count) = $check_sth->fetchrow_array();
        $check_sth->finish();
        
        if ($count == 0) {
            last;
        }
        
        $attempt++;
    }
    
    $dbh->disconnect();
    
    if ($attempt >= $max_attempts) {
        $c->flash(error => 'Failed to generate unique SKU. Please try again.');
        return $c->redirect_to('/products/add');
    }
    
    my $result = $product_model->create_product(
        name => $c->param('name'),
        description => $c->param('description'),
        sku => $sku,
        category => $category,
        price => $c->param('price'),
        cost => $c->param('cost'),
        stock_quantity => $c->param('stock_quantity'),
        reorder_level => $c->param('reorder_level'),
        image_url => $c->param('image_url')
    );
    
    if ($result->{success}) {
        $c->flash(success => 'Product added successfully');
        $c->redirect_to('/products');
    } else {
        $c->flash(error => $result->{message});
        $c->redirect_to('/products/add');
    }
}

sub show_edit_form {
    my ($self, $c) = @_;
    
    my $id = $c->param('id');
    my $product_model = ECommerce::Models::Product->new();
    my $product = $product_model->get_product_by_id($id);
    my $categories = $product_model->get_categories();
    
    $c->stash(product => $product, categories => $categories);
    $c->render(template => 'admin/product_edit');
}

sub update_product {
    my ($self, $c) = @_;
    
    my $id = $c->param('id');
    my $product_model = ECommerce::Models::Product->new();
    
    my $result = $product_model->update_product(
        $id,
        name => $c->param('name'),
        description => $c->param('description'),
        sku => $c->param('sku'),
        category => $c->param('category'),
        price => $c->param('price'),
        cost => $c->param('cost'),
        stock_quantity => $c->param('stock_quantity'),
        reorder_level => $c->param('reorder_level'),
        image_url => $c->param('image_url'),
        is_active => $c->param('is_active')
    );
    
    if ($result->{success}) {
        $c->flash(success => 'Product updated successfully');
        $c->redirect_to('/products');
    } else {
        $c->flash(error => $result->{message});
        $c->redirect_to("/products/$id/edit");
    }
}

sub delete_product {
    my ($self, $c) = @_;
    
    my $id = $c->param('id');
    my $product_model = ECommerce::Models::Product->new();
    
    my $result = $product_model->delete_product($id);
    
    if ($result->{success}) {
        $c->flash(success => 'Product deleted successfully');
    } else {
        $c->flash(error => $result->{message});
    }
    $c->redirect_to('/products');
}

1;
