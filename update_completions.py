from optparse import OptionParser
import json
import sys
import os.path

import get_completions
import re

def update_directory(directory, ls_results, cache):
    #find node
    for path_chunk in get_completions.split_path(directory):
        if path_chunk not in cache:
            cache[path_chunk] = {}
        cache = cache[path_chunk]
    basenames = [os.path.basename(ls_result) for ls_result in ls_results]

    for basename in basenames:
        if basename not in cache:
            cache[basename] = {}

    old_entries = set(cache.keys()).difference(set(basenames))
    for old_entry in old_entries:
        del cache[old_entry]

class LsParser(object):
    def __init__(self):
        pass

    def parse_line(self, line):
        m = re.search(" (/.*$)", line)
        if m is None:
            return None
        return m.group(1)

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
