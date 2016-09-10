import unittest
import mock
import subprocess

from hls_autocomplete.hls import hls, hls_with_update

class TestHls(unittest.TestCase):
    @mock.patch("hls_autocomplete.hls.subprocess.Popen")
    def test_nominal_case(self, popen_mock):
        process_mock = mock.MagicMock()
        process_mock.communicate.return_value = "foo bar", None
        process_mock.returncode = 0
        popen_mock.return_value = process_mock

        self.assertEqual((0, "foo bar"), hls("foo"))
        popen_mock.assert_called_once_with(['hdfs', 'dfs', '-ls', 'foo'], stdout=subprocess.PIPE)

class TestHlsWithUpdate(unittest.TestCase):
    @mock.patch("hls_autocomplete.hls.update")
    @mock.patch("hls_autocomplete.hls.hls")
    def test_nominal_case(self, hls_mock, update_mock):
        hls_mock.return_value = (0, "/User/simon/Music")
        self.assertEqual("/User/simon/Music", hls_with_update("/User/simon"))
        update_mock.assert_called_once_with("/User/simon", "/User/simon/Music")

    @mock.patch("hls_autocomplete.hls.update")
    @mock.patch("hls_autocomplete.hls.hls")
    def test_error_case(self, hls_mock, update_mock):
        hls_mock.return_value = (1, "Error")
        self.assertEqual("Error", hls_with_update("/User/simon"))
        update_mock.assert_not_called()