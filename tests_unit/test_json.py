# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2023-2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

import unittest
from pathlib import PurePosixPath, PureWindowsPath
from tempfile import NamedTemporaryFile

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
        with NamedTemporaryFile("w", delete=False):
            config = {"invalid_key": "This is an invalid key "
                                      "which is not supported by LOBSTER Json"}
        lobster_json = LOBSTER_Json()

        with self.assertRaises(KeyError):
            lobster_json.validate_yaml_supported_config_parameters(config)

    def test_mandatory_json_parameters(self):
        config = {"single": True, "name_attribute": "fruit"}
        lobster_json = LOBSTER_Json()

        with self.assertRaises(SystemExit):
            lobster_json.check_mandatory_config_parameters(config)
