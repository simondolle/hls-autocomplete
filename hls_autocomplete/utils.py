import os.path
import json

def get_cache_path():
    cache_dir = os.path.expanduser("~")
    input_file = os.path.join(cache_dir, ".hls_cache.json")
    return input_file

def load_cache():
    input_file = get_cache_path()
    try:
        cache_content = open(input_file)
        print "***********"
        #print cache_content.read()
        print "***********"
    except:
        return {}
    return json.load(cache_content)

def split_path(path):
    path_chunks = path.split("/")
    path_chunks = [chunk for chunk in path_chunks if len(chunk) != 0]
    return path_chunks

def append_slash(path, is_dir):
    if is_dir:
        return path + "/"
    else:
        return path