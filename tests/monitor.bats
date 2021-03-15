#!/usr/bin/env bats
load vars
@test "IDS: check if services is running" {
    /bin/curl -s "http://${monitor_ip}/status/cgi/status.cgi" | /bin/grep '{"iptables.service":"inactive"},{"ip6tables.service":"inactive"},{"httpd.service":"active"},{"rh-php71-php-fpm.service":"active"},{"icinga2.service":"active"},{"postgresql.service":"active"}'
}
@test "IDS: ensure we have redirect 302 from docs web" {
    HTTP_CODE=$(/bin/curl -s "http://${monitor_ip}/icingaweb2" -w "%{http_code}"|tail -1)
    [ ${HTTP_CODE} -eq 301 ]
}

@test "IDS: ensure we have 302 on login page" {
    HTTP_CODE=$(/bin/curl -s "http://${monitor_ip}/icingaweb2/authentication/login" -w "%{http_code}"|tail -1)
    [ ${HTTP_CODE} -eq 302 ]
}
