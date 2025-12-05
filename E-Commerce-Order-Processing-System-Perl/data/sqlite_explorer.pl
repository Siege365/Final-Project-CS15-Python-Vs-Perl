#!/usr/bin/env perl
use strict;
use warnings;
use DBI;
use Term::ReadLine;
#type sa terminal og perl sqlite_explorer.pl
#perl sqlite_explorer.pl path/to/database.db
sub explore_db {
    my $db_path = shift;
    
    # Connect to database
    my $dbh = DBI->connect("dbi:SQLite:dbname=$db_path", "", "", {
        RaiseError => 1,
        AutoCommit => 1,
    }) or die "Cannot connect to database: $DBI::errstr";
    
    print "\n" . "=" x 60 . "\n";
    print "SQLite Database: $db_path\n";
    print "=" x 60 . "\n\n";
    
    # List all tables
    my $tables = $dbh->selectall_arrayref(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    );
    
    print "📊 Tables in database:\n";
    foreach my $table (@$tables) {
        my $table_name = $table->[0];
        my ($count) = $dbh->selectrow_array("SELECT COUNT(*) FROM $table_name");
        printf("  ✓ %-25s (%d rows)\n", $table_name, $count);
    }
    
    print "\n" . "=" x 60 . "\n";
    print "💡 Commands you can run:\n";
    print "  - To see table structure: PRAGMA table_info(table_name)\n";
    print "  - To query data: SELECT * FROM table_name LIMIT 10\n";
    print "  - Type 'exit' or 'quit' to exit\n";
    print "=" x 60 . "\n\n";
    
    # Interactive mode
    my $term = Term::ReadLine->new('SQLite Explorer');
    $term->ornaments(0);  # Disable fancy formatting
    
    while (defined(my $query = $term->readline('SQL> '))) {
        $query =~ s/^\s+|\s+$//g;  # Trim whitespace
        
        last if $query =~ /^(exit|quit|q|\.quit|\.exit)$/i;
        next if $query eq '';
        
        eval {
            my $sth = $dbh->prepare($query);
            $sth->execute();
            
            if ($query =~ /^\s*(SELECT|PRAGMA)/i) {
                my $names = $sth->{NAME};
                my @results;
                
                while (my $row = $sth->fetchrow_arrayref()) {
                    push @results, [@$row];
                }
                
                if (@results) {
                    # Print headers
                    if ($names && @$names) {
                        print "\n" . join(" | ", @$names) . "\n";
                        print "-" x (length(join(" | ", @$names)) + 10) . "\n";
                    }
                    
                    # Print rows
                    foreach my $row (@results) {
                        my @formatted = map { defined $_ ? $_ : 'NULL' } @$row;
                        print join(" | ", @formatted) . "\n";
                    }
                    print "\n(" . scalar(@results) . " rows)\n\n";
                } else {
                    print "(No results)\n\n";
                }
            } else {
                print "✓ Query executed successfully\n\n";
            }
            
            $sth->finish();
        };
        
        if ($@) {
            print "❌ Error: $@\n";
        }
    }
    
    print "\nGoodbye! 👋\n";
    $dbh->disconnect();
}

# Main
my $db_path = $ARGV[0] || "E-Commerce-Order-Processing-System-Perl/data/ecommerce.db";

if (!-f $db_path) {
    die "Error: Database file not found: $db_path\n";
}

explore_db($db_path);
