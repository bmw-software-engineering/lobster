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

from pathlib import Path
import unittest
from tests_system.lobster_html_report.lobster_UI_system_test_case_base import (
    LobsterUISystemTestCaseBase)
from tests_system.asserter import Asserter
from tests_system.tests_utils.update_version_in_html import update_version_in_html_file
from tests_system.tests_utils.update_html_expected_output import update_html_output_file


class LobsterOnlineReportInputTest(LobsterUISystemTestCaseBase):
    """System test case for LOBSTER HTML report with different .lobster
       file scenarios."""

    def setUp(self):
        super().setUp()
        self.test_runner = self.create_test_runner()
        self.output_dir = Path(Path(__file__).parents[0])

    def test_online_report_input(self):
        # lobster-trace: html_req.HTML_Report_Lists_Lobster_Items
        # lobster-trace: html_req.HTML_Report_Displays_Coverage_Value
        # lobster-trace: html_req.HTML_Report_Uses_Valid_HTML_Syntax
        # lobster-trace: html_req.Item_Data_Unique
        """
        Tests the input file 'online report' is processed
        and links are generated correctly in the HTML report.
        the online report file is created using complex tracing policy
        which contains requirements, code and tests.
        """
        output_filename = "pizza_online.html"
        valid_inputfile = self._data_directory / "pizza_online_report.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / output_filename))
        self.test_runner.declare_output_file(self.output_dir / output_filename)

        update_version_in_html_file(
            self.output_dir / output_filename,
        )

        update_html_output_file(
            self.output_dir / output_filename,
            self.output_dir
        )

        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.lobster_report = str(valid_inputfile)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)

        expected_stdout = f"LOBSTER HTML report written to {output_filename}\n"

        self.assertIn(
            f"LOBSTER HTML report written to {output_filename}\n",
            completed_process.stdout,
        )
        self.assertIn(expected_stdout, completed_process.stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
