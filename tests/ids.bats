#!/usr/bin/env bats
load vars
load ids
@test "IDS: check if services is running" {
    /bin/curl -s "http://${ids_ip}/status/cgi/status.cgi" | /bin/grep '[{"iptables.service":"inactive"},{"ip6tables.service":"inactive"},{"httpd.service":"active"},{"snort@eth1.service":"unknown"},{"snort@eth0.service":"active"},{"barnyard2.service":"active"},{"snorby.service":"active"}]'
}
@test "IDS: ensure we have redirect 302 from docs web" {
    HTTP_CODE=`/usr/bin/curl -s "http://${ids_ip}/ids" -w "%{http_code}"|tail -1`
    [ $HTTP_CODE -eq 302 ]
}
@test "IDS: ensure we have redirect to login page" {
    /usr/bin/curl -s "http://${ids_ip}:81" -w "%{http_code}"|/bin/egrep 302$
}
@test "IDS: ensure we have 200 ok on login page" {
    HTTP_CODE=`/usr/bin/curl -s "http://${ids_ip}:81/users/login" -w "%{http_code}"|tail -1`
    [ $HTTP_CODE -eq 200 ]
}
@test "IDS: login to snorby" {
    csrf=$(get_csrf)
    cookie=$(get_cookie)
    authtoken=$(get_authtoken)
    curl -s "http://${ids_ip}:81/users/login" -H "X-CSRF-Token: ${csrf}" --data "utf8=%E2%9C%93&authenticity_token=${authtoken}%3D&user%5Bemail%5D=snorby%40example.com&user%5Bpassword%5D=snorby&user%5Bremember_me%5D=0&user%5Bremember_me%5D=1"
}
@test "IDS: get login page" {
    /bin/curl -s "http://${ids_ip}:81/" -H "X-CSRF-Token: ${csrf}" -H "Cookie: $(get_user_session)"
}
@test "IDS: check severity 0" {
    dash=$(get_dashboard)
    IFS=
    [[ $(echo "${dash}" | egrep 'High Severity$' -B4|head -1|sed 's/\t//g') -eq "0" ]]
    [[ $(echo "${dash}" | egrep 'Medium Severity$' -B4|head -1|sed 's/\t//g') -eq "0" ]]
    [[ $(echo "${dash}" | egrep 'Low Severity$' -B4|head -1|sed 's/\t//g') -eq "0" ]]
}
