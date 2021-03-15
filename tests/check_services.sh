#!/bin/bash

# we will ignore localhost and dhcp
if test "$(ss -ltunH | awk '!/127.0.0.1|::|*.68/{print $5}' | wc -l)" -ne 0; then
    echo "ERROR: server listening on external network interface"
    exit 1
fi
