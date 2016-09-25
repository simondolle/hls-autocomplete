#!/usr/bin/python

import os.path
import sys
import json

from utils import append_slash, split_path
from hls import HlsLs, CacheHls

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
        if not is_valid_path(directory):
            return self
        cache = self.json
        for path_chunk in split_path(directory):
            if path_chunk not in cache:
                cache[path_chunk] = {}
            cache = cache[path_chunk]
        basenames = [(os.path.basename(ls_result.relpath), ls_result.is_dir()) for ls_result in ls_results]
        for basename, is_dir in basenames:
            if basename not in cache:
                if is_dir:
                    cache[basename] = {}
                else:
                    cache[basename] = None

        old_entries = set(cache.keys()).difference(set([basename for basename, is_dir in basenames]))
        for old_entry in old_entries:
            del cache[old_entry]
        return self

    def __eq__(self, other):
        return self.json == other.json

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
            return Cache({})
        return Cache(json.load(cache_content))

    def save(self):
        json.dump(self.json, open(Cache.get_cache_path(), "w"), indent=4, sort_keys=True)

class CacheCompleter(object):
    def __init__(self, cache, lister):
        self.cache = cache
        self.lister = lister

    def get_completions(self, path):
        completions = self.cache.get_completions(path)
        if len(completions) == 0:
            self.lister.list_status(get_path_to_complete(path))
            self.cache = Cache.load_cache()
            completions = self.cache.get_completions(path)
        return completions

def main():
    if len(sys.argv) > 1:
        input_path = sys.argv[1].decode("utf-8")
        lister = HlsLs()
        hls_cache = Cache.load_cache()
        lister = CacheHls(lister, hls_cache)
        completer = CacheCompleter(hls_cache, lister)
        completions = completer.get_completions(input_path)
        completions = ["%s"%s for s in completions]
        result = "\n".join(completions)
        print result.encode("utf-8")
        hls_cache.save()


if __name__ == "__main__":
    main()
