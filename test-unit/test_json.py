import unittest
from pathlib import PurePosixPath, PureWindowsPath

from lobster.tools.json import json


class Test_Json(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSynName(self):
        self.assertEqual(
            json.syn_test_name(PurePosixPath("foo/bar.json")),
            "foo.bar")
        self.assertEqual(
            json.syn_test_name(PurePosixPath("/foo/bar.json")),
            "foo.bar")
        self.assertEqual(
            json.syn_test_name(PureWindowsPath("foo\\bar.json")),
            "foo.bar")
        self.assertEqual(
            json.syn_test_name(PureWindowsPath("C:\\foo\\bar.json")),
            "foo.bar")
        self.assertEqual(
            json.syn_test_name(PurePosixPath("../../foo/./bar.json")),
            "foo.bar")
        self.assertEqual(
            json.syn_test_name(PureWindowsPath("..\\..\\foo\\.\\bar.json")),
            "foo.bar")
