#!/bin/bash
file=$1
search=$2
prog='/usr/bin/grep'
if [ ! -f "${file}" ];then
    exit 1
fi
if [[ "${file}" == *.gz ]]; then
prog='/usr/bin/zgrep'
fi
${prog} -m 1 -e "${search}" "${file}"
