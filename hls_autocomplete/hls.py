

import subprocess
import os.path

from update import LsParser, FileStatus

class CacheHls(object):
    def __init__(self, lister, cache):
        self.lister = lister
        self.cache = cache

    def list_status(self, path):
        hls_return_code, hls_result = self.lister.hls(path)
        if hls_return_code == 0:
            self.update_cache(path, hls_result)
        return hls_result

    def update_cache(self, path, hls_result):

        self.cache = self.cache.update_directory(path, hls_result)
        return self.cache

class HlsSubprocess(object):
    def list_status(self, path):
        return self.hls(path)

    def hls(self, path):
        p = self.get_process(path)
        hls_result = p.communicate()[0]
        hls_result = hls_result.decode("utf-8")
        hls_return_code = p.returncode
        ls_parser = LsParser()
        hls_result = ls_parser.parse(hls_result)
        hls_result = [FileStatus(os.path.relpath(fileStatus.path, path), fileStatus.is_dir, fileStatus.rights, fileStatus.nbFiles, fileStatus.owner, fileStatus.group, fileStatus.size, fileStatus.date) for fileStatus in hls_result]

        return hls_return_code, hls_result

    def get_process(self, path):
        return None

class HlsHdfs(HlsSubprocess):
    def get_process(self, path):
        return subprocess.Popen(["hdfs", "dfs", "-ls", path], stdout=subprocess.PIPE)

class HlsLs(HlsSubprocess):
    def get_process(self, path):
        return subprocess.Popen("ls -ld %s" % os.path.join(path, "*"), shell = True, stdout=subprocess.PIPE)

