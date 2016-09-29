import subprocess
import os.path

from parse import LsParser, WebHdfsParser

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

class WebHdfsLister(object):
    def __init__(self, webhdfs_server, user):
        self.webhdfs_server = webhdfs_server
        self.user = user

    def list_status(self, path):
        p = self.get_process(path)
        hls_result = p.communicate()[0]
        hls_return_code = p.returncode
        if hls_return_code != 0:
            return hls_return_code, []
        hls_result = hls_result.decode("utf-8")
        ls_parser = WebHdfsParser(path)
        hls_result = ls_parser.parse(hls_result)
        return hls_return_code, hls_result

    def get_process(self, path):
        http_adress = "%s%s?op=LISTSTATUS" % (self.webhdfs_server, path)
        devnull = open(os.devnull, "w")
        return subprocess.Popen(["curl", "--negotiate", "-L", "-u:%s" % self.user, http_adress], stdout=subprocess.PIPE,
                            stderr=devnull)