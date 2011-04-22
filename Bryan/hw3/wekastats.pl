#!/usr/bin/env perl
use strict; use warnings;
use Getopt::Long;
use File::Glob qw{bsd_glob};
use List::Util qw{first};

my @data = ('diabetes');
my $ext = 'txt';
my @classes;
my @classifiers;
my $getopt_ok = GetOptions(
        'data=s' => \@data,
        'ext=s' => \$ext,
        'class=s' => \@classes,
        'classifier=s' => \@classifiers,);

my %class_ok = map {($_ => 1)} @classes;
my %classifier_ok = map {($_ => 1)} @classifiers;
my %class;

my %stats;
my $stat_order = q{};
for my $data_file (@data) {
    $stats{$data_file} = data_stats($data_file);
}

for my $data (@data) {
    print "$data\n";
    my $performance = $stats{$data};
    for my $class (keys %class) {
        print "CLASS: $class\n";
        printf "%15s%s\n", q{}, $stat_order;
        for my $classifier (keys %{$performance}) {
            printf "%15s%s\n", $classifier, $performance->{$classifier}->{$class};
        }
    }
}

sub data_stats {
    my $data = shift;
    my @classifier_outputs = bsd_glob("$data-*.$ext");
    my $data_len = length ($data) + 1; # Include the dash.
    my $ext_len = length ($ext) + 1; # Include the period.
    my $performance = {};
    STATFILES:
    for my $output (@classifier_outputs){
        my $stat_str = `grep -A2 -h 'TP Rate' "$output"`;
        my @stats = split qr{\s*\n}, $stat_str;
        $stat_order = shift @stats;
    
        substr $output, 0, $data_len, q{};
        substr $output, length ($output) - $ext_len, $ext_len, q{};
        my @details = split "-", $output;
        my $classifier = $details[-1];
        next STATFILES if @classifiers && !$classifier_ok{$classifier};

        $performance->{$classifier} = {};
        CLASSSTATS:
        for my $class_stat (@stats) {
            my $class = first {1} reverse split qr{\s+}, $class_stat;
            next CLASSSTATS if @classes && !$class_ok{$class};
            $class{$class} = 1;
            $performance->{$classifier}->{$class} = $class_stat;
        }
    }
    return $performance;
}
