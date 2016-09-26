import unittest
import mock
import subprocess
import datetime

from hls_autocomplete.hls import HlsHdfs, WebHdfsLister
from hls_autocomplete.update import FileStatus

class TestHls(unittest.TestCase):
    @mock.patch("hls_autocomplete.hls.subprocess.Popen")
    def test_nominal_case(self, popen_mock):
        process_mock = mock.MagicMock()
        process_mock.communicate.return_value = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music", None
        process_mock.returncode = 0
        popen_mock.return_value = process_mock

        lister = HlsHdfs()
        self.assertEqual((0, [FileStatus("/Users/simon/Music", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 12, 27))]), lister.hls("/Users/simon/"))
        popen_mock.assert_called_once_with(['hdfs', 'dfs', '-ls', '/Users/simon/'], stdout=subprocess.PIPE)

class TestWebHdfsLister(unittest.TestCase):
    @mock.patch("hls_autocomplete.hls.subprocess.Popen")
    def test_get_process(self, popen_mock):
        popen_mock.return_value = "cmd_result"

        lister = WebHdfsLister("server", "simon.dolle@gmail.com")
        self.assertEqual("cmd_result", lister.get_process("/foo/bar"))
        popen_mock.assert_called_once_with(['curl', '--negotiate', '-i', '-L', '-u:simon.dolle@gmail.com', 'server/foo/bar?op=LISTSTATUS'])