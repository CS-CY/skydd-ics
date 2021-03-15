#!/usr/bin/env bats
load vars
@test "LOG: Send UDP log" {
   /usr/bin/logger -n ${log_ip} -P 514 -d udp_${RANDOM_STRING}
   /usr/bin/curl -s "http://${log_ip}/log/cgi/get_file.cgi?file=incoming" | /usr/bin/grep udp_${RANDOM_STRING}
}
@test "LOG: Send TCP log" {
   /usr/bin/logger -n ${log_ip} -P 514 -T tcp_${RANDOM_STRING}
   /usr/bin/curl -s "http://${log_ip}/log/cgi/get_file.cgi?file=incoming" | /usr/bin/grep tcp_${RANDOM_STRING}
}
