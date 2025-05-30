from pathlib import Path
import shutil
from .lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from .lobster_cpptest_asserter import LobsterCppTestAsserter as Asserter
from ..tests_utils.update_cpptest_expected_output import update_cpptest_output_file


class ExtensionCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self.output_dir = Path(Path(__file__).parents[0] / "temp_data")

    def test_valid_extension_file(self):

        self._test_runner.cmd_args.config = str(
            self._data_directory / "valid_extension_config.yaml")
        self._test_runner.declare_input_file(
            self._data_directory / "valid_extension.cpp"
        )
        self.OUT_FILE = "valid_extension.lobster"
        self._test_runner.cmd_args.out = self.OUT_FILE

        self._test_runner.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / self.OUT_FILE))
        self._test_runner.declare_output_file(self.output_dir / self.OUT_FILE)

        update_cpptest_output_file(
            Path(self.output_dir / self.OUT_FILE),
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        self.assertIn('lobster items to', completed_process.stdout)
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(41, self.OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_invalid_extension_file(self):

        self._test_runner.cmd_args.config = str(
            self._data_directory / "invalid_extension_config.yaml")
        self._test_runner.declare_input_file(
            self._data_directory / "invalid_extension.xyz"
        )
        self.OUT_FILE = "invalid_extension.lobster"
        self._test_runner.cmd_args.out = self.OUT_FILE

        self._test_runner.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / self.OUT_FILE))
        self._test_runner.declare_output_file(self.output_dir / self.OUT_FILE)

        update_cpptest_output_file(
            Path(self.output_dir / self.OUT_FILE),
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        self.assertIn('lobster items to', completed_process.stdout)
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(40, self.OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_no_input_file(self):

        self._test_runner.cmd_args.config = str(
            self._data_directory / "no_input_file_config.yaml")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            f'usage: lobster-cpptest [-h] [-v, --version] [--config CONFIG]\n'
            f'lobster-cpptest: error: "no_input_file.cpp" is not a file or directory.\n'
        )
        asserter.assertExitCode(2)

    def tearDown(self):
        super().tearDown()
        if hasattr(self, "output_dir") and self.output_dir.is_dir():
            shutil.rmtree(self.output_dir)
