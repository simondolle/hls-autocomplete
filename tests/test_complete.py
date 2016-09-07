import unittest
from hls_complete import complete

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
        actual_result = complete.get_completions(
                "/Users/simon/D", self.json)
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/"]
        self.assertEquals(expected_result, actual_result)

    def test_directory_case(self):
        actual_result = complete.get_completions(
                "/Users/simon/", self.json)
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/", "/Users/simon/Music/"]
        self.assertEquals(expected_result, actual_result)

    def test_unexisting_directory(self):
        actual_result = complete.get_completions(
                "/Users/toto/t", self.json)
        expected_result = []
        self.assertEquals(expected_result, actual_result)

    def test_too_long_path(self):
        actual_result = complete.get_completions(
                "/Users/simon/Documents/work/old", self.json)
        expected_result = []
        self.assertEquals(expected_result, actual_result)

    def test_root_only(self):
        actual_result = complete.get_completions(
                "/", self.json)
        expected_result = ["/Users/"]
        self.assertEquals(expected_result, actual_result)

    def test_second_level(self):
        actual_result = complete.get_completions(
                "/Users/si", self.json)
        expected_result = ["/Users/simon/"]
        self.assertEquals(expected_result, actual_result)

    def test_file_with_extension(self):
        actual_result = complete.get_completions(
                "/Users/simon/Documents/work/C", self.json)
        expected_result = ["/Users/simon/Documents/work/CV.doc"]
        self.assertEquals(expected_result, actual_result)

    def test_empty_json(self):
        actual_result = complete.get_completions(
                "/Users", {})
        expected_result = []
        self.assertEquals(expected_result, actual_result)
