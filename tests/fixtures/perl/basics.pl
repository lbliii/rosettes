#!/usr/bin/env perl
use strict;
use warnings;
use feature 'say';

my $name = "World";
say "Hello, $name!";

my @items = (1, 2, 3, 4, 5);
my %hash = (key => 'value', foo => 'bar');

sub greet {
    my ($name, $greeting) = @_;
    $greeting //= "Hello";
    return "$greeting, $name!";
}