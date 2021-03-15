#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use JSON;
use PerlIO::gzip;

my $query = CGI->new;
print $query->header();
my $filerequest = $query->param('file');
if (! defined $filerequest){
   die "need a file arg: file=filename";
}

my @logrows;
my @logrows_raw;
my $base_dir = '/var/log';
my $timestamp = 'tor jan  1 01:00:00 CET 1970';
opendir(my $dir, $base_dir);
my @files = readdir $dir;
closedir($dir);
foreach my $file (@files){
    if ($file =~ /^incoming/){
        if ($file eq $filerequest){
            my $fh;
            if ($file =~ /.*gz/){
                open($fh, '<:gzip', "$base_dir/$file")
                  or die "Could not open file '$file' $!";
            } else {
                open($fh, '<', "$base_dir/$file")
                  or die "Could not open file '$file' $!";
            }
            while (my $row = <$fh>) {
                chomp $row;
                push @logrows, $query->escapeHTML($row);
                push @logrows_raw, $row;
            }
            close($fh);
            my $epoch_timestamp = (stat "$base_dir/$file")[9];
            $timestamp = localtime($epoch_timestamp);
        }
    }
}

if (defined $query->param('download') && $query->param('download') eq 'yes'){
    #print $query->header();
    my $fileSize = (-s "$base_dir/$filerequest");
    print "Content-Type: application/octet-stream\r\n";
    print "Content-Length: $fileSize\r\n";
    print "Content-Disposition: attachment; filename=\"$filerequest\"\r\n\r\n";
    foreach my $row (@logrows_raw){
    print "$row\n";
    }
} else {
    my $file_json = encode_json(\@logrows);
    print "{\"filerows\": $file_json, \"time\": \"$timestamp\"}";
}
