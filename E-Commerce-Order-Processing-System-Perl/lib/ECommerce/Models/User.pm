package ECommerce::Models::User;

# User Model
# Handles all user-related database operations

use strict;
use warnings;
use utf8;
use ECommerce::Database;
use Crypt::Bcrypt qw(bcrypt bcrypt_check);

sub new {
    my $class = shift;
    my $self = {
        db => ECommerce::Database->new(),
    };
    return bless $self, $class;
}

sub create_user {
    my ($self, $username, $email, $password, $role) = @_;
    
    $role //= 'customer';
    # Generate random salt
    my $salt = join('', map { chr(int(rand(256))) } 1..16);
    my $password_hash = bcrypt($password, '2b', 10, $salt);
    
    my $dbh = $self->{db}->connect();
    
    eval {
        $dbh->do(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            undef,
            $username, $email, $password_hash, $role
        );
    };
    
    if ($@) {
        $dbh->disconnect();
        return {success => 0, message => "Failed to create user: $@"};
    }
    
    my $user_id = $dbh->last_insert_id(undef, undef, 'users', 'id');
    $dbh->disconnect();
    
    return {success => 1, user_id => $user_id};
}

sub get_user_by_username {
    my ($self, $username) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare("SELECT * FROM users WHERE username = ?");
    $sth->execute($username);
    my $user = $sth->fetchrow_hashref();
    $dbh->disconnect();
    
    return $user;
}

sub get_user_by_id {
    my ($self, $user_id) = @_;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare("SELECT * FROM users WHERE id = ?");
    $sth->execute($user_id);
    my $user = $sth->fetchrow_hashref();
    $dbh->disconnect();
    
    return $user;
}

sub verify_password {
    my ($self, $username, $password) = @_;
    
    my $user = $self->get_user_by_username($username);
    return 0 unless $user;
    
    return bcrypt_check($password, $user->{password_hash});
}

sub update_last_login {
    my ($self, $user_id) = @_;
    
    my $dbh = $self->{db}->connect();
    $dbh->do(
        "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
        undef,
        $user_id
    );
    $dbh->disconnect();
}

sub get_all_users {
    my $self = shift;
    
    my $dbh = $self->{db}->connect();
    my $sth = $dbh->prepare("SELECT id, username, email, role, created_at, last_login, is_active FROM users ORDER BY created_at DESC");
    $sth->execute();
    my $users = $sth->fetchall_arrayref({});
    $dbh->disconnect();
    
    return $users;
}

sub update_user_role {
    my ($self, $user_id, $new_role) = @_;
    
    my $dbh = $self->{db}->connect();
    $dbh->do(
        "UPDATE users SET role = ? WHERE id = ?",
        undef,
        $new_role, $user_id
    );
    $dbh->disconnect();
    
    return {success => 1};
}

sub deactivate_user {
    my ($self, $user_id) = @_;
    
    my $dbh = $self->{db}->connect();
    $dbh->do(
        "UPDATE users SET is_active = 0 WHERE id = ?",
        undef,
        $user_id
    );
    $dbh->disconnect();
    
    return {success => 1};
}

1;

__END__

=head1 NAME

ECommerce::Models::User - User model for authentication and user management

=head1 SYNOPSIS

    use ECommerce::Models::User;
    
    my $user_model = ECommerce::Models::User->new();
    my $result = $user_model->create_user('username', 'email@example.com', 'password', 'customer');
    my $user = $user_model->get_user_by_username('username');
    my $valid = $user_model->verify_password('username', 'password');

=head1 DESCRIPTION

This module provides user management functionality including user creation,
authentication, and role management.

=head1 METHODS

=head2 new()

Creates a new User model instance.

=head2 create_user($username, $email, $password, $role)

Creates a new user with bcrypt password hashing.

=head2 get_user_by_username($username)

Retrieves a user by username.

=head2 get_user_by_id($user_id)

Retrieves a user by ID.

=head2 verify_password($username, $password)

Verifies a password against the stored hash.

=head2 update_last_login($user_id)

Updates the last login timestamp.

=head2 get_all_users()

Returns all users.

=head2 update_user_role($user_id, $new_role)

Updates a user's role.

=head2 deactivate_user($user_id)

Deactivates a user account.

=head1 AUTHOR

E-Commerce System Team

=cut
