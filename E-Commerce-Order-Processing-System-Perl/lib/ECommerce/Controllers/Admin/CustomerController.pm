package ECommerce::Controllers::Admin::CustomerController;

use strict;
use warnings;
use ECommerce::Models::Customer;

sub new {
    my $class = shift;
    return bless {}, $class;
}

sub list_customers {
    my ($self, $c) = @_;
    
    my $customer_model = ECommerce::Models::Customer->new();
    my $customers = $customer_model->get_all_customers();
    
    my $sort = $c->param('sort') // '';
    my $search = $c->param('search') // '';
    my $page = $c->param('page') // 1;
    my $per_page = 10;
    
    # Search filter
    if ($search) {
        $customers = [grep {
            (lc($_->{username} // '') =~ /\Q$search\E/i) ||
            (lc($_->{email} // '') =~ /\Q$search\E/i) ||
            (lc($_->{first_name} // '') =~ /\Q$search\E/i) ||
            (lc($_->{last_name} // '') =~ /\Q$search\E/i) ||
            (lc($_->{phone} // '') =~ /\Q$search\E/i) ||
            (lc($_->{address} // '') =~ /\Q$search\E/i)
        } @$customers];
    }
    
    # Sort customers
    if ($sort eq 'recent') {
        $customers = [sort { $b->{id} <=> $a->{id} } @$customers];
    } elsif ($sort eq 'inactive') {
        $customers = [sort { !$a->{is_active} <=> !$b->{is_active} } @$customers];
    } elsif ($sort eq 'all') {
        # Keep original order
    } else {
        $customers = [sort { $a->{id} <=> $b->{id} } @$customers];
    }
    
    # Pagination
    my $total = scalar @$customers;
    my $total_pages = int(($total + $per_page - 1) / $per_page);
    my $offset = ($page - 1) * $per_page;
    $customers = [@$customers[$offset .. ($offset + $per_page - 1 > $total - 1 ? $total - 1 : $offset + $per_page - 1)]];
    
    $c->stash(
        customers => $customers,
        page => $page,
        total_pages => $total_pages,
        sort => $sort,
        search => $search
    );
    $c->render(template => 'admin/customers');
}

sub delete_customer {
    my ($self, $c) = @_;
    
    my $id = $c->param('id');
    my $customer_model = ECommerce::Models::Customer->new();
    
    my $result = $customer_model->delete_customer($id);
    
    if ($result->{success}) {
        $c->flash(success => 'Customer deleted successfully');
    } else {
        $c->flash(error => $result->{message});
    }
    $c->redirect_to('/customers');
}

1;
