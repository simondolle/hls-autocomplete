import unittest
import mock
import datetime

from hls_autocomplete.complete import get_path_to_complete, is_valid_path, SimpleCompleter
from hls_autocomplete.parse import FileStatus

class TestGetPathToComplete(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEquals("/Users/simon", get_path_to_complete("/Users/simon/M"))
        self.assertEquals("/Users/simon", get_path_to_complete("/Users/simon/"))


class TestIsValidPath(unittest.TestCase):
    def test_is_valid_path(self):
        self.assertTrue(is_valid_path("/Users/simon"))
        self.assertTrue(is_valid_path("/Users/simon/"))
        self.assertFalse(is_valid_path("/Users/simon/*/Music"))

class TestSimpleCompleter(unittest.TestCase):
    def test_nominal_case(self):
        hls_lister_mock = mock.MagicMock()
        hls_lister_mock.list_status.return_value = (0, [
            FileStatus("/Users/simon/Documents", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20), "Documents"),
            FileStatus("/Users/simon/Dropbox", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20), "Dropbox"),
            FileStatus("/Users/simon/Music", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20), "Music"),
        ])
        completer = SimpleCompleter(hls_lister_mock)
        actual_result = completer.get_completions(
                "/Users/simon/D")
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/"]
        self.assertEquals(expected_result, actual_result)

    def test_directory_case(self):
        hls_lister_mock = mock.MagicMock()
        hls_lister_mock.list_status.return_value = (0, [
            FileStatus("/Users/simon/Documents", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20), "Documents"),
            FileStatus("/Users/simon/Dropbox", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20), "Dropbox"),
            FileStatus("/Users/simon/Music", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20), "Music"),
        ])
        completer = SimpleCompleter(hls_lister_mock)
        actual_result = completer.get_completions(
                "/Users/simon/")
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/", "/Users/simon/Music/"]
        self.assertEquals(expected_result, actual_result)

    def test_unexisting_directory(self):
        hls_lister_mock = mock.MagicMock()
        hls_lister_mock.list_status.return_value = (1, None)
        completer = SimpleCompleter(hls_lister_mock)
        actual_result = completer.get_completions(
                "/Users/toto/t")
        expected_result = []
        self.assertEquals(expected_result, actual_result)

    def test_double_slash(self):
        hls_lister_mock = mock.MagicMock()
        hls_lister_mock.list_status.return_value = (0, [
            FileStatus("/Users/simon/Documents", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20)),
            FileStatus("/Users/simon/Dropbox", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20)),
            FileStatus("/Users/simon/Music", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20)),
        ])
        completer = SimpleCompleter(hls_lister_mock)
        actual_result = completer.get_completions(
            "/Users/simon//")
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/", "/Users/simon/Music/"]
        self.assertEquals(expected_result, actual_result)

    def test_root_only(self):
        hls_lister_mock = mock.MagicMock()
        hls_lister_mock.list_status.return_value = (0, [
            FileStatus("/Users", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20))
        ])
        completer = SimpleCompleter(hls_lister_mock)
        actual_result = completer.get_completions("/")
        expected_result = ["/Users/"]
        self.assertEquals(expected_result, actual_result)