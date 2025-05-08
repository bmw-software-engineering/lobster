from .lobster_UI_system_test_case_base import LobsterUISystemTestCaseBase
from ..asserter import Asserter
from lobster.tools.core.html_report.html_report import is_dot_available


class LobsterHtmlReportInputFileTest(LobsterUISystemTestCaseBase):
    """System test case for LOBSTER HTML report with different .lobster
       file scenarios."""

    def setUp(self):
        super().setUp()
        self.test_runner = self.create_test_runner()

    def test_lobster_file_is_missing(self):
        # lobster-trace: html_req.Missing_Lobster_File
        """Verify the tool fails gracefully when the .lobster file does not exist."""
        missing_lobster_file = self._data_directory / "missing.lobster"
        self.test_runner.cmd_args.lobster_report = str(missing_lobster_file)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)

        expected_stderr = (
            "usage: lobster-html-report [-h] [-v, --version] [--out OUT] [--dot DOT]\n"
            "                           [--high-contrast] [--render-md]\n"
            "                           [lobster_report]\n"
            f"lobster-html-report: error: {str(missing_lobster_file)} is not a file\n"
        )

        asserter.assertStdErrText(expected_stderr)
        asserter.assertExitCode(2)

    def test_valid_lobster_file_succeeds(self):
        # lobster-trace: html_req.Valid_Lobster_File
        """Verify the tool runs successfully with a valid .lobster file."""
        output_filename = "is_actually_html.output"
        valid_inputfile = self._data_directory / "awesome.output"

        self.test_runner.declare_output_file(self._data_directory / output_filename)
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.lobster_report = str(valid_inputfile)

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

    def test_lobster_file_with_20k_records(self):
        # lobster-trace: html_req.HTML_Report_with_20k_records

        dot_present = is_dot_available(dot=None)
        if dot_present:
            output = "records_20k_tracing_policy.output"
        else:
            output = "records_20k.output"
        input = self._data_directory / "report_20k.lobster"

        self.test_runner.declare_output_file(self._data_directory / output)
        self.test_runner.cmd_args.out = output
        self.test_runner.cmd_args.lobster_report = str(input)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)

        if dot_present:
            expected_stdout = f"LOBSTER HTML report written to {output}\n"

        else:
            expected_stdout = (
                "warning: dot utility not found, report will not include "
                "the tracing policy visualisation\n"
                "> please install Graphviz (https://graphviz.org)\n"
                f"LOBSTER HTML report written to {output}\n"
            )

        asserter.assertStdOutText(expected_stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_custom_data_displayed_in_report(self):
        # lobster-trace: html_req.HTML_Report_Displays_Custom_data
        """Verify that 'custom_data' values are correctly
        displayed in the HTML report header."""
        dot_present = is_dot_available(dot=None)
        if dot_present:
            output = "custom_data_tracing_policy.output"
        else:
            output = "custom_data.output"
        input = self._data_directory / "custom_data_report.lobster"

        self.test_runner.declare_output_file(self._data_directory / output)
        self.test_runner.cmd_args.out = output
        self.test_runner.cmd_args.lobster_report = str(input)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)
        if dot_present:
            expected_stdout = f"LOBSTER HTML report written to {output}\n"
        else:
            expected_stdout = (
                "warning: dot utility not found, report will not include "
                "the tracing policy visualisation\n"
                "> please install Graphviz (https://graphviz.org)\n"
                f"LOBSTER HTML report written to {output}\n"
            )

        asserter.assertStdOutText(expected_stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_valid_md_lobster_file_succeeds(self):
        # lobster-trace: html_req.Valid_Lobster_File_With_Md_Content
        """Verify tool runs successfully with a valid .lobster file with md content."""
        output_filename = "to_render_md_content.output"
        valid_inputfile = self._data_directory / "to_render_md_content.lobster"

        self.test_runner.declare_output_file(self._data_directory / output_filename)
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.render_md = True
        self.test_runner.cmd_args.lobster_report = str(valid_inputfile)

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
