import unittest
import datetime

from hls_autocomplete.parse import FileStatus, LsParser, WebHdfsParser, get_file_statuses_pretty_print

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

    def test_french_month(self):
        parser = LsParser()
        line = "drwx------+  8 simon  staff  272 27 jui  2015 /Users/simon/Personal Documents"
        self.assertEquals(FileStatus("/Users/simon/Personal Documents", "drwx------+", 8, "simon", "staff", 272, datetime.date(2015, 6, 27)), parser.parse_line(line))

    def test_current_year(self):
        parser = LsParser()
        line = "drwx------+  8 simon  staff  272 27 jui  12:15 /Users/simon/Personal Documents"
        self.assertEquals(FileStatus("/Users/simon/Personal Documents", "drwx------+", 8, "simon", "staff", 272, datetime.date(datetime.datetime.now().year, 6, 27)), parser.parse_line(line))

    def test_invalid_lines(self):
        parser = LsParser()
        self.assertEquals(None, parser.parse_line("8 simon  staff  272 27 dec  2015 /Users/simon/Personal Documents"))
        self.assertEquals(None, parser.parse_line("drwx------+  8 simon  staff  272 27 dec  2015"))
        self.assertEquals(None, parser.parse_line("foo bar"))

    def test_parse(self):
        parser = LsParser()
        lines = ("foo bar\n"
            "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music\n"
            "drwx------+  8 simon  staff  272 17 nov  2014 /Users/simon/Documents\n")
        expected_result = [FileStatus("/Users/simon/Music", "drwx------+", 8, "simon", "staff", 272,  datetime.date(2015, 12, 27)),
                           FileStatus("/Users/simon/Documents", "drwx------+", 8, "simon", "staff", 272, datetime.date(2014, 11, 17))]

        self.assertEqual(expected_result, parser.parse(lines))

class TestWebHdfsParser(unittest.TestCase):
    def test_permissions_to_unix_name(self):
        parser = WebHdfsParser(None)
        self.assertEqual("-rwxrwxrwx", parser.permissions_to_unix_name(False, "777"))
        self.assertEqual("-rw-rwxr--", parser.permissions_to_unix_name(False, "674"))
        self.assertEqual("d---------", parser.permissions_to_unix_name(True, "000"))
        self.assertEqual("-rw-rwxr-t", parser.permissions_to_unix_name(False, "1674"))

    def test_parse_status(self):
        parser = WebHdfsParser("/foo")
        input = {"pathSuffix": "bar", "type": "DIRECTORY", "length": 0, "owner": "simon", "group": "staff",
             "permission": "700", "accessTime": 0, "modificationTime": 1461236412807, "blockSize": 0, "replication": 0}
        expected_result = FileStatus("/foo/bar", "drwx------", 0, "simon", "staff", 0, datetime.date(2016, 04, 21),"bar")
        self.assertEqual(expected_result, parser.parse_status(input))

    def test_parse(self):
        input = '''{"FileStatuses": {"FileStatus": [
            {"pathSuffix": "bar", "type": "DIRECTORY", "length": 0, "owner": "simon", "group": "staff",
             "permission": "700", "accessTime": 0, "modificationTime": 1461236412807, "blockSize": 0, "replication": 0},
            {"pathSuffix": "qux", "type": "FILE", "length": 0, "owner": "simon",
             "group": "staff", "permission": "775", "accessTime": 0, "modificationTime": 1473691319065,
             "blockSize": 0, "replication": 0}]}}'''
        parser = WebHdfsParser("/foo")

        expected_result = [
            FileStatus("/foo/bar", "drwx------", 0, "simon", "staff", 0, datetime.date(2016, 4, 21), "bar"),
            FileStatus("/foo/qux", "-rwxrwxr-x", 0, "simon", "staff", 0, datetime.date(2016, 9, 12), "qux")
        ]
        self.assertEqual(expected_result, parser.parse(input))

class TestGetFileStatutesPrettyPrint(unittest.TestCase):
    def test_nominal_case(self):
        file_statuses = [
            FileStatus("/foo/bar/qux", "drwx------", 0, "simon.dolle", "staff", 0, datetime.date(2016, 4, 21), "bar"),
            FileStatus("/foo/qux", "-rwxrwxr-x", 0, "simon", "root", 0, datetime.date(2016, 9, 12), "qux")
        ]

        expected_result = ("drwx------  0 simon.dolle  staff  0 21 apr  2016 /foo/bar/qux\n"
                           "-rwxrwxr-x  0       simon   root  0 12 sep  2016     /foo/qux")
        self.assertEqual(expected_result, get_file_statuses_pretty_print(file_statuses))

