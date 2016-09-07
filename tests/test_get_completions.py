import unittest
from hls_complete import get_completions
from hls_complete import update_completions
from hls_complete.update_completions import FileStatus


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
        actual_result = get_completions.get_completions(
                "/Users/simon/D", self.json)
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/"]
        self.assertEquals(expected_result, actual_result)

    def test_directory_case(self):
        actual_result = get_completions.get_completions(
                "/Users/simon/", self.json)
        expected_result = ["/Users/simon/Documents/", "/Users/simon/Dropbox/", "/Users/simon/Music/"]
        self.assertEquals(expected_result, actual_result)

    def test_unexisting_directory(self):
        actual_result = get_completions.get_completions(
                "/Users/toto/t", self.json)
        expected_result = []
        self.assertEquals(expected_result, actual_result)

    def test_too_long_path(self):
        actual_result = get_completions.get_completions(
                "/Users/simon/Documents/work/old", self.json)
        expected_result = []
        self.assertEquals(expected_result, actual_result)

    def test_root_only(self):
        actual_result = get_completions.get_completions(
                "/", self.json)
        expected_result = ["/Users/"]
        self.assertEquals(expected_result, actual_result)

    def test_second_level(self):
        actual_result = get_completions.get_completions(
                "/Users/si", self.json)
        expected_result = ["/Users/simon/"]
        self.assertEquals(expected_result, actual_result)

    def test_file_with_extension(self):
        actual_result = get_completions.get_completions(
                "/Users/simon/Documents/work/C", self.json)
        expected_result = ["/Users/simon/Documents/work/CV.doc"]
        self.assertEquals(expected_result, actual_result)

    def test_empty_json(self):
        actual_result = get_completions.get_completions(
                "/Users", {})
        expected_result = []
        self.assertEquals(expected_result, actual_result)


class TestUpdateDirectory(unittest.TestCase):
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

    def test_new_directory(self):
        update_completions.update_directory("/Users/simon/",
                [FileStatus("/Users/simon/Music", True),
                 FileStatus("/Users/simon/Documents", True),
                 FileStatus("/Users/simon/Dropbox", True),
                 FileStatus("/Users/simon/Pictures", True)],
                self.json)

        expected_cache = {
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
                    "Dropbox": {},
                    "Pictures": {}
                }
            }
        }
        self.assertEquals(expected_cache, self.json)

    def test_update_directory(self):
        update_completions.update_directory("/Users/simon",
                [FileStatus("/Users/simon/Music", True),
                    FileStatus("/Users/simon/Movies", True),
                    FileStatus("/Users/simon/Pictures", True)],
                self.json)
        expected_cache = {
            "Users": {
                "simon": {
                    "Music": {
                        "Spotify": {}
                    },
                    "Movies": {},
                    "Pictures": {}
                }
            }
        }
        self.assertEquals(expected_cache, self.json)

    def test_update_empty_cache(self):
        cache = {}
        update_completions.update_directory("/Users/simon",
                 [FileStatus("/Users/simon/Music", True),
                     FileStatus("/Users/simon/Movies", True)],
                 cache)
        expected_cache = {
            "Users": {
                "simon": {
                    "Music": {},
                    "Movies": {}
                }
            }
        }
        self.assertEquals(expected_cache, cache)

class TestLsParser(unittest.TestCase):
    def test_nominal_case(self):
        parser = update_completions.LsParser()
        line = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music"
        self.assertEquals(update_completions.FileStatus("/Users/simon/Music", True), parser.parse_line(line))

    def test_file_case(self):
        parser = update_completions.LsParser()
        line = "-rwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music"
        self.assertEquals(update_completions.FileStatus("/Users/simon/Music", False), parser.parse_line(line))

    def test_space_in_name(self):
        parser = update_completions.LsParser()
        line = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Personal Documents"
        self.assertEquals(update_completions.FileStatus("/Users/simon/Personal Documents", True), parser.parse_line(line))


class TestSplitPath(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEquals(["user", "s.dolle", "Music"], get_completions.split_path("/user/s.dolle/Music"))
        self.assertEquals(["user", "s.dolle", "Music"], get_completions.split_path("/user/s.dolle/Music/"))

class TestAppendSlash(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEquals("/user/s.dolle/Music/", get_completions.append_slash("/user/s.dolle/Music", True))
        self.assertEquals("/user/s.dolle/Music", get_completions.append_slash("/user/s.dolle/Music", False))


if __name__ == '__main__':
    unittest.main()
