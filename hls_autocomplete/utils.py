import os.path
import json



def split_path(path):
    path_chunks = path.split("/")
    path_chunks = [chunk for chunk in path_chunks if len(chunk) != 0]
    return path_chunks

def append_slash(path, is_dir):
    if is_dir:
        return path + "/"
    else:
        return path