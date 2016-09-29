from __future__ import print_function
import sys

from hls import WebHdfsLister
from configuration import Configuration
from parse import get_file_statuses_pretty_print

def main():
    if len(sys.argv) > 1:
        configuration = Configuration.load()
        lister = WebHdfsLister(configuration.user, configuration.httpfs)
        code, hls_result = lister.list_status(sys.argv[1])
        print(get_file_statuses_pretty_print(hls_result))

if __name__ == "__main__":
    main()