import os
import json

class Configuration(object):
    def __init__(self, user, webhdfsserver):
        self.user = user
        self.webhdfsserver = webhdfsserver

    @staticmethod
    def load(cl):
        return cl.load_from_file()

    @staticmethod
    def load_from_file(cl):
        with open(cl.get_configuration_file_path()) as f:
            j = json.load(f.read())
            if "user" not in j:
                raise ValueError('Missing "user" key in conf file')
            if "webhdfs" not in j:
                raise ValueError('Missing "webhdfs" key in conf file')
            return Configuration(j["user"], j["webhdfs"])

    @staticmethod
    def get_configuration_file_path(cl):
        return os.path.expanduser("~/.hls_autocomplete.conf")
