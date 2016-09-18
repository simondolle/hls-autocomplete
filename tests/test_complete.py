import unittest
import mock

from hls_autocomplete.complete import CacheCompleter, get_path_to_complete, is_valid_path, Cache

class TestGetCompletions(unittest.TestCase):

    def setUp(self):
        self.cache = Cache({
            "Users": {
                "simon": {
                    "Music": {
                        "Spotify": {}
                    },
                    "Documents": {
                        "work": {
                            "CV.doc": None
                        }
                    },
                    "Dropbox": {}
                }
            }
        })
        self.completer = CacheCompleter(self.cache, None)


    def test_nominal_case(self):
        actual_result = self.completer.get_completions(
                "/Users/simon/D")
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/"]
        self.assertEquals(expected_result, actual_result)

    def test_directory_case(self):
        actual_result = self.completer.get_completions(
                "/Users/simon/")
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/", "/Users/simon/Music/"]
        self.assertEquals(expected_result, actual_result)

    def test_directory_case(self):
        actual_result = self.completer.get_completions(
                "/Users/simon/")
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/", "/Users/simon/Music/"]
        self.assertEquals(expected_result, actual_result)

    def test_unexisting_directory(self):
        actual_result = self.completer.get_completions(
                "/Users/toto/t")
        expected_result = []
        self.assertEquals(expected_result, actual_result)

    def test_too_long_path(self):
        actual_result = self.completer.get_completions(
                "/Users/simon/Documents/work/old")
        expected_result = []
        self.assertEquals(expected_result, actual_result)

    def test_double_slash(self):
        actual_result = self.completer.get_completions(
            "/Users/simon//")
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/", "/Users/simon/Music/"]
        self.assertEquals(expected_result, actual_result)

    def test_root_only(self):
        actual_result = self.completer.get_completions(
                "/")
        expected_result = ["/Users/"]
        self.assertEquals(expected_result, actual_result)

    def test_second_level(self):
        actual_result = self.completer.get_completions(
                "/Users/si")
        expected_result = ["/Users/simon/"]
        self.assertEquals(expected_result, actual_result)

    def test_file_with_extension(self):
        actual_result = self.completer.get_completions(
                "/Users/simon/Documents/work/C")
        expected_result = ["/Users/simon/Documents/work/CV.doc"]
        self.assertEquals(expected_result, actual_result)

    def test_empty_json(self):
        actual_result = CacheCompleter(Cache({}), None).get_completions(
                "/Users")
        expected_result = []
        self.assertEquals(expected_result, actual_result)

class TestGetCompletionsWithUpdate(unittest.TestCase):
    def testNoUpdate(self):
        cache = Cache({
            "Users": {
                "simon": {
                    "Music": {
                        "Spotify": {}
                    },
                    "Documents": {
                        "work": {
                            "CV.doc": None
                        }
                    },
                    "Dropbox": {}
                }
            }
        })
        lister_mock = mock.MagicMock()
        path = "/Users/s"
        self.assertEquals(["/Users/simon/"], CacheCompleter(cache, lister_mock).get_completions_with_update(path))
        lister_mock.hls_with_update_mock.assert_not_called()

    @mock.patch("hls_autocomplete.complete.Cache.load_cache")
    def testUpdate(self, load_cache_mock):
        cache = Cache({
            "Users": {
                "simon": {}
            }
        })
        path = "/Users/simon/D"

        updated_cache = Cache({
            "Users": {
                "simon": {
                    "Music": {},
                    "Documents": {},
                    "Dropbox": {}
                }
            }
        })

        load_cache_mock.return_value = updated_cache
        lister_mock = mock.MagicMock()
        lister_mock.hls_with_update.return_value = None

        self.assertEquals(["/Users/simon/Documents/", "/Users/simon/Dropbox/"],
                          CacheCompleter(cache, lister_mock).get_completions_with_update(path))


class TestGetPathToComplete(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEquals("/Users/simon", get_path_to_complete("/Users/simon/M"))
        self.assertEquals("/Users/simon", get_path_to_complete("/Users/simon/"))

class TestLoadCache(unittest.TestCase):
    @mock.patch("hls_autocomplete.complete.Cache.get_cache_path")
    def test_nominal_case(self, get_cache_path_mock):
        get_cache_path_mock.return_value = "/tmp/file"

        m = mock.mock_open(read_data='{"foo":{}}')
        with mock.patch("hls_autocomplete.complete.open", m, create=True):
            self.assertEqual(Cache({"foo": {}}), Cache.load_cache())

    @mock.patch("hls_autocomplete.complete.Cache.get_cache_path")
    def test_unexisting_file(self, get_cache_path_mock):
        get_cache_path_mock.return_value = "/tmp/unexisting_file"
        self.assertEqual(Cache({}), Cache.load_cache())

class TestIsValidPath(unittest.TestCase):
    def test_is_valid_path(self):
        self.assertTrue(is_valid_path("/Users/simon"))
        self.assertTrue(is_valid_path("/Users/simon/"))
        self.assertFalse(is_valid_path("/Users/simon/*/Music"))