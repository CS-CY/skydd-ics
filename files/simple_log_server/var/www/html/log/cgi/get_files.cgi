#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use JSON;
use URI::Escape;
use URI::Encode;
use MIME::Base64;
use Encode;
use IPC::Run qw( run );

my $query = CGI->new;
my $base_dir = '/var/log';
opendir(my $dir, $base_dir);
my @files = readdir $dir;
my @logfiles;
closedir($dir);
if (defined $query->param('search')){
    print $query->header(-type => "application/json", -charset => "utf-8");
    my $filesearch = &base64_decode_unicode($query->param('search'));
    foreach my $file (@files){
        if ($file =~ /^incomin/){
            open (my $fh, ">", "/var/www/html/log/searching.json");
            flock($fh, 2);
            print $fh "{\"search\":\"$file\"}";
            close ($fh);
            if (defined $filesearch){
                my ($output, $error, $in) = ('', '', '');
                my @prog                  = ('/var/www/html/log/cgi/search.sh', "$base_dir/$file", "$filesearch");
                run \@prog, \$in, \$output, \$error;
                if ($output){
                    my %file_data = get_file_meta($base_dir, $file);
                    push @logfiles, \%file_data;
                }
            }
        }
    }
    my $files_json = encode_json(\@logfiles);
    open (my $fh, ">", "/var/www/html/log/searching.json");
            flock($fh, 2);
    print $fh "{\"files\": $files_json}";
    close ($fh);
} else {
    foreach my $file (@files){
        if ($file =~ /^incoming/){
            my %file_data = get_file_meta($base_dir, $file);
            push @logfiles, \%file_data;
        }
    }
    my $files_json = encode_json(\@logfiles);
    print $query->header();
    print "{\"files\": $files_json}";
}

sub get_file_meta {
    my ($base_dir, $file) = @_;
    my $epoch_timestamp = (stat "$base_dir/$file")[9];
    my $timestamp = localtime($epoch_timestamp);
    my $size = getFileSize("$base_dir/$file");
    my %file_data = ('name', $file, 'time', $timestamp, 'size', $size);
    return %file_data;
}

sub getFileSize {
    # this sub will return the file size of a file in a human value
    # currently it use two decimals from a calculated metric
    my ($file) = @_;
    if (-f $file){
        my $fileSize = (-s $file);
        my ($fileSizeHuman, $metric, $divide);
        my $kB = '1000';
        my $MB = '1000000';         # 1000 * 1000
        my $GB = '1000000000';      # 1000 * 1000 * 1000
        my $TB = '1000000000000';   # 1000 * 1000 * 1000 * 1000
        my $PB = '1000000000000000';# 1000 * 1000 * 1000 * 1000 * 1000
        if ($fileSize > $PB ){
            $divide = $PB;
            $metric = 'PB';
        } elsif ($fileSize > $TB){
            $divide = $TB;
            $metric = 'TB';
        } elsif ($fileSize > $GB){
            $divide = $GB;
            $metric = 'GB';
        } elsif ($fileSize > $MB){
            $divide = $MB;
            $metric = 'MB';
        } elsif ($fileSize > $kB){
            $divide = $kB;
            $metric = 'kB';
        } else {
            $divide = '1';
            $metric = 'B';
        }
        $fileSize       = ($fileSize) / $divide;
        $fileSizeHuman  = sprintf("%.2f", $fileSize);
        return "$fileSizeHuman $metric";
    } else {
        die("Did nog get a valid file, $file. [$!]");
    }
}
sub base64_decode_unicode{
    my $encoded_data = shift;
    my $uri = URI::Encode->new( { encode_reserved => 0 } );
    my $base64_encoded_data = decode_base64($encoded_data);
    my $uri_decode = $uri->decode($base64_encoded_data);
    my $string = decode( "utf8", $uri_decode );
    utf8::encode($string);
    if ($string =~ /^(.*)$/ ){
        $string = $1;
    }
    return $string;
}
