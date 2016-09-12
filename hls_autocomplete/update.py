from optparse import OptionParser
import json
import sys
import os.path

import re

class FileStatus(object):
    def __init__(self, path, is_dir):
        self.path = path
        self.is_dir = is_dir

    def __eq__(self, other):
        return self.path == other.path and self.is_dir == other.is_dir

    def __str__(self):
        return str((self.path, self.is_dir))

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
        return FileStatus(filename, is_dir)

    def parse(self, output):
        result = [self.parse_line(line) for line in output.split("\n")]
        return [p for p in result if p is not None]



def update(path, hls_result):
    hls_cache = load_cache()

    ls_parser = LsParser()
    ls_result = ls_parser.parse(hls_result)

    hls_cache = update_directory(path, ls_result, hls_cache)
    json.dump(hls_cache, open(get_cache_path(), "w"), indent=4)
    return hls_cache
