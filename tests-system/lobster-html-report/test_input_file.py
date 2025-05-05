from .lobster_UI_system_test_case_base import LobsterUISystemTestCaseBase
from ..asserter import Asserter


class TestLobsterHtmlReportInputFile(LobsterUISystemTestCaseBase):
    """System test case for LOBSTER HTML report with different .lobster
       file scenarios."""

    def setUp(self):
        super().setUp()
        self.test_runner = self.create_test_runner()

    def test_lobster_file_is_missing(self):
        # lobster-trace: html_req.Missing_Lobster_File_Error
        """Verify the tool fails gracefully when the .lobster file does not exist."""
        missing_lobster_file = self._data_directory / "missing.lobster"
        self.test_runner.cmd_args.lobster_report = str(missing_lobster_file)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)

        expected_stderr = (
            "usage: lobster-html-report [-h] [-v, --version] [--out OUT] [--dot DOT]\n"
            "                           [--high-contrast]\n"
            "                           [lobster_report]\n"
            f"lobster-html-report: error: {str(missing_lobster_file)} is not a file\n"
        )

        asserter.assertStdErrText(expected_stderr)
        asserter.assertStdOutText("")
        asserter.assertExitCode(2)

    def test_valid_lobster_file_succeeds(self):
        # lobster-trace: html_req.Valid_Lobster_File_Success
        """Verify the tool runs successfully with a valid .lobster file."""
        output_filename = "is_actually_html.output"
        valid_inputfile = self._data_directory / "awesome.output"

        self.test_runner.declare_output_file(self._data_directory / output_filename)
        self.test_runner.cmd_args.out = output_filename
        self.test_runner.cmd_args.lobster_report = str(valid_inputfile)

        completed_process = self.test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self.test_runner)

        expected_stdout = (
            "warning: dot utility not found, report will not include "
            "the tracing policy visualisation\n"
            "> please install Graphviz (https://graphviz.org)\n"
            f"LOBSTER HTML report written to {output_filename}\n"
        )

        asserter.assertStdErrText("")
        asserter.assertStdOutText(expected_stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
