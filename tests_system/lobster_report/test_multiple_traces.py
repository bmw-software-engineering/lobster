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
from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase,
)


class ReportMultipleTracesTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_multiple_traces_justification(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: UseCases.Software_Test_to_Requirement_Mapping_in_output
        # lobster-trace: core_report_req.Multiple_Traces_Support
        # lobster-trace: core_report_req.Status_Justified_Up
        """
        This test checks that the lobster report tool can handle multiple lobster traces
         with justifications in code as well as tests
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_just.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_code.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_test.lobster")

        conf_file = "multiple_traces_just.conf"
        out_file = "report_multiple_traces_just.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
