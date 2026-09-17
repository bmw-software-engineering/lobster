# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
from tests_system.lobster_json.lobsterjsonasserter import LobsterJsonAsserter
from tests_system.lobster_json.lobsterjsonsystemtestcasebase import (
    LobsterJsonSystemTestCaseBase
)


class InvalidJsonTest(LobsterJsonSystemTestCaseBase):
    """Test cases for handling invalid JSON input files"""

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.tag_attribute = "RequirementIDs"

    def test_empty_json_file(self):
        """
        Test that lobster-json handles empty JSON files gracefully.
        Expected: tool exits with return code 1 and prints proper error to stderr.
        """
        # lobster-trace: json_req.Empty_JSON_File_Handling
        out_file = "empty_json.lobster"
        input_file = "empty_file.json"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.declare_input_file(
            self._data_directory / input_file
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertStdErrEqual(f"{input_file}: Input file contains invalid JSON.\n")
        asserter.assertExitCode(1)

    def test_invalid_json_content(self):
        """
        Test that lobster-json handles invalid JSON content gracefully.
        The tool should exit with code 1 and print error to stderr.
        """
        out_file = "invalid_content.lobster"
        input_file = "valid_extension_invalid_json.json"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.declare_input_file(
            self._data_directory / input_file
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterJsonAsserter(self, completed_process, self._test_runner)
        asserter.assertStdErrEqual(f"{input_file}: Input file contains invalid JSON.\n")
        asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
