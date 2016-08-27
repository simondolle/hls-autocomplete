import unittest
import get_completions
import update_completions

class TestGetCompletions(unittest.TestCase):

    def setUp(self):
        self.json = {
            "user": {
                "recocomputer": {
                    "bestofs": {"richcatalog":{}},
                    "dev": {
                        "s.dolle": {"img.jpg": {}},
                        "s.yachaoui": {},
                        "b.delayen": {}
                    }
                }
            }
        }

    def test_nominal_case(self):
        actual_result = get_completions.get_completions(
                "/user/recocomputer/dev/s.", self.json)
        expected_result = ["/user/recocomputer/dev/s.dolle/", "/user/recocomputer/dev/s.yachaoui/"]
        self.assertEquals(expected_result, actual_result)

    def test_directory_case(self):
        actual_result = get_completions.get_completions(
                "/user/recocomputer/dev/", self.json)
        expected_result = ["/user/recocomputer/dev/b.delayen/", "/user/recocomputer/dev/s.dolle/", "/user/recocomputer/dev/s.yachaoui/"]
        self.assertEquals(expected_result, actual_result)

    def test_unexisting_directory(self):
        actual_result = get_completions.get_completions(
                "/user/recocomputer/t", self.json)
        expected_result = []
        self.assertEquals(expected_result, actual_result)

    def test_too_long_path(self):
        actual_result = get_completions.get_completions(
                "/user/recocomputer/dev/s.dolle/toto", self.json)
        expected_result = []
        self.assertEquals(expected_result, actual_result)

    def test_root_only(self):
        actual_result = get_completions.get_completions(
                "/", self.json)
        expected_result = ["/user/"]
        self.assertEquals(expected_result, actual_result)

    def test_second_level(self):
        actual_result = get_completions.get_completions(
                "/user/re", self.json)
        expected_result = ["/user/recocomputer/"]
        self.assertEquals(expected_result, actual_result)

    def test_file_with_extension(self):
        actual_result = get_completions.get_completions(
                "/user/recocomputer/dev/s.dolle/im", self.json)
        expected_result = ["/user/recocomputer/dev/s.dolle/img.jpg"]
        self.assertEquals(expected_result, actual_result)

    def test_empty_json(self):
        actual_result = get_completions.get_completions(
                "/user", {})
        expected_result = []
        self.assertEquals(expected_result, actual_result)


class TestUpdateDirectory(unittest.TestCase):
    def setUp(self):
        self.json = {
            "user": {
                "recocomputer": {
                    "bestofs": {"richcatalog": {}},
                    "dev": {
                        "s.dolle": {"richcatalog": {}},
                        "s.yachaoui": {},
                        "b.delayen": {}
                    }
                }
            }
        }

    def test_new_directory(self):
        update_completions.update_directory("/user/recocomputer/bestofs/ussrPV",
                ["/user/recocomputer/bestofs/ussrPV/output1", "/user/recocomputer/bestofs/ussrPV/output2"],
                self.json)
        expected_cache = {
            "user": {
                "recocomputer": {
                    "bestofs": {"richcatalog": {},
                                "ussrPV" : {
                                    "output1": {},
                                    "output2": {}
                                    }
                                },
                    "dev": {
                        "s.dolle": {"richcatalog": {}},
                        "s.yachaoui": {},
                        "b.delayen": {}
                    }
                }
            }
        }
        self.assertEquals(expected_cache, self.json)

    def test_update_directory(self):
        update_completions.update_directory("/user/recocomputer/dev",
                ["/user/recocomputer/dev/s.dolle", "/user/recocomputer/dev/s.yachaoui", "/user/recocomputer/dev/pe.mazare"],
                self.json)
        expected_cache = {
            "user": {
                "recocomputer": {
                    "bestofs": {"richcatalog": {}},
                    "dev": {
                        "s.dolle": {"richcatalog": {}},
                        "s.yachaoui": {},
                        "pe.mazare": {}
                    }
                }
            }
        }
        self.assertEquals(expected_cache, self.json)

    def test_update_empty_cache(self):
        cache = {}
        update_completions.update_directory("/user/recocomputer/dev",
                 ["/user/recocomputer/dev/s.dolle", "/user/recocomputer/dev/s.yachaoui", "/user/recocomputer/dev/pe.mazare"],
                 cache)
        expected_cache = {
            "user": {
                "recocomputer": {
                    "dev": {
                        "s.dolle": {},
                        "s.yachaoui": {},
                        "pe.mazare": {}
                    }
                }
            }
        }
        self.assertEquals(expected_cache, cache)

class TestLsParser(unittest.TestCase):
    def test_nominal_case(self):
        parser = update_completions.LsParser()
        line = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Music"
        self.assertEquals("/Users/simon/Music", parser.parse_line(line))

    def test_space_in_name(self):
        parser = update_completions.LsParser()
        line = "drwx------+  8 simon  staff  272 27 dec  2015 /Users/simon/Personal Documents"
        self.assertEquals("/Users/simon/Personal Documents", parser.parse_line(line))





if __name__ == '__main__':
    unittest.main()
