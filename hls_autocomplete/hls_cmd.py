from __future__ import print_function
import sys

from hls import WebHdfsLister
from configuration import Configuration
from parse import get_file_statuses_pretty_print

def main():
    if len(sys.argv) > 1:
        configuration = Configuration.load()
        lister = WebHdfsLister(configuration.httpfs, configuration.user)
        code, hls_result = lister.list_status(sys.argv[1])
        if code == 0:
            print(get_file_statuses_pretty_print(hls_result))
        sys.exit(code)
if __name__ == "__main__":
    main()
