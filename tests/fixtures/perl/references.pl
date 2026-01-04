my $scalar_ref = \$scalar;
my $array_ref = \@array;
my $hash_ref = \%hash;
my $code_ref = \&subroutine;

my $anon_array = [1, 2, 3];
my $anon_hash = {key => 'value'};
my $anon_sub = sub { return $_[0] * 2 };

print $$scalar_ref;
print $array_ref->[0];
print $hash_ref->{key};
$code_ref->();