import unittest
import datetime

from hls_autocomplete.update import FileStatus, LsParser

class TestFileStatus(unittest.TestCase):
    def test_str(self):
        fileStatus = FileStatus("/Users/simon/Music", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 12, 27))
        self.assertEquals("drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music", str(fileStatus))

class TestLsParser(unittest.TestCase):
    def test_nominal_case(self):
        parser = LsParser()
        line = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music"
        self.assertEquals(FileStatus("/Users/simon/Music", "drwx------+", 8, "simon", "staff",  272, datetime.date(2015, 12, 27)), parser.parse_line(line))

    def test_file_case(self):
        parser = LsParser()
        line = "-rwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music"
        self.assertEquals(FileStatus("/Users/simon/Music", "-rwx------+", 8, "simon", "staff", 272, datetime.date(2015, 12, 27)), parser.parse_line(line))

    def test_space_in_name(self):
        parser = LsParser()
        line = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Personal Documents"
        self.assertEquals(FileStatus("/Users/simon/Personal Documents", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 12, 27)), parser.parse_line(line))

    def test_invalid_lines(self):
        parser = LsParser()
        self.assertEquals(None, parser.parse_line("8 simon  staff  272 27 dec  2015 /Users/simon/Personal Documents"))
        self.assertEquals(None, parser.parse_line("drwx------+  8 simon  staff  272 27 dec  2015"))

    def test_parse(self):
        parser = LsParser()
        lines = ("foo bar\n"
            "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music\n"
            "drwx------+  8 simon  staff  272 17 nov  2014 /Users/simon/Documents\n")
        expected_result = [FileStatus("/Users/simon/Music", "drwx------+", 8, "simon", "staff", 272,  datetime.date(2015, 12, 27)),
                           FileStatus("/Users/simon/Documents", "drwx------+", 8, "simon", "staff", 272, datetime.date(2014, 11, 17))]

        self.assertEqual(expected_result, parser.parse(lines))