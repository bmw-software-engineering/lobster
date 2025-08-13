from .lobster_pkg_system_test_case_base import LobsterPKGSystemTestCaseBase
from ..asserter import Asserter


class InputFilePkgTest(LobsterPKGSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_valid_input_pkg_file(self):
        OUT_FILE = "sample1.lobster"
        self._test_runner.cmd_args.files = [str(
            self._data_directory / "sample1.pkg")]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        self._test_runner.declare_output_file(
            self._data_directory / OUT_FILE)

        asserter = Asserter(self, completed_process, self._test_runner)

        asserter.assertNoStdErrText()
        self.assertIn('Written output for 1 items', completed_process.stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_valid_input_pkg_files(self):
        OUT_FILE = "sample1_and_sample2.lobster"
        self._test_runner.cmd_args.files = [str(
            self._data_directory / "sample1.pkg"),
            str(self._data_directory / "sample2.pkg")]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        self._test_runner.declare_output_file(
            self._data_directory / OUT_FILE)

        asserter = Asserter(self, completed_process, self._test_runner)

        asserter.assertNoStdErrText()
        self.assertIn('Written output for 2 items', completed_process.stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_valid_input_pkg_folder(self):
        OUT_FILE = "sample1_folder.lobster"
        self._test_runner.cmd_args.files = [str(
            self._data_directory / "pkg_files")]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        self._test_runner.declare_output_file(
            self._data_directory / OUT_FILE)

        asserter = Asserter(self, completed_process, self._test_runner)

        asserter.assertNoStdErrText()
        self.assertIn('Written output for 1 items', completed_process.stdout)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()