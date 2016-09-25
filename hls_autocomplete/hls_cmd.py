from __future__ import print_function
import sys
import os.path

from complete import Cache
from hls import HlsLs, CacheHls

def main():
    if len(sys.argv) > 1:
        lister = HlsLs()
        cache = Cache.load_cache()
        lister = CacheHls(lister, cache)
        path = sys.argv[1]
        hls_result = lister.list_status(sys.argv[1])
        #hls_result = [fileStatus.path for fileStatus in hls_result]
        #hls_result = [os.path.join(path, relpath) for relpath in hls_result]
        for path in hls_result:
            print(path)
        cache.save()

if __name__ == "__main__":
    main()