from optparse import OptionParser
import json
import sys
import os.path
import datetime
from time import strptime
import re

class FileStatus(object):
    def __init__(self, path, rights, nbFiles, owner, group, size, date):
        self.path = path

        self.rights = rights
        self.nbFiles = nbFiles
        self.owner = owner
        self.group = group

        self.size = size

        self.date = date
        self.relpath = None

    def __eq__(self, other):
        return (self.path == other.path and self.rights == other.rights and
                self.nbFiles == other.nbFiles and self.owner == other.owner and self.group == other.group and
                self.size == other.size and self.date == other.date)

    def is_dir(self):
        return self.rights.startswith("d")

    def __str__(self):
        result = "%s  %d %s  %s  %d %s %s" % (self.rights, self.nbFiles, self.owner, self.group, self.size, self.date.strftime("%d %b  %Y").lower(), self.path)
        return result

class LsParser(object):
    def __init__(self):
        pass

    def parse_line(self, line):
        m = re.search(" (/.*$)", line)
        if m is None:
            return None
        filename = m.group(1)
        m = re.match("^([rwxd+-]+)", line)
        if m is None:
            return None
        is_dir = m.group(1).startswith("d")


        #""drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music""

        regex = "^([rwxd+-]+)\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(\w+)\s+(\d+)\s+([\w\/]+)"
        m = re.match(regex, line)
        if m is None:
            return None

        rights =  m.group(1)
        nbFiles = int(m.group(2))
        owner =  m.group(3)
        group = m.group(4)
        size = int(m.group(5))

        day = int(m.group(6))
        month = m.group(7)
        month = strptime(month, '%b').tm_mon
        year = int(m.group(8))

        path = m.group(9)

        date = datetime.date(year, month, day)

        return FileStatus(filename, rights, nbFiles, owner, group, size, date)

    def parse(self, output):
        result = [self.parse_line(line) for line in output.split("\n")]
        return [p for p in result if p is not None]