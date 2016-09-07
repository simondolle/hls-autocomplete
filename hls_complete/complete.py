#!/usr/bin/python

import os.path
import json
import sys

from hls_complete.utils import append_slash, split_path, load_cache

def get_completions(path, cache):
    dirname = os.path.dirname(path)
    path_chunks = split_path(dirname)
    for path_chunk in path_chunks:
        if path_chunk not in cache:
            return []
        cache = cache[path_chunk]
    if not type(cache) == type(dict()):
        return []
    result = []
    #if "content" not in cache:
    #    return []
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

def main():
    hls_cache = load_cache()
    if len(sys.argv) > 1:
        input_path = sys.argv[1].decode("utf-8")
        completions = get_completions(input_path, hls_cache)
        completions = ["'%s'"%s for s in completions]
        result = " ".join(completions)
        print result.encode("utf-8")

if __name__ == "__main__":
    main()
