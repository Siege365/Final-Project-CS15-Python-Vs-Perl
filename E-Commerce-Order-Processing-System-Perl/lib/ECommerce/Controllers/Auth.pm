package ECommerce::Controllers::Auth;

# Authentication Controller
# Handles login, logout, registration, and authorization

use strict;
use warnings;
use utf8;
use ECommerce::Models::User;
use ECommerce::Models::Customer;

sub new {
    my $class = shift;
    my $self = {
        user_model => ECommerce::Models::User->new(),
        customer_model => ECommerce::Models::Customer->new(),
    };
    return bless $self, $class;
}

sub login {
    my ($self, $username, $password) = @_;
    
    return undef unless $username && $password;
    
    my $user = $self->{user_model}->get_user_by_username($username);
    return undef unless $user;
    return undef unless $user->{is_active};
    
    my $valid = $self->{user_model}->verify_password($username, $password);
    return undef unless $valid;
    
    # Update last login
    $self->{user_model}->update_last_login($user->{id});
    
    # Get customer_id if role is customer
    my $customer_id = undef;
    if ($user->{role} eq 'customer') {
        my $customer = $self->{customer_model}->get_customer_by_user_id($user->{id});
        $customer_id = $customer->{id} if $customer;
    }
    
    return {
        id => $user->{id},
        username => $user->{username},
        email => $user->{email},
        role => $user->{role},
        customer_id => $customer_id,
    };
}

sub register {
    my ($self, $username, $email, $password, $role, $phone, $address, $first_name, $last_name) = @_;
    
    # Validate input
    return {success => 0, message => 'Username is required'} unless $username;
    return {success => 0, message => 'Email is required'} unless $email;
    return {success => 0, message => 'Password is required'} unless $password;
    return {success => 0, message => 'Password must be at least 6 characters'} if length($password) < 6;
    
    # Check if username already exists
    my $existing_user = $self->{user_model}->get_user_by_username($username);
    return {success => 0, message => 'Username already exists'} if $existing_user;
    
    # Create user
    my $result = $self->{user_model}->create_user($username, $email, $password, $role // 'customer');
    
    # If user creation successful and role is customer, create customer record
    if ($result->{success} && ($role // 'customer') eq 'customer') {
        my $customer_result = $self->{customer_model}->create_customer(
            user_id => $result->{user_id},
            first_name => $first_name || $username,
            last_name => $last_name || '',
            phone => $phone // '',
            address => $address // ''
        );
        
        unless ($customer_result->{success}) {
            return {success => 0, message => 'User created but failed to create customer profile'};
        }
    }
    
    return $result;
}

sub is_admin {
    my ($self, $role) = @_;
    return ($role // '') eq 'admin';
}

sub is_staff {
    my ($self, $role) = @_;
    return ($role // '') eq 'staff' || ($role // '') eq 'admin';
}

sub is_customer {
    my ($self, $role) = @_;
    return ($role // '') eq 'customer';
}

1;

__END__

=head1 NAME

ECommerce::Controllers::Auth - Authentication and authorization controller

=head1 SYNOPSIS

    use ECommerce::Controllers::Auth;
    
    my $auth = ECommerce::Controllers::Auth->new();
    my $user = $auth->login('username', 'password');
    my $result = $auth->register('username', 'email@example.com', 'password', 'customer');

=head1 DESCRIPTION

This controller handles user authentication (login/logout) and registration,
as well as role-based access control.

=head1 METHODS

=head2 new()

Creates a new Auth controller instance.

=head2 login($username, $password)

Authenticates a user and returns user data on success.

=head2 register($username, $email, $password, $role)

Registers a new user.

=head2 is_admin($role)

Checks if role is admin.

=head2 is_staff($role)

Checks if role is staff or admin.

=head2 is_customer($role)

Checks if role is customer.

=head1 AUTHOR

E-Commerce System Team

=cut
