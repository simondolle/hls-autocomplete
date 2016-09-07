from __future__ import print_function

import sys
import json
import subprocess

from hls_autocomplete.complete import get_completions
from hls_autocomplete.update import update_directory, LsParser
from hls_autocomplete.utils import get_cache_path

def hls(path):
    p = subprocess.Popen(["hdfs", "dfs", "-ls", path], stdout=subprocess.PIPE)
    hls_result = p.communicate()[0]
    hls_return_code = p.returncode
    print(hls_result, end="")
    if hls_return_code == 0:
        hls_cache = get_completions.load_cache()

        ls_parser = LsParser()
        ls_result = ls_parser.parse(hls_result)

        update_directory(path, ls_result, hls_cache)
        json.dump(hls_cache, open(get_cache_path(), "w"), indent=4)


def main():
    if len(sys.argv) > 1:
        hls(sys.argv[1])

if __name__ == "__main__":
    main()
