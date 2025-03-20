import unittest
import re
from pathlib import PurePosixPath, PureWindowsPath
from tempfile import NamedTemporaryFile

import yaml

from lobster.errors import LOBSTER_Error
from lobster.tools.json import json
from lobster.tools.json.json import LOBSTER_Json


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

    def test_invalid_json_parameters(self):
        with NamedTemporaryFile("w", delete=False) as temp:
            yaml.dump({"invalid_key": "This is a invalid key "
                                      "which not supported by LOBSTER Json"}, temp)
            temp_path = temp.name
        lobster_json = LOBSTER_Json()

        with self.assertRaises(LOBSTER_Error):
            lobster_json.validate_yaml_supported_config_parameters(temp_path)

    def test_mandatory_json_parameters(self):
        config = {"single": True, "name_attribute": "fruit"}
        lobster_json = LOBSTER_Json()

        with self.assertRaises(SystemExit):
            lobster_json.check_mandatory_config_parameters(config)
