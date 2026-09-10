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
    LobsterReportSystemTestCaseBase
)


class ReportJustificationTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_justification_and_coverage(self):
        # lobster-trace: core_report_req.Tracing_Policy_Written_To_Output_File
        # lobster-trace: core_report_req.Level_Coverage_Percentage_From_Item_Status
        # lobster-trace: core_report_req.Item_Status_Ok_When_Required_References_Present
        # lobster-trace: core_report_req.Item_Status_Justified_By_Justification
        # lobster-trace: core_report_req.Item_Status_Partial_One_Direction_Satisfied
        # lobster-trace: core_report_req.Item_Status_Missing_When_Reference_Absent
        """
        This test checks that the lobster report tool can handle justifications
        and coverage changes according to justifications and generate lobster report.
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_policy.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_usecases.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_system_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_software_requirements.lobster")

        conf_file = "just_policy.conf"
        out_file = "just_report.lobster"
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
