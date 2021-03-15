#!/usr/bin/python

from __future__ import division
import pyinotify
from os.path import isfile, join
import sys
import os
import re

def files_to_delete(path, file_pattern):
    return sorted([ join(path,f) for f in os.listdir(path) if isfile(join(path,f)) \
                    and re.match(file_pattern, f) ], 
                  key=lambda fn: os.stat(fn).st_mtime, reverse=True)

def free_space_up_to(free_bytes_required, path, file_pattern):
    file_list = files_to_delete(path, file_pattern)
    while file_list:
        statv = os.statvfs(path)
        if statv.f_bavail*statv.f_frsize >= free_bytes_required:
            break
        filename = file_list.pop()
        print("reaper.py: removing %s because free space went below %d bytes" \
            % (filename, free_bytes_required))
        os.remove(filename)

class event_handler(pyinotify.ProcessEvent):
    def __init__(self, path, free, pattern):
        self.path = path
        self.pattern = pattern
        s = os.statvfs(path)
        self.free_bytes = (s.f_frsize * s.f_blocks) * (float(free) / 100)

    def process_IN_CREATE(self, event):
        s = os.statvfs(path)
        if  (s.f_frsize * s.f_bavail) < self.free_bytes:
            free_space_up_to(self.free_bytes, self.path, self.pattern)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: ./reaper.py <directory> <disk_percent_free> [file_pattern]")
        sys.exit(1)

    path = sys.argv[1]
    percent_free = sys.argv[2]
    file_pattern = ""
    if len(sys.argv) == 4:
        file_pattern = sys.argv[3]

    wm = pyinotify.WatchManager()

    notifier = pyinotify.Notifier(wm, event_handler(path, percent_free, file_pattern))
    wm.add_watch(path, pyinotify.IN_CREATE)
    notifier.loop()
