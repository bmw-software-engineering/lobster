from .lobster_pkg_asserter import LobsterPkgAsserter
from .lobster_pkg_system_test_case_base import LobsterPKGSystemTestCaseBase


class InvalidInputFilePkgTest(LobsterPKGSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_not_existing_pkg_file(self):
        OUT_FILE = "not_existing.lobster"
        non_existing_file = str(
            self._data_directory / "not_existing.pkg")
        self._test_runner.cmd_args.files = [non_existing_file]

        self._test_runner.cmd_args.out = OUT_FILE

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertInStdErr(f'{non_existing_file} is not a file or directory')
        asserter.assertExitCode(1)

    def test_not_existing_output_path(self):
        OUT_FILE = "not_existing/not_existing.lobster"
        self._test_runner.cmd_args.files = [
            str(self._data_directory / "valid_file1.pkg")
        ]

        self._test_runner.cmd_args.out = OUT_FILE

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertInStdErr(f'No such file or directory: \'{OUT_FILE}\'')
        asserter.assertExitCode(1)

    def test_misplaced_lobster_trace_file(self):
        OUT_FILE = "report.lobster"
        misplaced_lobster_trace_file = str(
            self._data_directory / "misplaced_lobster_trace.pkg")
        self._test_runner.cmd_args.files = [misplaced_lobster_trace_file]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        expected_output = (
            'WARNING: misplaced lobster-trace in misplaced_lobster_trace.pkg: '
            'lobster-trace: misplaced.req1,misplaced.req2\n'
            'Written output for 1 items to report.lobster\n'
        )
        asserter.assertStdOutText(expected_output)
        asserter.assertExitCode(0)

    def test_misplaced_tags_file(self):
        OUT_FILE = "report.lobster"
        misplaced_tags_file_name = "misplaced_tags.pkg"
        misplaced_tags_file_path = str(
            self._data_directory / misplaced_tags_file_name)
        self._test_runner.cmd_args.files = [misplaced_tags_file_path]
        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        expected_output = (
            f'LOBSTER Error: Misplaced LOBSTER tag(s) in file '
            f'{misplaced_tags_file_name} at line(s): [63]\n'
        )
        asserter.assertStdOutText(expected_output)
        asserter.assertExitCode(1)

    def test_invalid_xml_file(self):
        OUT_FILE = "report.lobster"
        invalid_xml_file_name = "invalid_xml.pkg"
        invalid_xml_file_path = str(
            self._data_directory / invalid_xml_file_name)
        self._test_runner.cmd_args.files = [invalid_xml_file_path]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        expected_output = (
            f"Error parsing XML file '{invalid_xml_file_name}' : "
            f"mismatched tag: line 13, column 2\n"
        )
        asserter.assertStdOutText(expected_output)
        asserter.assertExitCode(1)

    def test_invalid_input_pkg_file_without_output_argument(self):
        self._test_runner.cmd_args.files = [
            str(self._data_directory / "valid_file1.pkg")
        ]

        completed_process = self._test_runner.run_tool_test()

        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)

        asserter.assertExitCode(2)
        asserter.assertInStdErr("the following arguments are required: --out")
