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
my $base_dir = '/home/tcpdump';
my $filesearch = undef;
my $param = $query->param('search');
if (defined($param) && length($param) > 0) {
    $filesearch = &base64_decode_unicode($param);
}
opendir(my $dir, $base_dir) or die "Could not open $base_dir: $!";
my @files = readdir $dir;
my @logfiles;
my $message = '';
my $counter = 0;
closedir($dir);
if (defined $filesearch && $filesearch =~ /^[A-Za-z0-9:. ]+$/){
    open (my $fh, ">", "/var/www/html/dump/searching.json");
    flock($fh, 2);
    print $fh '{"search":""}';
    close ($fh);
    print $query->header(-type => "application/json", -charset => "utf-8");
    foreach my $file (@files) {
        next if ($file !~ /pcap$/);
        next if ( -z "$base_dir/$file");
        $counter += 1;
        open (my $fh, ">", "/var/www/html/dump/searching.json");
        flock($fh, 2);
        print $fh "{\"search\":\"$file\"}";
        close ($fh);
        my ($output, $error, $in) = ('', '', '');
        my @prog = ('/usr/sbin/ngrep', "-q", "-n 1", "-I", "$base_dir/$file", "$filesearch");
        run \@prog, \$in, \$output, \$error;
        my @res = $output;
        if (scalar @res == 2) {
            chomp($res[1]);
            if ($message eq ''){
                $message = "Ingen match: $res[1]";
            }
            next;
        }
        elsif (scalar @res > 2) {
            if (defined $res[2] && $res[2]){
                chomp($res[2]);
                next if ($res[2] =~ m/match: $filesearch/g);
            }
            my %file_data = get_file_meta($base_dir, $file);
            push @logfiles, \%file_data;
            chomp($res[1]);
            $message = "Sökuttryck: [$filesearch] $res[1]";
        }
        else {
            my $len = scalar(@res);
            if ($message eq ''){
                $message = "Ej ngrep-kompatibelt uttryck: $filesearch [$file][length $len][@res]";
                last;
            }
            next;
        }
    }
    my $files_json = encode_json(\@logfiles);
    open (my $fh_search, ">", "/var/www/html/dump/searching.json");
    flock($fh_search, 2);
    print $fh_search "{\"files\": $files_json, \"files_count\":\"$counter\", \"message\": \"$message\"}";
    close ($fh_search);
}
elsif  (defined $filesearch) {
    $message = "<$filesearch> ej korrekt. Enbart tecken: A-Za-z0-9:. och mellanslag";
    print $query->header(-type => "application/json", -charset => "utf-8");
    print "{\"files\": \"\", \"message\": \"$message\"}";
}
else {
    foreach my $file (@files) {
        next if ($file !~ /pcap[0-9]*$/);
        next if ( -z "$base_dir/$file");
        my %file_data = get_file_meta($base_dir, $file);
        push @logfiles, \%file_data;
    }
    if (scalar(@files) == 0){
        $message = "Det finns inga nätverksinspelningar";
    }
    my $files_json = encode_json(\@logfiles);
    print $query->header(-type => "application/json", -charset => "utf-8");
    print "{\"files\": $files_json, \"message\": \"$message\"}";
}


sub get_file_meta {
    my ($base_dir, $file) = @_;
    my $epoch_timestamp = (stat "$base_dir/$file")[9];
    die "Could not stat file: $!" if (!defined $epoch_timestamp);
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
