import unittest
import mock

from hls_autocomplete.complete import get_completions, get_path_to_complete, get_completions_with_update

class TestGetCompletions(unittest.TestCase):

    def setUp(self):
        self.json = {
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
        }


    def test_nominal_case(self):
        actual_result = get_completions(
                "/Users/simon/D", self.json)
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/"]
        self.assertEquals(expected_result, actual_result)

    def test_directory_case(self):
        actual_result = get_completions(
                "/Users/simon/", self.json)
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/", "/Users/simon/Music/"]
        self.assertEquals(expected_result, actual_result)

    def test_directory_case(self):
        actual_result = get_completions(
                "/Users/simon/", self.json)
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/", "/Users/simon/Music/"]
        self.assertEquals(expected_result, actual_result)

    def test_unexisting_directory(self):
        actual_result = get_completions(
                "/Users/toto/t", self.json)
        expected_result = []
        self.assertEquals(expected_result, actual_result)

    def test_too_long_path(self):
        actual_result = get_completions(
                "/Users/simon/Documents/work/old", self.json)
        expected_result = []
        self.assertEquals(expected_result, actual_result)

    def test_double_slash(self):
        actual_result = get_completions(
            "/Users/simon//", self.json)
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/", "/Users/simon/Music/"]
        self.assertEquals(expected_result, actual_result)

    def test_root_only(self):
        actual_result = get_completions(
                "/", self.json)
        expected_result = ["/Users/"]
        self.assertEquals(expected_result, actual_result)

    def test_second_level(self):
        actual_result = get_completions(
                "/Users/si", self.json)
        expected_result = ["/Users/simon/"]
        self.assertEquals(expected_result, actual_result)

    def test_file_with_extension(self):
        actual_result = get_completions(
                "/Users/simon/Documents/work/C", self.json)
        expected_result = ["/Users/simon/Documents/work/CV.doc"]
        self.assertEquals(expected_result, actual_result)

    def test_empty_json(self):
        actual_result = get_completions(
                "/Users", {})
        expected_result = []
        self.assertEquals(expected_result, actual_result)

class TestGetCompletionsWithUpdate(unittest.TestCase):
    @mock.patch("hls_autocomplete.complete.hls_with_update")
    def testNoUpdate(self, hls_with_update_mock):
        cache = {
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
        }
        path = "/Users/s"
        self.assertEquals(["/Users/simon/"], get_completions_with_update(path, cache))
        hls_with_update_mock.assert_not_called()

    @mock.patch("hls_autocomplete.complete.hls_with_update")
    def testUpdate(self, hls_with_update_mock):
        cache = {
            "Users": {
                "simon": {}
            }
        }
        path = "/Users/simon/D"

        updated_cache = {
            "Users": {
                "simon": {
                    "Music": {},
                    "Documents": {},
                    "Dropbox": {}
                }
            }
        }
        hls_with_update_mock.return_value = (None, updated_cache)
        self.assertEquals(["/Users/simon/Documents/", "/Users/simon/Dropbox/"],
                          get_completions_with_update(path, cache))


class TestGetPathToComplete(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEquals("/Users/simon", get_path_to_complete("/Users/simon/M"))
        self.assertEquals("/Users/simon", get_path_to_complete("/Users/simon/"))
