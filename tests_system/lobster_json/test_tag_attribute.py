# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
from tests_system.lobster_json.\
    lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase
from tests_system.lobster_json.lobsterjsonasserter import LobsterJsonAsserter


class JsonTagAttributeTest(LobsterJsonSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_tag_attribute_given(self):
        # lobster-trace: json_req.Tag_Attribute_Given
        self._test_runner.declare_input_file(
            self._data_directory / "tag_attribute_given.json")
        self._test_runner.config_file_data.tag_attribute = "Requirements"
        out_file = "tag_attribute_requirements.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(8, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_tag_attribute_given_but_key_missing(self):
        # lobster-trace: json_req.Tag_Attribute_Given_Key_Missing
        self._test_runner.declare_input_file(
            self._data_directory / "tag_attribute_given_key_missing.json")
        self._test_runner.config_file_data.tag_attribute = "missingkey"
        out_file = "tag_attribute_irrelavent.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(4, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_tag_attribute_missing(self):
        # lobster-trace: json_req.Config_File_Mandatory_Parameter_Missing
        self._test_runner.declare_input_file(self._data_directory / "basic.json")
        # Intentionally not setting tag_attribute (it's mandatory)

        completed_process = self._test_runner.run_tool_test()
        self.assertEqual(
            completed_process.returncode,
            "Required mandatory parameters missing - tag_attribute",
        )


if __name__ == "__main__":
    unittest.main()
