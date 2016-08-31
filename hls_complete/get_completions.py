#!/usr/bin/python

import os.path
import json
import sys

def get_cache_path():
    cache_dir = os.path.expanduser("~")
    input_file = os.path.join(cache_dir, ".hls_cache.json")
    return input_file

def load_cache():
    input_file = get_cache_path()
    if not os.path.exists(input_file):
        return {
            "is_dir": True,
            "content": {}
        }
    else:
        return json.load(open(input_file))

def split_path(path):
    path_chunks = path.split("/")
    path_chunks = [chunk for chunk in path_chunks if len(chunk) != 0]
    return path_chunks

def append_slash(path, is_dir):
    if is_dir:
        return path + "/"
    else:
        return path

def get_completions(path, cache):
    dirname = os.path.dirname(path)
    path_chunks = split_path(dirname)
    for path_chunk in path_chunks:
        if path_chunk not in cache["content"]:
            return []
        cache = cache["content"][path_chunk]
    if not type(cache) == type(dict()):
        return []

    result = []
    if "content" not in cache:
        return []
    for key, value in cache["content"].items():
        result.append((key, value["is_dir"]))

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
