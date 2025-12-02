package ECommerce::Database;

# Database Module
# Handles database initialization, connections, and schema creation

use strict;
use warnings;
use utf8;
use DBI;
use File::Path qw(make_path);
use File::Basename;
use ECommerce::Config;

sub new {
    my $class = shift;
    my $self = {
        db_path => $ECommerce::Config::DB_PATH,
    };
    return bless $self, $class;
}

sub connect {
    my $self = shift;
    
    # Ensure data directory exists
    my $dir = dirname($self->{db_path});
    make_path($dir) unless -d $dir;
    
    my $dbh = DBI->connect(
        "dbi:SQLite:dbname=$self->{db_path}",
        "", "",
        {
            RaiseError => 1,
            AutoCommit => 1,
            sqlite_unicode => 1,
        }
    ) or die "Cannot connect to database: $DBI::errstr";
    
    return $dbh;
}

sub initialize_database {
    my $self = shift;
    
    my $dbh = $self->connect();
    
    # Enable foreign keys
    $dbh->do("PRAGMA foreign_keys = ON");
    
    # Create tables
    $self->create_tables($dbh);
    
    # Check if we need to populate sample data
    my $count = $dbh->selectrow_array("SELECT COUNT(*) FROM users");
    if ($count == 0) {
        $self->create_sample_data($dbh);
        print "Database initialized with sample data.\n";
    }
    
    $dbh->disconnect();
}

sub create_tables {
    my ($self, $dbh) = @_;
    
    # Users table
    $dbh->do(qq{
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'customer',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_login TEXT,
            is_active INTEGER DEFAULT 1
        )
    });
    
    # Customers table
    $dbh->do(qq{
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT DEFAULT 'USA',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    });
    
    # Products table
    $dbh->do(qq{
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            sku TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            cost REAL,
            stock_quantity INTEGER DEFAULT 0,
            reorder_level INTEGER DEFAULT 10,
            image_url TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    });
    
    # Orders table
    $dbh->do(qq{
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            customer_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            subtotal REAL NOT NULL,
            tax REAL DEFAULT 0,
            shipping REAL DEFAULT 0,
            total REAL NOT NULL,
            payment_method TEXT,
            payment_status TEXT DEFAULT 'pending',
            shipping_address TEXT,
            billing_address TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    });
    
    # Order items table
    $dbh->do(qq{
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            product_sku TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    });
    
    # Inventory transactions table
    $dbh->do(qq{
        CREATE TABLE IF NOT EXISTS inventory_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity_change INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            reference_id INTEGER,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    });
}

sub create_sample_data {
    my ($self, $dbh) = @_;
    
    use Crypt::Bcrypt qw(bcrypt);
    use Digest::SHA qw(sha256);
    
    # Create default users
    my @users = (
        {username => 'admin', email => 'admin@example.com', password => 'admin123', role => 'admin'},
        {username => 'staff', email => 'staff@example.com', password => 'staff123', role => 'staff'},
        {username => 'customer', email => 'customer@example.com', password => 'customer123', role => 'customer'},
    );
    
    foreach my $user (@users) {
        # Generate a random salt
        my $salt = join('', map { chr(int(rand(256))) } 1..16);
        my $password_hash = bcrypt($user->{password}, '2b', 10, $salt);
        $dbh->do(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            undef,
            $user->{username}, $user->{email}, $password_hash, $user->{role}
        );
    }
    
    # Create sample customers
    my @customers = (
        {user_id => 3, first_name => 'John', last_name => 'Doe', phone => '555-0101', 
         address => '123 Main St', city => 'New York', state => 'NY', zip_code => '10001'},
        {user_id => undef, first_name => 'Jane', last_name => 'Smith', phone => '555-0102',
         address => '456 Oak Ave', city => 'Los Angeles', state => 'CA', zip_code => '90001'},
        {user_id => undef, first_name => 'Bob', last_name => 'Johnson', phone => '555-0103',
         address => '789 Pine Rd', city => 'Chicago', state => 'IL', zip_code => '60601'},
        {user_id => undef, first_name => 'Alice', last_name => 'Williams', phone => '555-0104',
         address => '321 Elm St', city => 'Houston', state => 'TX', zip_code => '77001'},
        {user_id => undef, first_name => 'Charlie', last_name => 'Brown', phone => '555-0105',
         address => '654 Maple Dr', city => 'Phoenix', state => 'AZ', zip_code => '85001'},
    );
    
    foreach my $customer (@customers) {
        $dbh->do(
            "INSERT INTO customers (user_id, first_name, last_name, phone, address, city, state, zip_code) 
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            undef,
            $customer->{user_id}, $customer->{first_name}, $customer->{last_name}, $customer->{phone},
            $customer->{address}, $customer->{city}, $customer->{state}, $customer->{zip_code}
        );
    }
    
    # Create sample products
    my @products = (
        {name => 'Laptop Pro 15"', description => 'High-performance laptop', sku => 'ELEC001', 
         category => 'Electronics', price => 1299.99, cost => 800.00, stock => 25},
        {name => 'Wireless Mouse', description => 'Ergonomic wireless mouse', sku => 'ELEC002',
         category => 'Electronics', price => 29.99, cost => 15.00, stock => 100},
        {name => 'Mechanical Keyboard', description => 'RGB mechanical keyboard', sku => 'ELEC003',
         category => 'Electronics', price => 89.99, cost => 45.00, stock => 50},
        {name => 'USB-C Hub', description => '7-in-1 USB-C hub', sku => 'ELEC004',
         category => 'Electronics', price => 49.99, cost => 25.00, stock => 75},
        {name => 'Webcam HD', description => '1080p HD webcam', sku => 'ELEC005',
         category => 'Electronics', price => 79.99, cost => 40.00, stock => 40},
        {name => 'T-Shirt Classic', description => 'Cotton t-shirt', sku => 'CLTH001',
         category => 'Clothing', price => 19.99, cost => 8.00, stock => 200},
        {name => 'Jeans Denim', description => 'Classic denim jeans', sku => 'CLTH002',
         category => 'Clothing', price => 59.99, cost => 30.00, stock => 150},
        {name => 'Hoodie Comfort', description => 'Comfortable hoodie', sku => 'CLTH003',
         category => 'Clothing', price => 45.99, cost => 22.00, stock => 80},
        {name => 'Programming Book', description => 'Learn Perl programming', sku => 'BOOK001',
         category => 'Books', price => 39.99, cost => 20.00, stock => 30},
        {name => 'Cookbook Deluxe', description => 'Professional cookbook', sku => 'BOOK002',
         category => 'Books', price => 29.99, cost => 15.00, stock => 45},
        {name => 'Coffee Maker', description => 'Automatic coffee maker', sku => 'HOME001',
         category => 'Home', price => 89.99, cost => 50.00, stock => 35},
        {name => 'Blender Pro', description => 'High-speed blender', sku => 'HOME002',
         category => 'Home', price => 69.99, cost => 35.00, stock => 40},
        {name => 'Yoga Mat', description => 'Non-slip yoga mat', sku => 'SPRT001',
         category => 'Sports', price => 24.99, cost => 12.00, stock => 60},
        {name => 'Dumbbells Set', description => '10kg dumbbell set', sku => 'SPRT002',
         category => 'Sports', price => 49.99, cost => 25.00, stock => 30},
        {name => 'Board Game Classic', description => 'Family board game', sku => 'TOYS001',
         category => 'Toys', price => 34.99, cost => 18.00, stock => 50},
        {name => 'Puzzle 1000pc', description => '1000-piece puzzle', sku => 'TOYS002',
         category => 'Toys', price => 19.99, cost => 10.00, stock => 70},
        {name => 'Shampoo Premium', description => 'Professional shampoo', sku => 'BEAU001',
         category => 'Beauty', price => 14.99, cost => 7.00, stock => 120},
        {name => 'Face Cream', description => 'Moisturizing face cream', sku => 'BEAU002',
         category => 'Beauty', price => 24.99, cost => 12.00, stock => 90},
        {name => 'Car Phone Mount', description => 'Universal phone mount', sku => 'AUTO001',
         category => 'Automotive', price => 15.99, cost => 8.00, stock => 100},
        {name => 'Tire Pressure Gauge', description => 'Digital tire gauge', sku => 'AUTO002',
         category => 'Automotive', price => 12.99, cost => 6.00, stock => 85},
    );
    
    foreach my $product (@products) {
        $dbh->do(
            "INSERT INTO products (name, description, sku, category, price, cost, stock_quantity) 
             VALUES (?, ?, ?, ?, ?, ?, ?)",
            undef,
            $product->{name}, $product->{description}, $product->{sku}, $product->{category},
            $product->{price}, $product->{cost}, $product->{stock}
        );
    }
}

1;

__END__

=head1 NAME

ECommerce::Database - Database management module

=head1 SYNOPSIS

    use ECommerce::Database;
    
    my $db = ECommerce::Database->new();
    $db->initialize_database();
    
    my $dbh = $db->connect();

=head1 DESCRIPTION

This module handles all database operations including initialization,
schema creation, and sample data generation.

=head1 METHODS

=head2 new()

Creates a new Database object.

=head2 connect()

Establishes and returns a database connection.

=head2 initialize_database()

Initializes the database with tables and sample data if needed.

=head2 create_tables($dbh)

Creates all required database tables.

=head2 create_sample_data($dbh)

Populates database with sample users, customers, and products.

=head1 AUTHOR

E-Commerce System Team

=cut
