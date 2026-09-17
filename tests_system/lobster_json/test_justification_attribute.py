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


class JsonJustificationAttributeTest(LobsterJsonSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.tag_attribute = "RequirementIDs"
        self._test_runner.config_file_data.name_attribute = "Name"

    def test_justification_attribute_given(self):
        self._test_runner.declare_input_file(
            self._data_directory / "justification_attribute_given.json")

        self._test_runner.config_file_data.justification_attribute = "Justification"
        out_file = "justification_attribute_given.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(7, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_justification_attribute_given_but_key_missing(self):
        self._test_runner.declare_input_file(
            self._data_directory / "justification_attribute_given.json")

        self._test_runner.config_file_data.justification_attribute = "missingkey"

        out_file = "justification_attribute_irrelavent.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(7, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_justification_attribute_not_given(self):
        self._test_runner.declare_input_file(
            self._data_directory / "justification_attribute_given.json")

        out_file = "justification_attribute_not_given.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(7, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
