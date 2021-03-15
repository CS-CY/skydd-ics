#!/usr/bin/perl
use strict;
use warnings;
use CGI;

my $query = CGI->new;
my $filerequest = $query->param('file');
if (! defined $filerequest){
   die "need a file arg";
}
# If pcap data already created, just redirect
if (-f "/var/www/html/dump/unpacked/$filerequest/index.html"){
    print "Location: /dump/unpacked/$filerequest/index.html\n\n";
    exit;
}
my $base_dir = '/home/tcpdump';
opendir(my $dir, $base_dir);
my @files = readdir $dir;
closedir($dir);
foreach my $file (@files){
    if ($file =~ /pcap/){
        if ($file eq $filerequest){
            (-d "/var/www/html/dump/unpacked/$file") || mkdir "/var/www/html/dump/unpacked/$file";
            system("/opt/chaosreader -D /var/www/html/dump/unpacked/$file $base_dir/$file >/dev/null");
            my $index_html = "/var/www/html/dump/unpacked/$file/index.html";
            open (my $fh, '<', $index_html) or die "$!";
            my @fc = <$fh> or die "$!";
            close ($fh) or die "$!";
            open (my $write, '>', $index_html) or die "$!";
            foreach my $line (@fc){
                if ($line =~ /^<html>/){
                    print $write '<html><link href="/dump/css/chaos.css" rel="stylesheet" type="text/css"><link rel="stylesheet" type="text/css" href="/css/main.css">';
                } elsif ($line =~ /<body/){
                    print $write $line;
                    print $write '<header class="header"><a href="/dump/index.html" class="brand"><span class="brand-img"></span>Trafikdumplistning</a></header>';
                } else {
                    print $write $line;
                }
            }
            close ($write) or die "$!";
            print $query->redirect("../unpacked/$file/");
            exit(0);
        }
    }
}
print  $query->header(), $query->p("No such file."), $query->end_html();
