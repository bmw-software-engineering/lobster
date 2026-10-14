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

import json
import unittest
from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase,
)


class ReportTracingStatusTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    # Tests for the report generation with different statuses
    # Status Ok
    def test_status_ok(self):
        # lobster-trace: core_report_req.Tracing_Policy_Written_To_Output_File
        # lobster-trace: core_report_req.Item_Status_Ok_When_Required_References_Present
        # lobster-trace: core_report_req.Report_Generation_For_Valid_Config_And_Inputs
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_ok.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_ok.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_ok.lobster")

        conf_file = "lobster_ok.conf"
        out_file = "report_ok.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_status_ok_when_no_references_required(self):
        # lobster-trace: core_report_req.Item_Status_Ok_When_No_References_Required
        self._test_runner.declare_input_file(self._data_directory /
                                             "unconstrained_level.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "unconstrained_level.lobster")

        out_file = "report_unconstrained_level.lobster"
        self._test_runner.cmd_args.lobster_config = "unconstrained_level.conf"
        self._test_runner.cmd_args.out = out_file

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)

        with open(
            self._test_runner.working_dir / out_file,
            encoding="UTF-8",
        ) as report_file:
            report = json.load(report_file)
        item = report["levels"][0]["items"][0]
        self.assertEqual("OK", item["tracing_status"])
        self.assertEqual(100.0, report["levels"][0]["coverage"])

    # Status Missing
    def test_status_missing(self):
        # lobster-trace: core_report_req.Tracing_Policy_Written_To_Output_File
        # lobster-trace: core_report_req.Item_Status_Missing_When_Reference_Absent
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_missing.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_missing.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_missing.lobster")

        conf_file = "lobster_missing.conf"
        out_file = "report_missing.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_status_missing_mixed(self):
        # lobster-trace: core_report_req.Tracing_Policy_Written_To_Output_File
        # lobster-trace: core_report_req.Item_Status_Missing_When_Reference_Absent
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_mixed.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_mixed.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_mixed.lobster")

        conf_file = "lobster_mixed.conf"
        out_file = "report_mixed.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    # Status Justified
    def test_status_justified(self):
        # lobster-trace: core_report_req.Tracing_Policy_Written_To_Output_File
        # lobster-trace: core_report_req.Item_Status_Justified_By_Justification
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_justified.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_justified.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_justified.lobster")

        conf_file = "lobster_justified.conf"
        out_file = "report_justified.lobster"
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
