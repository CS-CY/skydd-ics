#!/bin/bash
grep -Ei 'error|warn' /var/log/messages | \
    grep -Ev 'gnome|avahi|pulse|dbus|firewalld|freedesktop|anaconda|spice|warn=True|find_install_errors|warning/ApplyRule|barnyard2: INFO|barnyard2: WARNING|snorby: Jammit Warning|snort: WARNING:|FATAL ERROR: User "snort" unknown.'
