#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use JSON;
use IPC::Run qw( run );

my $query = CGI->new;
my $filerequest = $query->param('file');
if (! defined $filerequest){
   die "need a file arg";
}

my @logrows;
my @logrows_raw;
my $base_dir = '/home/tcpdump';
my $timestamp = 'tor jan  1 01:00:00 CET 1970';
opendir(my $dir, $base_dir);
my @files = readdir $dir;
closedir($dir);
foreach my $file (@files){
    if ($file =~ /pcap/){
        if ($file eq $filerequest){
            my ($output, $error, $in) = ('', '', '');
            my @prog = ('/usr/sbin/capinfos', "$base_dir/$file");
            run \@prog, \$in, \$output, \$error;
            my @res = split /$/m, $output;
            foreach my $row (@res) {
                if ($row =~ /capinfos: An error occurred/) {
                    $row = "Gick inte att analysera filen. Inspelning sker till den. Testa senare igen.";
                }
                push @logrows, $query->escapeHTML($row);
            }
            my $epoch_timestamp = (stat "$base_dir/$file")[9];
            $timestamp = localtime($epoch_timestamp);
        }
    }
}

if (defined $query->param('download') && $query->param('download') eq 'yes'){
    my $fileSize = (-s "$base_dir/$filerequest");
    print $query->header(
      -type=>'application/octet-stream',
      -Content_Length=> $fileSize,
      -attachment=>$filerequest);

    foreach my $file (@files){
        if ($file =~ /pcap/){
            if ($file eq $filerequest){
                open(my $fh, "$base_dir/$file") or die "Could not open file '$file' $!";
                binmode($fh);
                while (my $row = <$fh>) {
                    print $row;
                }
            }
        }
    }
} else {
    print $query->header();
    my $file_json = encode_json(\@logrows);
    print "{\"filerows\": $file_json, \"time\": \"$timestamp\"}";
}
