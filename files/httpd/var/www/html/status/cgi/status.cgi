#!/usr/bin/perl
use strict;
use warnings;
use CGI;
use JSON;
use IPC::Run qw( run );
my $query = CGI->new;
my @service_list;
my @services;
if ( -f "/opt/.foss-common") {
    my @service_list_common = ('iptables.service', 'ip6tables.service');
    push @service_list, @service_list_common;
}
if ( -f "/opt/.foss-httpd") {
    my @service_list_httpd = ('httpd.service');
    push @service_list, @service_list_httpd;
}
if ( -f "/opt/.foss-simple_log") {
    my @service_list_log = ('rsyslog.service');
    push @service_list, @service_list_log;
}
if ( -f "/opt/.foss-monitor") {
    my @service_list_log = ('rh-php71-php-fpm.service', 'icinga2.service', 'postgresql.service');
    push @service_list, @service_list_log;
}
if ( -f "/opt/.foss-ids") {
    my @service_list_ids = ('mariadb.service', 'barnyard2.service', 'snorby.service');
    my @intf = &get_interface;
    foreach my $int (@intf){
        my $service = 'snort@'.$int.'.service';
        push @service_list, $service;
    }
    push @service_list, @service_list_ids;
}
if ( -f "/opt/.foss-traffic") {
my @service_list_dump = ('reaper.service');
    my @intf = &get_interface;
    foreach my $int (@intf){
        my $service = 'tcpdump@'.$int.'.service';
        push @service_list, $service;
    }
    push @service_list, @service_list_dump;
}

foreach my $service (@service_list) {
    my ($output, $error, $in) = ('', '', '');
    my @prog = ('/bin/systemctl', 'is-active', $service);
    run \@prog, \$in, \$output, \$error;
    if ($output){
        chomp $output;
        push @services, { $service => $output };
    }
    else {
       die $error;
    }
}
my $json = encode_json(\@services);
print $query->header(-type => "application/json", -charset => "utf-8");
print "$json";

sub get_interface {
    my @intf;
    opendir (my $dh, '/sys/class/net');
    while (readdir $dh) {
        next if $_ =~ /^\./;
        next if $_ =~ /^lo$/;
        push @intf, $_;
    }
    return @intf;
}
