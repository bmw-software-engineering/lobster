from pathlib import Path
from tests_system.lobster_html_report.lobster_UI_system_test_case_base import (
    LobsterUISystemTestCaseBase)
from tests_system.asserter import Asserter
from lobster.tools.core.html_report.html_report import is_dot_available
from tests_system.tests_utils.update_version_in_html import update_version_in_html_file


class LobsterHtmlReportcontentTest(LobsterUISystemTestCaseBase):
    """System test case for LOBSTER HTML report with different .lobster
       file scenarios."""

    def setUp(self):
        super().setUp()
        self.test_runner = self.create_test_runner()
        self.output_dir = Path(Path(__file__).parents[0])

    def test_item_unique_data(self):
        # lobster-trace: html_req.Item_Data_Unique
        """
        This test checks that the data is not mixed
        and unique data in each item processed correctly
        """
        output_filename = "octopus.output"
        inputfile2 = self._data_directory / "report_octopus.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / output_filename))
        self.test_runner.declare_output_file(self.output_dir / output_filename)

        update_version_in_html_file(
            self.output_dir / output_filename,
        )
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.render_md = True
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
        # lobster-trace: html_req.Complex_Tracing_Policy_Data
        """
        This test checks that the data created using complex tracing
        policy is processed correctly.
        """
        output_filename = "pizza.output"
        inputfile = self._data_directory / "report_pizza.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / output_filename))
        self.test_runner.declare_output_file(self.output_dir / output_filename)

        update_version_in_html_file(
            self.output_dir / output_filename,
        )
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.render_md = True
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
        # lobster-trace: html_req.Selective_Input_File_Processing
        """
        This test checks that the tool shall process only the provided input file
        and ignore all other files in the working directory.
        """
        output_filename = "pizza.output"
        inputfile1 = self._data_directory / "report_pizza.lobster"
        inputfile2 = self._data_directory / "report_octopus.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / output_filename))
        self.test_runner.declare_output_file(self.output_dir / output_filename)

        update_version_in_html_file(
            self.output_dir / output_filename,
        )
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.render_md = True
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

    def test_html_content_with_justifications(self):
        # lobster-trace: html_req.Processing_Data_With_Justifications
        """
        This test checks that the data containing the justifications
        is processed and displays content correctly according to the justifications.
        """
        output_filename = "just.output"
        inputfile = self._data_directory / "report_just.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / output_filename))
        self.test_runner.declare_output_file(self.output_dir / output_filename)

        update_version_in_html_file(
            self.output_dir / output_filename,
        )
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.render_md = True
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
