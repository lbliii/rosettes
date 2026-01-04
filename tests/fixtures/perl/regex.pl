if ($text =~ /pattern/) {
    print "Match!\n";
}

$text =~ s/old/new/g;
$text =~ tr/a-z/A-Z/;

my @matches = $text =~ /(\w+)/g;