#!/bin/bash
counter=0
rm -rf /home/tcpdump/testfile-*
while true; do
  counter=$((counter + 1))
  echo "Will create 1GB file: /home/tcpdump/testfile-${counter}"
  dd if=/dev/zero of=/home/tcpdump/testfile-"${counter}" count=1024 bs=1048576 &>/dev/null
  echo "Used disk space in %:"
  df -h /home/tcpdump/ | tail -1 | awk '{ print substr($5 , 1, length($5)-1)}'
done
