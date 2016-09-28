from __future__ import print_function
import sys

from hls import WebHdfsLister
from configuration import Configuration

def main():
    if len(sys.argv) > 1:
        configuration = Configuration.load()
        lister = WebHdfsLister(configuration.user, configuration.httpfs)
        code, hls_result = lister.list_status(sys.argv[1])
        for path in hls_result:
            print(path)

if __name__ == "__main__":
    main()