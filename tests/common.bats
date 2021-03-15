#!/usr/bin/env bats
load vars
@test "LOG: ensure we have redirect 302" {
    HTTP_CODE=`/usr/bin/curl -q -s -k "http://${log_ip}/" -w "%{http_code}"|tail -1`
    [ $HTTP_CODE -eq 302 ]
}
@test "LOG: ensure we have /foss/doc/" {
    HTTP_CODE=`/usr/bin/curl -q -s -k "http://${log_ip}/foss/doc/" -w "%{http_code}"|tail -1`
    [ $HTTP_CODE -eq 200 ]
}
@test "IDS: ensure we have redirect 302" {
    HTTP_CODE=`/usr/bin/curl -q -s -k "http://${ids_ip}/" -w "%{http_code}"|tail -1`
    [ $HTTP_CODE -eq 302 ]
}
@test "IDS: ensure we have /foss/doc/" {
    HTTP_CODE=`/usr/bin/curl -q -s -k "http://${ids_ip}/foss/doc/" -w "%{http_code}"|tail -1`
    [ $HTTP_CODE -eq 200 ]
}
@test "DUMP: ensure we have redirect 302" {
    HTTP_CODE=`/usr/bin/curl -q -s -k "http://${dump_ip}/" -w "%{http_code}"|tail -1`
    [ $HTTP_CODE -eq 302 ]
}
@test "DUMP: ensure we have /foss/doc/" {
    HTTP_CODE=`/usr/bin/curl -q -s -k "http://${dump_ip}/foss/doc/" -w "%{http_code}"|tail -1`
    [ $HTTP_CODE -eq 200 ]
}
@test "MONITOR: ensure we have redirect 302" {
    HTTP_CODE=`/usr/bin/curl -q -s -k "http://${monitor_ip}/" -w "%{http_code}"|tail -1`
    [ $HTTP_CODE -eq 302 ]
}
@test "MONITOR: ensure we have /foss/doc/" {
    HTTP_CODE=`/usr/bin/curl -q -s -k "http://${monitor_ip}/foss/doc/" -w "%{http_code}"|tail -1`
    [ $HTTP_CODE -eq 200 ]
}
