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


def is_valid_path(path):
    return "*" not in path

class Cache(object):
    def __init__(self, json):
        self.json = json

    def get_completions(self, path):
        json = self.json
        dirname = get_path_to_complete(path)
        path_chunks = split_path(dirname)
        for path_chunk in path_chunks:
            if path_chunk not in json:
                return []
            json = json[path_chunk]
        if not type(json) == type(dict()):
            return []
        result = []
        for key, value in json.items():
            result.append((key, value is not None))

        if not path.endswith("/"):
            partial_basename = os.path.basename(path)
            result = [s for s in result if s[0].startswith(partial_basename)]

        if len(path_chunks) == 0:
            result = [("/" + r[0], r[1]) for r in result]
        result = [append_slash(r[0], r[1]) for r in result]
        result = [os.path.join(dirname, r) for r in result]
        return sorted(result)

    def update_directory(self, directory, ls_results):
        result = self.json
        if not is_valid_path(directory):
            return result
        cache = self.json
        for path_chunk in split_path(directory):
            if path_chunk not in cache:
                cache[path_chunk] = {}
            cache = cache[path_chunk]
        basenames = [(os.path.basename(ls_result.path), ls_result.is_dir) for ls_result in ls_results]
        for basename, is_dir in basenames:
            if basename not in cache:
                if is_dir:
                    cache[basename] = {}
                else:
                    cache[basename] = None

        old_entries = set(cache.keys()).difference(set([basename for basename, is_dir in basenames]))
        for old_entry in old_entries:
            del cache[old_entry]
        return result

    @classmethod
    def get_cache_path(c):
        cache_dir = os.path.expanduser("~")
        input_file = os.path.join(cache_dir, ".hls_cache.json")
        return input_file

    @classmethod
    def load_cache(c):
        input_file = Cache.get_cache_path()
        try:
            cache_content = open(input_file)
        except:
            return {}
        return json.load(cache_content)

class CacheCompleter(object):
    def __init__(self):
        pass

    def get_completions(self, path, cache):
        return Cache(cache).get_completions(path)

    def get_completions_with_update(self, path, cache, lister):
        completions = self.get_completions(path, cache)
        if len(completions) == 0:
            lister.hls_with_update(get_path_to_complete(path))
            cache = self.load_cache()
            completions = self.get_completions(path, cache)
        return completions


def main():
    completer = CacheCompleter()
    hls_cache = completer.load_cache()
    if len(sys.argv) > 1:
        input_path = sys.argv[1].decode("utf-8")
        lister = HlsHdfs()
        lister = CacheHls(lister, Cache.load_cache())
        completions = completer.get_completions_with_update(input_path, hls_cache, lister)
        completions = ["%s"%s for s in completions]
        result = "\n".join(completions)
        print result.encode("utf-8")

if __name__ == "__main__":
    main()
