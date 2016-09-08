import unittest
import mock

from hls_autocomplete import complete
from hls_autocomplete.utils import append_slash, load_cache

class TestSplitPath(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEquals(["user", "s.dolle", "Music"], complete.split_path("/user/s.dolle/Music"))
        self.assertEquals(["user", "s.dolle", "Music"], complete.split_path("/user/s.dolle/Music/"))

class TestAppendSlash(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEquals("/user/s.dolle/Music/", complete.append_slash("/user/s.dolle/Music", True))
        self.assertEquals("/user/s.dolle/Music", complete.append_slash("/user/s.dolle/Music", False))

class TestLoadCache(unittest.TestCase):
    @mock.patch("hls_autocomplete.utils.get_cache_path")
    def test_nominal_case(self, get_cache_path_mock):
        get_cache_path_mock.return_value = "/tmp/file"

        m = mock.mock_open(read_data='{"foo":{}}')
        with mock.patch("hls_autocomplete.utils.open", m, create=True):
            self.assertEqual({"foo": {}}, load_cache())

    @mock.patch("hls_autocomplete.utils.get_cache_path")
    def test_nominal_case(self, get_cache_path_mock):
        get_cache_path_mock.return_value = "/tmp/unexisting_file"
        self.assertEqual({}, load_cache())
