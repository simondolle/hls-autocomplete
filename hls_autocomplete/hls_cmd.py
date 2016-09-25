from __future__ import print_function
import sys

from hls import HlsLs

def main():
    if len(sys.argv) > 1:
        lister = HlsLs()
        code, hls_result = lister.list_status(sys.argv[1])
        for path in hls_result:
            print(path)

if __name__ == "__main__":
    main()