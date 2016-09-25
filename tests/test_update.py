import unittest
import datetime

from hls_autocomplete.complete import Cache
from hls_autocomplete.update import FileStatus, LsParser

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
        self.cache = Cache(self.json)

    "drwx------+  8 simon  staff  272 17 nov  2014"
    def test_new_directory(self):
        cache = self.cache.update_directory("/Users/simon/",
                [FileStatus("/Users/simon/Music", True, "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20)),
                 FileStatus("/Users/simon/Documents", True, "drwx------+", 8, "simon", "staff", 300, datetime.date(2015, 3, 10)),
                 FileStatus("/Users/simon/Dropbox", True, "drwx------+", 3, "simon", "staff", 272, datetime.date(2016, 8, 20)),
                 FileStatus("/Users/simon/Pictures", True, "drwx------+", 8, "simon", "staff", 180, datetime.date(2015, 10, 28))])

        expected_cache = Cache({
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
        })
        self.assertEquals(expected_cache, cache)

    def test_update_directory(self):
        cache = self.cache.update_directory("/Users/simon",
                    [FileStatus("/Users/simon/Music", True, "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20)),
                    FileStatus("/Users/simon/Movies", True, "drwx------+", 8, "simon", "staff", 180, datetime.date(2016, 4, 7)),
                    FileStatus("/Users/simon/Pictures", True, "drwx------+", 8, "simon", "staff", 180, datetime.date(2015, 10, 28)),
                    FileStatus("/Users/simon/CV.doc", False, "-rwx------+", 1, "simon", "staff", 1180, datetime.date(2015, 10, 4)),
                 ])
        expected_cache = Cache({
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
        })
        self.assertEquals(expected_cache, cache)

    def test_update_empty_cache(self):
        cache = Cache({})
        cache = cache.update_directory("/Users/simon",
                 [FileStatus("/Users/simon/Music", True, "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20)),
                     FileStatus("/Users/simon/Movies", True, "drwx------+", 8, "simon", "staff", 180, datetime.date(2016, 4, 7))])
        expected_cache = Cache({
            "Users": {
                "simon": {
                    "Music": {},
                    "Movies": {}
                }
            }
        })
        self.assertEquals(expected_cache, cache)

    def test_update_invalid_path(self):
        cache = self.cache.update_directory("/Users/*",
                         [FileStatus("/Users/simon/Music", True, "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 11, 20)),
                          FileStatus("/Users/simon/Movies", True, "drwx------+", 8, "simon", "staff", 180, datetime.date(2016, 4, 7)),
                          FileStatus("/Users/simon/Pictures", True, "drwx------+", 8, "simon", "staff", 180, datetime.date(2015, 10, 28)),
                          FileStatus("/Users/simon/CV.doc", False, "-rwx------+", 1, "simon", "staff", 1180, datetime.date(2015, 10, 4)),
                          ])
        expected_cache = Cache({
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
        self.assertEquals(expected_cache, cache)

class TestLsParser(unittest.TestCase):
    def test_nominal_case(self):
        parser = LsParser()
        line = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music"
        self.assertEquals(FileStatus("/Users/simon/Music", True, "drwx------+", 8, "simon", "staff",  272, datetime.date(2015, 12, 27)), parser.parse_line(line))

    def test_file_case(self):
        parser = LsParser()
        line = "-rwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music"
        self.assertEquals(FileStatus("/Users/simon/Music", False, "-rwx------+", 8, "simon", "staff", 272, datetime.date(2015, 12, 27)), parser.parse_line(line))

    def test_space_in_name(self):
        parser = LsParser()
        line = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Personal Documents"
        self.assertEquals(FileStatus("/Users/simon/Personal Documents", True, "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 12, 27)), parser.parse_line(line))

    def test_invalid_lines(self):
        parser = LsParser()
        self.assertEquals(None, parser.parse_line("8 simon  staff  272 27 dec  2015 /Users/simon/Personal Documents"))
        self.assertEquals(None, parser.parse_line("drwx------+  8 simon  staff  272 27 dec  2015"))

    def test_parse(self):
        parser = LsParser()
        lines = ("foo bar\n"
            "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music\n"
            "drwx------+  8 simon  staff  272 17 nov  2014 /Users/simon/Documents\n")
        expected_result = [FileStatus("/Users/simon/Music", True, "drwx------+", 8, "simon", "staff", 272,  datetime.date(2015, 12, 27)),
                           FileStatus("/Users/simon/Documents", True, "drwx------+", 8, "simon", "staff", 272, datetime.date(2014, 11, 17))]

        self.assertEqual(expected_result, parser.parse(lines))