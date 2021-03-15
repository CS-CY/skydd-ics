#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
my %hash;
open (my $fh, '<', '95_refs.md') or die;
binmode($fh, ":utf8");
while(my $row = <$fh>) {
    chomp $row;
    if ($row =~ m/^\[(.*)]: (http.*) \".*/) {
        $hash{$1} = $2;
    }
}
open (my $pf, '>', '96_refs.md') or die;
binmode($pf, ":utf8");
my $max_length = 0;
foreach my $key(keys %hash){
    if (length($key) > $max_length){
        $max_length = length($key);
    }
}
print $pf "# Referenser\n";
print $pf "\n";
print $pf "+---";
&printCharNumberOfTimes('-',$max_length);
print $pf "---+---------------------------------+\n";
print $pf "| Referens     ";
&printCharNumberOfTimes(' ', $max_length - 9);
print $pf " | Länk                            |\n";
print $pf "+===";
&printCharNumberOfTimes('=',$max_length);
print $pf "===+=================================+\n";



foreach my $key(sort keys %hash){
    #print "$key $hash{$key}\n";
	    print $pf "| **$key** ";
        &printCharNumberOfTimes(' ',$max_length - length($key));
        print $pf "| <$hash{$key}> |\n";
print $pf "+---";
&printCharNumberOfTimes('-',$max_length);
print $pf "---+---------------------------------+\n";
}



#while(<>) {
#	if ($_ =~ /^\[([^\]]*)]: (http.*)/){
#	if ($_ =~ /^\[(.*)]: (http.*) \".*/){
#	    print "| **$1** ";
#        &printCharNumberOfTimes(' ',$max_length - length($1));
#        print " | $2 |\n";
#        print "+----------------------------+---------------------------------+\n";
#	}
#}

print $pf "\n";
print $pf "\\clearpage\n";

close ($pf);

sub printCharNumberOfTimes {
    my ($char, $number) = @_;
    for (my $i = 0; $i < $number; $i++){
        print $pf "$char";
    }
}
