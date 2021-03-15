#!/bin/bash
export IP=${IP}
echo "DEVICE=\"eth1\"
ONBOOT=yes
NETBOOT=no
IPV6INIT=yes
BOOTPROTO=static
IPADDR=${IP}
PREFIX=24
#IPV6ADDR=\"fc00::17/7\"
NM_CONTROLLED=no
TYPE=Ethernet
NAME=\"eth1\"
" > /etc/sysconfig/network-scripts/ifcfg-eth1

systemctl restart network
