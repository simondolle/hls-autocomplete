from optparse import OptionParser
import json
import sys
import os.path

import get_completions
import re

def update_directory(directory, ls_results, cache):
    #find node
    for path_chunk in get_completions.split_path(directory):
        if path_chunk not in cache["content"]:
            cache["content"][path_chunk] = {
                        "is_dir": True,
                        "content": {}
                    }
        cache = cache["content"][path_chunk]
    basenames = [(os.path.basename(ls_result.path), ls_result.is_dir) for ls_result in ls_results]
    for basename, is_dir in basenames:
        if basename not in cache["content"]:
            cache["content"][basename] = {
                        "is_dir": is_dir,
                        "content": {}
                    }

    old_entries = set(cache["content"].keys()).difference(set([basename for basename, is_dir in basenames]))
    for old_entry in old_entries:
        del cache["content"][old_entry]

class FileStatus(object):
    def __init__(self, path, is_dir):
        self.path = path
        self.is_dir = is_dir

    def __eq__(self, other):
        return self.path == other.path and self.is_dir == other.is_dir

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

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-d", dest="directory")
    parser.add_option("-l", dest="ls_result")

    (options, args) = parser.parse_args()

    hls_cache = get_completions.load_cache()

    if options.directory is None:
        print "Missing directory"
        sys.exit(1)

    if options.ls_result is None:
        print "Missing ls result"
        sys.exit(1)

    ls_parser = LsParser()
    ls_result = ls_parser.parse(options.ls_result)

    update_directory(options.directory, ls_result, hls_cache)
    json.dump(hls_cache, open(get_completions.get_cache_path(), "w"), indent=4)
