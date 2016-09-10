import unittest

from hls_autocomplete.update import FileStatus, update_directory, LsParser, is_valid_path

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
        update_directory("/Users/simon/",
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
        update_directory("/Users/simon",
                [FileStatus("/Users/simon/Music", True),
                    FileStatus("/Users/simon/Movies", True),
                    FileStatus("/Users/simon/Pictures", True),
                    FileStatus("/Users/simon/CV.doc", False),
                 ],
                self.json)
        expected_cache = {
            "Users": {
                "simon": {
                    "Music": {
                        "Spotify": {}
                    },
                    "Movies": {},
                    "Pictures": {},
                    "CV.doc": None
                }
            }
        }
        self.assertEquals(expected_cache, self.json)

    def test_update_empty_cache(self):
        cache = {}
        update_directory("/Users/simon",
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

    def test_update_invalid_path(self):
        update_directory("/Users/*",
                         [FileStatus("/Users/simon/Music", True),
                          FileStatus("/Users/simon/Movies", True),
                          FileStatus("/Users/simon/Pictures", True),
                          FileStatus("/Users/simon/CV.doc", False),
                          ],
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
                    "Dropbox": {}
                }
            }
        }
        self.assertEquals(expected_cache, self.json)

    def test_is_valid_path(self):
        self.assertTrue(is_valid_path("/Users/simon"))
        self.assertTrue(is_valid_path("/Users/simon/"))
        self.assertFalse(is_valid_path("/Users/simon/*/Music"))

class TestLsParser(unittest.TestCase):
    def test_nominal_case(self):
        parser = LsParser()
        line = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music"
        self.assertEquals(FileStatus("/Users/simon/Music", True), parser.parse_line(line))

    def test_file_case(self):
        parser = LsParser()
        line = "-rwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music"
        self.assertEquals(FileStatus("/Users/simon/Music", False), parser.parse_line(line))

    def test_space_in_name(self):
        parser = LsParser()
        line = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Personal Documents"
        self.assertEquals(FileStatus("/Users/simon/Personal Documents", True), parser.parse_line(line))

    def test_invalid_lines(self):
        parser = LsParser()
        self.assertEquals(None, parser.parse_line("8 simon  staff  272 27 dec  2015 /Users/simon/Personal Documents"))
        self.assertEquals(None, parser.parse_line("drwx------+  8 simon  staff  272 27 dec  2015"))

    def test_parse(self):
        parser = LsParser()
        lines = ("foo bar\n"
            "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music\n"
            "drwx------+  8 simon  staff  272 17 nov  2014 /Users/simon/Documents\n")
        expected_result = [FileStatus("/Users/simon/Music", True),
                           FileStatus("/Users/simon/Documents", True)]

        self.assertEqual(expected_result, parser.parse(lines))