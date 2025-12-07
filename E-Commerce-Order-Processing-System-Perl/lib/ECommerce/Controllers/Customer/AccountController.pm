package ECommerce::Controllers::Customer::AccountController;

use strict;
use warnings;
use ECommerce::Models::Customer;
use ECommerce::Models::User;

sub new {
    my $class = shift;
    return bless {}, $class;
}

sub show_account {
    my ($self, $c) = @_;
    
    my $user_model = ECommerce::Models::User->new();
    my $customer_model = ECommerce::Models::Customer->new();
    
    my $user_id = $c->session('user_id');
    my $customer_id = $c->session('customer_id');
    
    my $user = $user_model->get_user_by_id($user_id);
    my $customer = $customer_id ? $customer_model->get_customer_by_id($customer_id) : undef;
    
    $c->stash(user => $user, customer => $customer);
    $c->render(template => 'customer/account');
}

sub update_account {
    my ($self, $c) = @_;
    
    my $phone = $c->param('phone');
    my $address = $c->param('address');
    my $first_name = $c->param('first_name');
    my $last_name = $c->param('last_name');
    
    my $customer_model = ECommerce::Models::Customer->new();
    my $customer_id = $c->session('customer_id');
    
    if ($customer_id) {
        $customer_model->update_customer($customer_id,
            first_name => $first_name,
            last_name => $last_name,
            phone => $phone,
            address => $address
        );
        $c->flash(success => 'Account updated successfully!');
    }
    
    $c->redirect_to('/account');
}

sub delete_account {
    my ($self, $c) = @_;
    
    my $user_model = ECommerce::Models::User->new();
    my $user_id = $c->session('user_id');
    
    # Deactivate user account
    $user_model->deactivate_user($user_id);
    
    # Log out the user
    $c->session(expires => 1);
    $c->flash(success => 'Your account has been deactivated');
    $c->redirect_to('/');
}

1;
