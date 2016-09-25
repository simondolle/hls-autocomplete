import subprocess
import os.path

from update import LsParser

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
        for fileStatus in hls_result:
            fileStatus.relpath = os.path.relpath(fileStatus.path, path)

        return hls_return_code, hls_result

    def get_process(self, path):
        return None

class HlsHdfs(HlsSubprocess):
    def get_process(self, path):
        return subprocess.Popen(["hdfs", "dfs", "-ls", path], stdout=subprocess.PIPE)

class HlsLs(HlsSubprocess):
    def get_process(self, path):
        return subprocess.Popen("ls -ld %s" % os.path.join(path, "*"), shell = True, stdout=subprocess.PIPE)