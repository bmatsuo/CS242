#!/usr/bin/env perl
use File::Glob qw{bsd_glob};

my $exdir = 'ex2_data';
my @files = bsd_glob("$exdir/*");
my %files_with_rule;
for my $o (@files) {
    if ($o =~ /train\.txt \z/xms) { next; }
    elsif ($o =~ /test-.*\.txt \z/xms) { next; }
    elsif ($o =~ /(\w+)-(\w+).txt/xms) {
        #print "$o\n";
        my ($noise, $rule) = ($1,$2);
        if (!defined $files_with_rule{$rule}) {
            $files_with_rule{$rule} = {
                clean => [],
                noisy => [],
            };
        }
        push @{$files_with_rule{$rule}->{$noise}}, $o
    }
    else {
        die "Can't find prediction rule for file"
    }
}
my @rules = sort keys %files_with_rule;
printf "%7s", q{};
#print "@rules\n"; exit 0;
print join (q{}, map {sprintf "%8s", $_} @rules), "\n";
for my $noise (qw{noisy clean}) {
    printf "%7s", $noise;
    for my $rule (@rules) {
        my @rule_outs = @{$files_with_rule{$rule}->{$noise}};
        #print "@rule_outs\n";
        my $mistakes = 0;
        for my $output (@rule_outs) {
            open my $oh, '<', $output
                or die "Couldn't open output $output";
            my @lines = <$oh>;
            @lines = grep {$_ !~ m/\A [#]/xms} @lines;
            for my $l (@lines) {
                $l =~ s/\s* \n \z//xms;
                my @data = split /\s+/, $l;
                my ($label, $pred) = @data[-2 .. -1];
                #print "$rule $label $pred\n";
                $mistakes++ if $pred ne $label;
            }
            close $oh;
        }
        printf "%8d", $mistakes;
    }
    print "\n";
}
