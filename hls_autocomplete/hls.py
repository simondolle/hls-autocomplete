from __future__ import print_function

import sys
import subprocess

from hls_autocomplete.update import update

def hls(path):
    p = subprocess.Popen(["hdfs", "dfs", "-ls", path], stdout=subprocess.PIPE)
    hls_result = p.communicate()[0]
    hls_return_code = p.returncode
    print(hls_result, end="")
    if hls_return_code == 0:
        update(path, hls_result)

def main():
    if len(sys.argv) > 1:
        hls(sys.argv[1])

if __name__ == "__main__":
    main()