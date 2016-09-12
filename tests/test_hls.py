import unittest
import mock
import subprocess

from hls_autocomplete.hls import HlsHdfs, CacheHls

class TestHls(unittest.TestCase):
    @mock.patch("hls_autocomplete.hls.subprocess.Popen")
    def test_nominal_case(self, popen_mock):
        process_mock = mock.MagicMock()
        process_mock.communicate.return_value = "foo bar", None
        process_mock.returncode = 0
        popen_mock.return_value = process_mock

        lister = HlsHdfs()
        self.assertEqual((0, "foo bar"), lister.hls("foo"))
        popen_mock.assert_called_once_with(['hdfs', 'dfs', '-ls', 'foo'], stdout=subprocess.PIPE)

class TestHlsWithUpdate(unittest.TestCase):
    @mock.patch("hls_autocomplete.hls.update")
    def test_nominal_case(self, update_mock):
        lister_mock = mock.MagicMock()
        lister_mock.hls.return_value = (0, "/User/simon/Music")
        lister = CacheHls(lister_mock)
        self.assertEqual("/User/simon/Music", lister.list_status("/User/simon"))
        update_mock.assert_called_once_with("/User/simon", "/User/simon/Music")

    @mock.patch("hls_autocomplete.hls.update")
    def test_error_case(self, update_mock):
        lister_mock = mock.MagicMock()
        lister_mock.hls.return_value = (1, "Error")
        lister = CacheHls(lister_mock)
        self.assertEqual("Error", lister.list_status("/User/simon"))
        update_mock.assert_not_called()