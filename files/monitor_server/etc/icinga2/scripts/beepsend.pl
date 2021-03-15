#!/usr/bin/perl -T
use strict;
use warnings;
use LWP::UserAgent;

###################################################################
#
# Nedanstående 3 variabler måste ändras för att beepsend ska kunna fungera
# Ändra det värdet som är mellan enkelfnuttarna (') till respektive variabel
#
###################################################################
#

# Avsändare på sms, både namn och nummer fungerar
my $from = 'system'; 

# Den anslutning som används för det aktuella kontot
my $beepConnection  = ''; # example company_ab

# Den hemliga nyckeln som hämtas från beepsend
my $beepToken = ''; # ex 1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef (64 tecken)

#
####################





my $toNumber = $ARGV[0];
my $msg      = $ARGV[1];
my $response = 0;
if ($toNumber =~ m/^([1-9]{1}[0-9]{1,15})$/){
    $toNumber = "+$1";  # append the plus sign
} else {
    die "Could not validate number, $toNumber";
}
if ($msg =~ /^[A-Za-z0-9\s\n\:]{1,160}$/i ){    # Only allow some characters at the moment
    $msg = $msg;
} else {
    die "Wrong message: $msg [$!]";
}

my $verifyssl       = '1';        # 0 = not verify, 1 = verify
my $beepServerDomain= 'connect.beepsend.com';
my $beepServer      = 'https://'.$beepServerDomain;
my $sendSMSurl      = '/api/2/sms/'.$beepConnection;
my $uri             = $beepServer.$sendSMSurl;
my $headBeepToken   = 'Token '.$beepToken; # Tokenformat used by beepsend
my $json =   "{
    \"batch_label\": \"label\",
    \"to\": \"$toNumber\",
    \"message\": \"$msg\",
    \"from\": \"$from\",
    \"encoding\": \"UTF-8\",
    \"receive_dlr\": false
}";

my $ua = LWP::UserAgent->new(ssl_opts => {verify_hostname => $verifyssl });
my $req = HTTP::Request->new(POST => $uri);
$req->header('Accept'           => 'text/html');
$req->header('Accept-Language'  => 'en-US');
$req->header('Content-Type'     => 'application/json; charset=UTF-8');
$req->header('Authorization'    => $headBeepToken);
$req->header('Host'             => $beepServerDomain);
$req->header('Referer'          => $beepServer);
$req->header('User-Agent'       => 'foss/server');
$req->content($json);
my $resp = $ua->request($req);
if ($resp->is_success) {
    my $message = $resp->decoded_content;
    if ($message =~ m/\"errors\"\:null/){
        $response = 1;
        warn "Response: $message";
    } else {
        warn "Response: $message";
    }
}
else {
    my $responseCode = $resp->code;
    my $responseMessage = $resp->message;
    warn "HTTP POST error code: $responseCode";
    warn "HTTP POST error message: $responseMessage";
}
