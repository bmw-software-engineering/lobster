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
from lobster.tools.cpptest.cpptest import (CODEBEAMER_URL, KIND,
                                           OUTPUT_FILE, SUPPORTED_KINDS)
from tests_system.lobster_cpptest.\
    lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from tests_system.asserter import Asserter
from lobster.common.exceptions import LOBSTER_Exception


class ConfigParserExceptionsCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.declare_input_file(self._data_directory / "test_case.cpp")

    def test_missing_config_file(self):
        """
        Tests that the yaml config file is missing and tool gives an error
        """
        # lobster-trace: cpptest_req.Config_File_Not_Found
        self._test_runner.cmd_args.config = str(
            self._data_directory / "non-existing.yaml")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        asserter.assertStdErrText(
            f'lobster-cpptest: {self._test_runner.cmd_args.config} '
            f'is not an existing file!\n'
        )
        asserter.assertExitCode(1)

    def test_config_file_errors(self):
        """
        Tests various yaml config file errors.
        """
        # lobster-trace: cpptest_req.Config_File_Invalid_Content
        test_cases = [
            {
                "config_file": "with_key_error.yaml",
                "expected_error": f'Missing attribute {CODEBEAMER_URL}',
                "case": "key_error",
                "expected_exit_code": 1
            },
            {
                "config_file": "with_list_of_output.yaml",
                "expected_error": f' {OUTPUT_FILE} must be a string',
                "case": "list_of_output",
                "expected_exit_code": 1
            },
            {
                "config_file": "with_list_of_kind.yaml",
                "expected_error": f'{KIND} must be a string',
                "case": "list_of_kind",
                "expected_exit_code": 1
            },
            {
                "config_file": "with_not_supported_kind.yaml",
                "expected_error": (
                    f'{KIND} must be one of {",".join(SUPPORTED_KINDS)}'
                ),
                "case": "not_supported_kind",
                "expected_exit_code": 1
            }
        ]

        for test_case in test_cases:
            with self.subTest(i=test_case["case"]):
                self._test_runner.cmd_args.config = str(
                    self._data_directory / test_case["config_file"]
                )

                completed_process = self._test_runner.run_tool_test()
                asserter = Asserter(self, completed_process, self._test_runner)

                asserter.assertInStdErr(test_case["expected_error"])
                asserter.assertExitCode(test_case["expected_exit_code"])

    def test_config_file_syntax_error(self):
        """
        Tests yaml config file syntax errors.
        """
        # lobster-trace: cpptest_req.Config_File_Invalid_YAML
        self._test_runner.cmd_args.config = str(
            self._data_directory / "with_syntax_error.yaml"
        )

        with self.assertRaises(LOBSTER_Exception) as ctx:
            self._test_runner.run_tool_test()
        self.assertIn("Invalid config file", ctx.exception.message)


if __name__ == "__main__":
    unittest.main()
