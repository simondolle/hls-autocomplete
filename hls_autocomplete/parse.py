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
        return self.to_str(0, 0, 0, 0, 0, 0, 0)

    def to_str(self, rights_width, nbFiles_width, owner_width, group_width, size_width, date_width, path_with):
	if self.is_dir:
          nb_files = "-"
	else:
          nb_files = str(self.nbFiles)
        result = "%s   %s %s %s          %s %s %s" % (self.rights.ljust(rights_width),
                                             nb_files.ljust(nbFiles_width),
                                             self.owner.ljust(owner_width),
                                             self.group.ljust(group_width),
                                             str(self.size).ljust(size_width),
                                             self.date.strftime("%Y-%M-%d %H:%M").ljust(date_width),
                                             self.path.ljust(path_with))
        return result.encode("utf-8")

def get_file_statuses_pretty_print(file_statuses):
    rights_width = max([len(fs.rights) for fs in file_statuses])
    nb_files_width = max([len(str(fs.nbFiles)) for fs in file_statuses])
    owner_width = max([len(fs.owner) for fs in file_statuses])
    group_width = max([len(fs.group) for fs in file_statuses])
    size_width = max([len(str(fs.size)) for fs in file_statuses])
    date_width = max([len(fs.date.strftime("%Y-%M-%d %H:%M")) for fs in file_statuses])
    path_width = max([len(fs.path) for fs in file_statuses])

    result = []
    for file_status in file_statuses:
        result.append(file_status.to_str(rights_width, nb_files_width, owner_width, group_width, size_width, date_width, path_width))
    return "\n".join(result)

class LsParser(object):
    def __init__(self):
        pass

    def parse_line(self, line):
        regex = "^([rwxd@+-]+)\s+(\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(\w+)\s+([:\d]+)\s+(/.+)$"

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
        filename = m.group(9)

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
        sticky = False
        if len(rights) == 4 and rights[0] == '1':
            sticky = True
            rights = rights[1:]
        dic = {'7': 'rwx', '6': 'rw-', '5': 'r-x', '4': 'r--', '3': '-wx', '2': '-w-', '1': '--x', '0': '---'}
        result = is_dir_prefix + ''.join(dic[x] for x in rights)
        if sticky:
            result = result[:-1] + "t"
        return result

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

        parsed_date = datetime.datetime.utcfromtimestamp(int(status["modificationTime"])/1000)

        date = datetime.datetime(parsed_date.year, parsed_date.month, parsed_date.day, parsed_date.hour, parsed_date.minute)

        return FileStatus(path, rights, nbFiles, owner, group, size, date, relpath)


    def parse(self, output):
	try:
          j = json.loads(output)
	except:
	  print output	
	  return []	
        if "FileStatuses" not in j or "FileStatus" not in j["FileStatuses"]:
            print j
            return []
        statuses = j["FileStatuses"]["FileStatus"]
        result = []
        for status in statuses:
            result.append(self.parse_status(status))
        return result
