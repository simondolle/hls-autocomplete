#!/usr/bin/python

import os.path
import sys
import json

from utils import append_slash, split_path
from hls import HlsHdfs, CacheHls

def get_path_to_complete(path):
    if path.endswith("/"):
        result = path[:-1]
    else:
        result = os.path.dirname(path)
    return result

class CacheCompleter(object):
    def __init__(self):
        pass

    def get_completions(self, path, cache):
        dirname = get_path_to_complete(path)
        path_chunks = split_path(dirname)
        for path_chunk in path_chunks:
            if path_chunk not in cache:
                return []
            cache = cache[path_chunk]
        if not type(cache) == type(dict()):
            return []
        result = []
        for key, value in cache.items():
            result.append((key, value is not None))

        if not path.endswith("/"):
            partial_basename = os.path.basename(path)
            result = [s for s in result if s[0].startswith(partial_basename)]

        if len(path_chunks) == 0:
            result = [("/" + r[0], r[1]) for r in result]
        result = [append_slash(r[0], r[1]) for r in result]
        result = [os.path.join(dirname, r) for r in result]
        return sorted(result)

    def get_completions_with_update(self, path, cache, lister):
        completions = self.get_completions(path, cache)
        if len(completions) == 0:
            lister.hls_with_update(get_path_to_complete(path))
            cache = self.load_cache()
            completions = self.get_completions(path, cache)
        return completions

    def get_cache_path(self):
        cache_dir = os.path.expanduser("~")
        input_file = os.path.join(cache_dir, ".hls_cache.json")
        return input_file

    def load_cache(self):
        input_file = self.get_cache_path()
        try:
            cache_content = open(input_file)
        except:
            return {}
        return json.load(cache_content)

def main():
    completer = CacheCompleter()
    hls_cache = completer.load_cache()
    if len(sys.argv) > 1:
        input_path = sys.argv[1].decode("utf-8")
        lister = HlsHdfs()
        lister = CacheHls(lister)
        completions = completer.get_completions_with_update(input_path, hls_cache, lister)
        completions = ["%s"%s for s in completions]
        result = "\n".join(completions)
        print result.encode("utf-8")

if __name__ == "__main__":
    main()
