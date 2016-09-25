#!/usr/bin/python

import os.path
import sys

from utils import append_slash
from hls import HlsLs

def get_path_to_complete(path):
    if path.endswith("/"):
        result = path[:-1]
    else:
        result = os.path.dirname(path)
    return result

def is_valid_path(path):
    return "*" not in path

class SimpleCompleter(object):
    def __init__(self, lister):
        self.lister = lister

    def get_completions(self, path):
        code, result = self.lister.list_status(get_path_to_complete(path))
        if code != 0:
            return []
        if not path.endswith("/"):
            partial_basename = os.path.basename(path)
            result = [fileStatus for fileStatus in result if fileStatus.relpath.startswith(partial_basename)]

        result = [append_slash(fileStatus.path, fileStatus.is_dir()) for fileStatus in result]
        return sorted(result)

def main():
    if len(sys.argv) > 1:
        input_path = sys.argv[1].decode("utf-8")
        lister = HlsLs()
        completer = SimpleCompleter(lister)
        completions = completer.get_completions(input_path)
        completions = ["%s"%s for s in completions]
        result = "\n".join(completions)
        print result.encode("utf-8")

if __name__ == "__main__":
    main()
