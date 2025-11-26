from pathlib import Path
import unittest
from tests_system.lobster_html_report.lobster_UI_system_test_case_base import (
    LobsterUISystemTestCaseBase)
from tests_system.lobster_html_report.\
    lobster_UI_system_asserter import LobsterUIAsserter as Asserter
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
        # lobster-trace: UseCases.Source_location_in_output
        # lobster-trace: UseCases.HTML_file_generation
        # lobster-trace: UseCases.Correct_Item_Data
        # lobster-trace: UseCases.Coverage_in_output
        # lobster-trace: UseCases.List_of_tests_covering_requirements_in_HTML_file
        # lobster-trace: UseCases.Covered_Requirement_list_in_HTML_file
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
