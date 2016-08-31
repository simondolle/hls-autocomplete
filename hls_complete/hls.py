from __future__ import print_function

import sys
import json
import subprocess

import hls_complete.get_completions
import hls_complete.update_completions

def hls(path):
    p = subprocess.Popen(["ls", "-l", path], stdout=subprocess.PIPE)
    hls_result = p.communicate()[0]
    hls_return_code = p.returncode
    print(hls_result, end="")
    if hls_return_code == 0:
        hls_cache = hls_complete.get_completions.load_cache()

        ls_parser = hls_complete.update_completions.LsParser()
        ls_result = ls_parser.parse(hls_result)


        hls_complete.update_completions.update_directory(path, ls_result, hls_cache)
        json.dump(hls_cache, open(hls_complete.get_completions.get_cache_path(), "w"), indent=4)


def main():
    if len(sys.argv) > 1:
        hls(sys.argv[1])
