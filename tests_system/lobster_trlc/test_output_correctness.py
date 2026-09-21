# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025-2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)
from tests_system.asserter import Asserter


class OutputCorrectnessTest(LobsterTrlcSystemTestCaseBase):
    """These tests verify the correctness of the output LOBSTER files"""

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_output_correctness(self):
        """Test that output is correlated to input.

           This tests uses data where each value is used only once in the whole input
           set, so we can verify that each output item is populated with data only
           based on one single input item.
        """
        # lobster-trace: UseCases.Incorrect_data_Extraction_from_TRLC
        self._test_runner.cmd_args.out = "output_correctness_test.out.lobster"
        self._test_runner.declare_output_file(
            self._data_directory / self._test_runner.cmd_args.out)

        config = self._test_runner.config_file_data

        config.inputs_from_file = "output_correctness_test_inputs.txt"
        for file in (
            "output_correctness_test.rsl",
            config.inputs_from_file,
        ):
            self._test_runner.copy_file_to_working_directory(
                self._data_directory / file,
            )

        for file in (
            "output_correctness_test_a.trlc",
            "output_correctness_test_b.trlc",
        ):
            self._test_runner.declare_input_file(self._data_directory / file)

        config.conversion_rules = [
            {
                "package": "output_correctness_test",
                "record-type": "TheType",
                "namespace": "req",
                "description-fields": [
                    "string",
                    "integer",
                    "decimal",
                    "boolean",
                    "strings",
                    "decimals",
                    "booleans",
                    "integers",
                    "references",
                ],
            }
        ]
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            "lobster-trlc: wrote 5 items to "
            "output_correctness_test.out.lobster\n",
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
