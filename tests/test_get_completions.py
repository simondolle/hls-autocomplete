import unittest
from hls_complete import get_completions
from hls_complete import update_completions
from hls_complete.update_completions import FileStatus


class TestGetCompletions(unittest.TestCase):

    def setUp(self):
        self.json = {
            "is_dir": True,
            "content": {
                "user": {
                    "is_dir": True,
                    "content": {
                        "recocomputer": {
                            "is_dir": True,
                            "content": {
                                "bestofs": {
                                    "is_dir": True,
                                    "content": {
                                        "richcatalog":{
                                            "is_dir": True,
                                            "content": {}}
                                    }
                                },
                                "dev": {
                                    "is_dir": True,
                                    "content": {
                                        "s.dolle": {
                                            "is_dir": True,
                                            "content": {
                                                "img.jpg": {
                                                    "is_dir": False
                                                }
                                            },
                                        },
                                        "s.yachaoui": {
                                            "is_dir": True,
                                            "content": {}
                                        },
                                        "b.delayen": {
                                             "is_dir": True,
                                            "content": {}
                                        }
                                    }
                                }
                            }
                        }
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
        #self.maxDiff = None
        self.json = {
            "is_dir": True,
            "content": {
                    "user": {
                        "is_dir": True,
                        "content": {
                            "recocomputer": {
                                "is_dir": True,
                                "content": {
                                    "bestofs": {
                                        "is_dir": True,
                                        "content": {
                                            "richcatalog": {
                                                "is_dir": True,
                                                "content": {}
                                                }
                                            }
                                        },
                                    "dev": {
                                        "is_dir": True,
                                        "content": {
                                            "s.dolle": {
                                                "is_dir": True,
                                                "content": {
                                                    "richcatalog": {"is_dir": True, "content": {}}}
                                                },
                                            "s.yachaoui": {"is_dir": True, "content": {}},
                                            "b.delayen": {"is_dir": True, "content": {}}
                                        }
                                    }
                                }
                            }
                        }
                    }
            }
        }

    def test_new_directory(self):
        update_completions.update_directory("/user/recocomputer/bestofs/ussrPV",
                [FileStatus("/user/recocomputer/bestofs/ussrPV/output1", True),
                    FileStatus("/user/recocomputer/bestofs/ussrPV/output2", True)],
                self.json)

        expected_cache = {
            "is_dir": True,
            "content": {
                    "user": {
                        "is_dir": True,
                        "content": {
                            "recocomputer": {
                                "is_dir": True,
                                "content": {
                                    "bestofs": {
                                        "is_dir": True,
                                        "content": {
                                            "richcatalog": {
                                                "is_dir": True,
                                                "content": {}
                                            },

                                            "ussrPV": {
                                                "is_dir": True,
                                                "content": {
                                                    "output1": {"is_dir": True, "content": {}},
                                                    "output2": {"is_dir": True, "content": {}}
                                                }
                                            }
                                        }
                                    },
                                    "dev": {
                                        "is_dir": True,
                                        "content": {
                                            "s.dolle": {
                                                "is_dir": True,
                                                "content": {
                                                    "richcatalog": {"is_dir": True, "content": {}}}
                                                },
                                            "s.yachaoui": {"is_dir": True, "content": {}},
                                            "b.delayen": {"is_dir": True, "content": {}}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

        self.assertEquals(expected_cache, self.json)

    def test_update_directory(self):
        update_completions.update_directory("/user/recocomputer/dev",
                [FileStatus("/user/recocomputer/dev/s.dolle", True),
                    FileStatus("/user/recocomputer/dev/s.yachaoui", True),
                    FileStatus("/user/recocomputer/dev/pe.mazare", True)],
                self.json)
        expected_cache = {
            "is_dir": True,
            "content": {
                    "user": {
                        "is_dir": True,
                        "content": {
                            "recocomputer": {
                                "is_dir": True,
                                "content": {
                                    "bestofs": {
                                        "is_dir": True,
                                        "content": {
                                            "richcatalog": {
                                                "is_dir": True,
                                                "content": {}
                                            },
                                        }
                                    },
                                    "dev": {
                                        "is_dir": True,
                                        "content": {
                                            "s.dolle": {
                                                "is_dir": True,
                                                "content": {
                                                    "richcatalog": {"is_dir": True, "content": {}}}
                                                },
                                            "s.yachaoui": {"is_dir": True, "content": {}},
                                            "pe.mazare": {"is_dir": True, "content": {}}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        self.assertEquals(expected_cache, self.json)

    def test_update_empty_cache(self):
        cache = {
            "is_dir": True,
            "content": {}
        }
        update_completions.update_directory("/user/recocomputer/dev",
                 [FileStatus("/user/recocomputer/dev/s.dolle", True),
                     FileStatus("/user/recocomputer/dev/s.yachaoui", True),
                     FileStatus("/user/recocomputer/dev/pe.mazare", True)],
                 cache)
        expected_cache = {
            "is_dir": True,
            "content": {
                "user": {
                    "is_dir": True,
                    "content": {
                        "recocomputer": {
                            "is_dir": True,
                            "content": {
                                "dev": {
                                    "is_dir": True,
                                    "content": {
                                        "s.dolle": {"is_dir": True, "content": {}},
                                        "s.yachaoui": {"is_dir": True, "content": {}},
                                        "pe.mazare": {"is_dir": True, "content": {}}
                                    }
                                }
                            }
                        }
                    }
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





if __name__ == '__main__':
    unittest.main()
