import unittest

from hls_complete import get_completions

class TestSplitPath(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEquals(["user", "s.dolle", "Music"], get_completions.split_path("/user/s.dolle/Music"))
        self.assertEquals(["user", "s.dolle", "Music"], get_completions.split_path("/user/s.dolle/Music/"))

class TestAppendSlash(unittest.TestCase):
    def test_nominal_case(self):
        self.assertEquals("/user/s.dolle/Music/", get_completions.append_slash("/user/s.dolle/Music", True))
        self.assertEquals("/user/s.dolle/Music", get_completions.append_slash("/user/s.dolle/Music", False))
