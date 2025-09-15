from pathlib import Path
import unittest
from tests_system.lobster_html_report.lobster_UI_system_test_case_base import (
    LobsterUISystemTestCaseBase)
from tests_system.asserter import Asserter
from tests_system.tests_utils.update_version_in_html import update_version_in_html_file
from lobster.tools.core.html_report.html_report import is_dot_available


class LobsterHtmlReportcontentTest(LobsterUISystemTestCaseBase):
    """System test case for LOBSTER HTML report with different .lobster
       file scenarios."""

    def setUp(self):
        super().setUp()
        self.test_runner = self.create_test_runner()
        self.output_dir = Path(Path(__file__).parents[0])

    def test_item_unique_data(self):
        # lobster-trace: html_req.Item_Data_Unique
        # lobster-trace: UseCases.Correct_Item_Data
        # lobster-trace: UseCases.Coverage_in_output
        # lobster-trace: UseCases.HTML_file_generation
        # lobster-trace: UseCases.Covered_Requirement_list_in_HTML_file
        # lobster-trace: UseCases.List_of_tests_Not_covering_requirements_in_HTML_file
        # lobster-trace: UseCases.List_of_tests_covering_requirements_in_HTML_file
        # lobster-trace: UseCases.Source_location_in_output
        # lobster-trace: UseCases.Missing_tracing_policy_violation_in_output
        """
        This test checks that the data is not mixed
        and unique data in each item processed correctly
        """
        output_filename = "octopus.html"
        inputfile2 = self._data_directory / "report_octopus.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / output_filename))
        self.test_runner.declare_output_file(self.output_dir / output_filename)

        update_version_in_html_file(
            self.output_dir / output_filename,
        )
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.lobster_report = str(inputfile2)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)

        if is_dot_available(dot=None):
            expected_stdout = f"LOBSTER HTML report written to {output_filename}\n"

        else:
            expected_stdout = (
                "warning: dot utility not found, report will not include "
                "the tracing policy visualisation\n"
                "> please install Graphviz (https://graphviz.org)\n"
                f"LOBSTER HTML report written to {output_filename}\n"
            )

        asserter.assertStdOutText(expected_stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_complex_tracing_policy_data(self):
        # lobster-trace: UseCases.Correct_Item_Data
        # lobster-trace: UseCases.Coverage_in_output
        # lobster-trace: UseCases.HTML_file_generation
        # lobster-trace: UseCases.List_of_tests_covering_requirements_in_HTML_file
        # lobster-trace: UseCases.Covered_Requirement_list_in_HTML_file
        # lobster-trace: UseCases.Source_location_in_output
        """
        This test checks that the data created using complex tracing
        policy is processed correctly.
        """
        output_filename = "pizza.html"
        inputfile = self._data_directory / "report_pizza.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / output_filename))
        self.test_runner.declare_output_file(self.output_dir / output_filename)

        update_version_in_html_file(
            self.output_dir / output_filename,
        )
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.lobster_report = str(inputfile)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)

        if is_dot_available(dot=None):
            expected_stdout = f"LOBSTER HTML report written to {output_filename}\n"

        else:
            expected_stdout = (
                "warning: dot utility not found, report will not include "
                "the tracing policy visualisation\n"
                "> please install Graphviz (https://graphviz.org)\n"
                f"LOBSTER HTML report written to {output_filename}\n"
            )

        asserter.assertStdOutText(expected_stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_multiple_input_files_in_working_directory(self):
        # lobster-trace: html_req.Only_Given_Input_File_Consumed
        # lobster-trace: UseCases.Coverage_in_output
        # lobster-trace: UseCases.HTML_file_generation
        # lobster-trace: UseCases.Covered_Requirement_list_in_HTML_file
        # lobster-trace: UseCases.Correct_Item_Data
        # lobster-trace: UseCases.List_of_tests_covering_requirements_in_HTML_file
        # lobster-trace: UseCases.Source_location_in_output
        """
        This test checks that the tool shall process only the provided input file
        and ignore all other files in the working directory.
        """
        output_filename = "pizza.html"
        inputfile1 = self._data_directory / "report_pizza.lobster"
        inputfile2 = self._data_directory / "report_octopus.lobster"

        self.test_runner.declare_input_file(inputfile1)
        self.test_runner.declare_input_file(inputfile2)
        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / output_filename))
        self.test_runner.declare_output_file(self.output_dir / output_filename)

        update_version_in_html_file(
            self.output_dir / output_filename,
        )
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.lobster_report = str(inputfile1)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)

        if is_dot_available(dot=None):
            expected_stdout = f"LOBSTER HTML report written to {output_filename}\n"

        else:
            expected_stdout = (
                "warning: dot utility not found, report will not include "
                "the tracing policy visualisation\n"
                "> please install Graphviz (https://graphviz.org)\n"
                f"LOBSTER HTML report written to {output_filename}\n"
            )

        asserter.assertStdOutText(expected_stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_html_content_with_multiple_status(self):
        # lobster-trace: html_req.Processing_Data_With_Justifications
        # lobster-trace: UseCases.Correct_Item_Data
        # lobster-trace: UseCases.Coverage_in_output
        # lobster-trace: UseCases.Source_location_in_output
        # lobster-trace: UseCases.HTML_file_generation
        # lobster-trace: UseCases.Not_covered_Requirement_list_in_Output
        # lobster-trace: UseCases.Missing_tracing_policy_violation_in_output
        """
        This test checks that the tool processes data containing the items
        with multiple status like ok, missing, partial, justified
        and displays content correctly according to its status.
        """
        output_filename = "all_status.html"
        inputfile = self._data_directory / "report_all_status.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / output_filename))
        self.test_runner.declare_output_file(self.output_dir / output_filename)

        update_version_in_html_file(
            self.output_dir / output_filename,
        )
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.lobster_report = str(inputfile)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)

        if is_dot_available(dot=None):
            expected_stdout = f"LOBSTER HTML report written to {output_filename}\n"

        else:
            expected_stdout = (
                "warning: dot utility not found, report will not include "
                "the tracing policy visualisation\n"
                "> please install Graphviz (https://graphviz.org)\n"
                f"LOBSTER HTML report written to {output_filename}\n"
            )

        asserter.assertStdOutText(expected_stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_codebeamer_links(self):
        # lobster-trace: UseCases.Source_location_in_output
        # lobster-trace: UseCases.Correct_Item_Data
        # lobster-trace: UseCases.Coverage_in_output
        # lobster-trace: UseCases.HTML_file_generation
        # lobster-trace: UseCases.Covered_Requirement_list_in_HTML_file
        """
        This test checks that the HTML report has codebeamer links
        It also covers that the correct codebeamer links i.e codebeamer source location
        is included in output
        """
        output_filename = "codebeamer_links.html"
        inputfile = self._data_directory / "codebeamer_links.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / output_filename))
        self.test_runner.declare_output_file(self.output_dir / output_filename)

        update_version_in_html_file(
            self.output_dir / output_filename,
        )
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.lobster_report = str(inputfile)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)

        if is_dot_available(dot=None):
            expected_stdout = f"LOBSTER HTML report written to {output_filename}\n"

        else:
            expected_stdout = (
                "warning: dot utility not found, report will not include "
                "the tracing policy visualisation\n"
                "> please install Graphviz (https://graphviz.org)\n"
                f"LOBSTER HTML report written to {output_filename}\n"
            )

        asserter.assertStdOutText(expected_stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_message_in_item(self):
        # lobster-trace: UseCases.Correct_Item_Data
        # lobster-trace: UseCases.Coverage_in_output
        # lobster-trace: UseCases.HTML_file_generation
        # lobster-trace: UseCases.Covered_Requirement_list_in_HTML_file
        # lobster-trace: UseCases.List_of_tests_Not_covering_requirements_in_HTML_file
        # lobster-trace: UseCases.List_of_tests_covering_requirements_in_HTML_file
        # lobster-trace: UseCases.Source_location_in_output
        # lobster-trace: UseCases.Missing_tracing_policy_violation_in_output
        """
        This test checks the input .lobster file has a content in message attributes
        and HTML tool correctly processes it and write correct output file.
        """
        output_filename = "octopus.html"
        inputfile = self._data_directory / "report_octopus.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / output_filename))
        self.test_runner.declare_output_file(self.output_dir / output_filename)

        update_version_in_html_file(
            self.output_dir / output_filename,
        )
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.lobster_report = str(inputfile)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)

        if is_dot_available(dot=None):
            expected_stdout = f"LOBSTER HTML report written to {output_filename}\n"

        else:
            expected_stdout = (
                "warning: dot utility not found, report will not include "
                "the tracing policy visualisation\n"
                "> please install Graphviz (https://graphviz.org)\n"
                f"LOBSTER HTML report written to {output_filename}\n"
            )

        asserter.assertStdOutText(expected_stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
