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
    LobsterReportSystemTestCaseBase)


class ReportResolveReferencesErrorsTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_unknown_tracing_target(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Unknown_Tracing_Target
        self._test_runner.declare_input_file(self._data_directory /
                                             "unknown_tracing_target.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_unknown_tracing_target.lobster")

        self._test_runner.cmd_args.lobster_config = "unknown_tracing_target.conf"
        self._test_runner.cmd_args.out = "report_unknown_tracing_target.lobster"
        self._test_runner.declare_output_file(self._data_directory /
                                              "report_unknown_tracing_target.lobster")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_tracing_destination_unversioned(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Tracing_Destination_Unversioned
        self._test_runner.declare_input_file(self._data_directory /
                                             "unversioned_trace.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_unversioned_trace_dest.lobster")

        self._test_runner.cmd_args.lobster_config = "unversioned_trace.conf"
        self._test_runner.cmd_args.out = "report_unversioned_trace_dest.lobster"
        self._test_runner.declare_output_file(self._data_directory /
                                              "report_unversioned_trace_dest.lobster")

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_tracing_destination_version_mismatch(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Tracing_Destination_Version_Mismatch
        self._test_runner.declare_input_file(self._data_directory /
                                             "version_mismatch_trace.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_ver_mismatch_trace_dest.lobster")

        self._test_runner.cmd_args.lobster_config = "version_mismatch_trace.conf"
        self._test_runner.cmd_args.out = "report_ver_mismatch_trace_dest.lobster"
        self._test_runner.declare_output_file(self._data_directory /
                                              "report_ver_mismatch_trace_dest.lobster")

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
