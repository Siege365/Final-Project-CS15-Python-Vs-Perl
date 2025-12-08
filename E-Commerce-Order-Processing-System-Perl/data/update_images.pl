#!/usr/bin/env perl
use strict;
use warnings;
use DBI;

my $db_path = "ecommerce.db";
my $dbh = DBI->connect("dbi:SQLite:dbname=$db_path", "", "", {
    RaiseError => 1,
    AutoCommit => 1,
}) or die "Cannot connect to database: $DBI::errstr";

# Define correct image URLs for each product based on actual product names
my %product_images = (
    # Electronics
    1  => 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop',  # Laptop Pro 15"
    2  => 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop',  # Wireless Mouse
    3  => 'https://www.popsci.com/wp-content/uploads/2022/02/12/mechanical-keyboard-with-rbg.jpg?quality=85',  # Mechanical Keyboard
    4  => 'https://m.media-amazon.com/images/I/513AvAPJgXL._AC_UF894,1000_QL80_.jpg',  # USB-C Hub
    5  => 'https://cdn.mos.cms.futurecdn.net/NeyiJFuPXVSzH5JRp5X8H5-1200-80.jpg',  # Webcam HD
    21 => 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',  # Orashare Headphones
    23 => 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=300&fit=crop',  # Orashare Headphones (different)
    
    # Clothing
    6  => 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop',  # T-Shirt Classic
    7  => 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=300&fit=crop',  # Jeans Denim
    8  => 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=300&fit=crop',  # Hoodie Comfort
    
    # Books
    9  => 'https://m.media-amazon.com/images/I/81YWUlX6J4L._AC_UF1000,1000_QL80_.jpg',  # Programming Book
    10 => 'https://www.lordandlion.com/cdn/shop/products/serendip.jpg?v=1627902766&width=1445',  # Cookbook Deluxe
    
    # Home
    11 => 'https://www.bhg.com/thmb/sog5eX8qb6bk4JIWdMnM4qAbQVo=/4000x0/filters:no_upscale():strip_icc()/bhg-product-mr-coffee-5-cup-mini-brew-switch-coffee-maker-14-rkilgore-1410-1-7365d15ab5594daeb983c081502ba0c4.jpeg',  # Coffee Maker
    12 => 'https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400&h=300&fit=crop',  # Blender Pro
    
    # Sports
    13 => 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=300&fit=crop',  # Yoga Mat
    14 => 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=400&h=300&fit=crop',  # Dumbbells Set
    22 => 'https://images.unsplash.com/photo-1617083934555-ac7b4d0c8be9?w=400&h=300&fit=crop',  # Yonex Badminton Racket
    
    # Toys
    15 => 'https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400&h=300&fit=crop',  # Board Game Classic
    16 => 'https://images.unsplash.com/photo-1494059980473-813e73ee784b?w=400&h=300&fit=crop',  # Puzzle 1000pc
    
    # Beauty
    17 => 'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=400&h=300&fit=crop',  # Shampoo Premium
    18 => 'https://www.tyoemcosmetic.com/wp-content/uploads/face-creams-manufacturer-1-1-1-768x576.jpg',  # Face Cream
    
    # Automotive
    19 => 'https://m.media-amazon.com/images/I/716tH1xGrdL._AC_SL1500_.jpg',  # Car Phone Mount
    20 => 'https://upload.wikimedia.org/wikipedia/commons/6/6a/ReifendruckPruefen.jpg',  # Tire Pressure Gauge
);

print "Updating product images with correct matches...\n";
print "-" x 60 . "\n";

my $update_sth = $dbh->prepare("UPDATE products SET image_url = ? WHERE id = ?");

foreach my $id (sort { $a <=> $b } keys %product_images) {
    my $image_url = $product_images{$id};
    $update_sth->execute($image_url, $id);
    print "Updated product ID $id with image\n";
}

$update_sth->finish();
$dbh->disconnect();

print "\n✓ All product images updated successfully!\n";
