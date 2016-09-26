#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
from time import strptime
import re
import os
import json

class FileStatus(object):
    def __init__(self, path, rights, nbFiles, owner, group, size, date, relpath = None):
        self.path = path

        self.rights = rights
        self.nbFiles = nbFiles
        self.owner = owner
        self.group = group

        self.size = size

        self.date = date
        self.relpath = relpath

    def __eq__(self, other):
        return (self.path == other.path and self.rights == other.rights and
                self.nbFiles == other.nbFiles and self.owner == other.owner and self.group == other.group and
                self.size == other.size and self.date == other.date)

    def is_dir(self):
        return self.rights.startswith("d")

    def __str__(self):
        result = "%s  %d %s  %s  %d %s %s" % (self.rights, self.nbFiles, self.owner, self.group, self.size, self.date.strftime("%d %b  %Y").lower(), self.path)
        return result.encode("utf-8")

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

        regex = "^([rwxd@+-]+)\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(\w+)\s+([:\d]+)\s+([\w\/]+)"

        m = re.match(regex, line, re.UNICODE)
        if m is None:
            return None

        rights =  m.group(1)
        nbFiles = int(m.group(2))
        owner =  m.group(3)
        group = m.group(4)
        size = int(m.group(5))

        day = int(m.group(6))
        month = m.group(7)
        try:
            month = strptime(month, '%b').tm_mon
        except:
            month = [u"jan", u"fév", u"mar", u"avr", u"mai", u"jui", u"juil", u"aoû", u"sep", u"oct", u"nov", u"déc"].index(month) + 1

        try:
            year = int(m.group(8))
        except:
            year = datetime.datetime.now().year
        path = m.group(9)

        date = datetime.date(year, month, day)

        return FileStatus(filename, rights, nbFiles, owner, group, size, date)

    def parse(self, output):
        result = [self.parse_line(line) for line in output.split("\n")]
        return [p for p in result if p is not None]

class WebHdfsParser(object):
    def __init__(self, path):
        self.path = path

    def permissions_to_unix_name(self, is_dir, rights):
        is_dir_prefix = 'd' if is_dir else '-'
        dic = {'7': 'rwx', '6': 'rw-', '5': 'r-x', '4': 'r--', '0': '---'}
        return is_dir_prefix + ''.join(dic[x] for x in rights)

    def parse_status(self, status):
        relpath = status["pathSuffix"]
        path = os.path.join(self.path, relpath)
        nbFiles = 0
        size = status["length"]
        owner = status["owner"]
        group = status["group"]
        is_dir = status["type"] == "DIRECTORY"
        right_digits = status["permission"]
        rights = self.permissions_to_unix_name(is_dir, right_digits)

        parsed_date = datetime.datetime.fromtimestamp(int(status["modificationTime"])/1000)

        date = datetime.date(parsed_date.year, parsed_date.month, parsed_date.day)

        return FileStatus(path, rights, nbFiles, owner, group, size, date, relpath)

    def parse(self, output):
        j = json.loads(output)
        statuses = j["FileStatuses"]["FileStatus"]
        result = []
        for status in statuses:
            result.append(self.parse_status(status))
        return result