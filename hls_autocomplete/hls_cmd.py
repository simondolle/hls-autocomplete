from __future__ import print_function
import sys


from complete import Cache
from hls import HlsLs, CacheHls

def main():
    if len(sys.argv) > 1:
        lister = HlsLs()
        cache = Cache.load_cache()
        lister = CacheHls(lister, cache)
        hls_result = lister.list_status(sys.argv[1])
        print(hls_result, end="")
        cache.save()

if __name__ == "__main__":
    main()