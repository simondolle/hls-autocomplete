import os
import json

USER = "user"
HTTPFS = "httpfs"

class Configuration(object):
    def __init__(self, user, httpfs):
        self.user = user
        self.httpfs = httpfs

    @staticmethod
    def load():
        return Configuration.load_from_file()

    @staticmethod
    def load_from_file():
        with open(Configuration.get_configuration_file_path()) as f:
            j = json.load(f)
            if USER not in j:
                raise ValueError('Missing "%s" key in conf file' % USER)
            if HTTPFS not in j:
                raise ValueError('Missing "%s" key in conf file' % HTTPFS)
            return Configuration(j[USER], j[HTTPFS])

    @staticmethod
    def get_configuration_file_path():
        return os.path.expanduser("~/.hls_autocomplete.conf")
