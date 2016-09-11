from __future__ import print_function

import sys
import subprocess

from hls_autocomplete.update import update
from hls_autocomplete.utils import load_cache

def hls_with_update(path):
    hls_return_code, hls_result = hls(path)
    if hls_return_code == 0:
        cache = update(path, hls_result)
    else:
        cache = load_cache()
    return hls_result, cache

def hls(path):
    p = subprocess.Popen(["hdfs", "dfs", "-ls", path], stdout=subprocess.PIPE)
    hls_result = p.communicate()[0]
    hls_result = hls_result.decode("utf-8")
    hls_return_code = p.returncode
    return hls_return_code, hls_result

def main():
    if len(sys.argv) > 1:
        hls_result, cache = hls_with_update(sys.argv[1])
        print(hls_result, end="")

if __name__ == "__main__":
    main()