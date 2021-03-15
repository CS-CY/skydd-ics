#!/usr/bin/env bats
load vars
@test "DUMP: check if services is running" {
    /bin/curl -s "http://${dump_ip}/status/cgi/status.cgi" | /bin/grep '[{"iptables.service":"inactive"},{"ip6tables.service":"inactive"},{"httpd.service":"active"},{"tcpdump@eth1.service":"active"},{"tcpdump@eth0.service":"active"},{"reaper.service":"active"}]'
}
@test "DUMP: check if dump files exist" {
    [[ $(/bin/curl -s "http://${dump_ip}/dump/cgi/get_files.cgi" | /bin/python -c 'import sys, json; print len(json.load(sys.stdin)["files"])') > 0 ]]
}
@test "DUMP: send data and verify" {
    /usr/bin/logger -n ${dump_ip} -P 514 -d dump_${RANDOM_STRING}_dump
    len=$(($(/bin/curl -s "http://${dump_ip}/dump/cgi/get_files.cgi" | /bin/python -c "import sys, json; print len(json.load(sys.stdin)['files'])")-1))
    file_name=""
    while [[ ! "${file_name}" =~ "eth1" ]]; do
        file_name=$(/bin/curl -s "http://${dump_ip}/dump/cgi/get_files.cgi" | /bin/python -c "import sys, json; print json.load(sys.stdin)['files'][$len]['name']")
        len=$((${len}-1))
        if [ ${len} < 0 ]; then
            exit 1
        fi
    done
    curl -s -o /tmp/bats-${file_name} "http://${dump_ip}/dump/cgi/get_file.cgi?file=${file_name}&download=yes"
    egrep -U dump_${RANDOM_STRING}_dump /tmp/bats-${file_name}
}
@test "DUMP: unpack a pcap" {
    counter=0
    file_name=$(/bin/curl -s "http://${dump_ip}/dump/cgi/get_files.cgi" | /bin/python -c "import sys, json; print json.load(sys.stdin)['files'][0]['name']")
    curl -s  "http://${dump_ip}/dump/cgi/chaos.cgi?file=${file_name}"
    while [[ ! "$(curl -s "http://${dump_ip}/dump/unpacked/${file_name}/index.html" -w "%{http_code}"|tail -1)" -eq "200" ]]; do
        counter=$((counter + 1))
        sleep 1
        if [ ${counter} > 10 ]; then
            echo "time out waiting"
            exit 1
        fi
    done
}
