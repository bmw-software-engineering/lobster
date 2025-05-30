from pathlib import Path
import shutil
from .lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from .lobster_cpptest_asserter import LobsterCppTestAsserter as Asserter
from ..tests_utils.update_cpptest_expected_output import update_cpptest_output_file


class ReferencesCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self.output_dir = Path(Path(__file__).parents[0] / "temp_data")

    def test_no_references_cpptest_file(self):
        # lobster-trace: UseCases.Incorrect_number_of_requirement_references_in_Output
        self.OUT_FILE = "no_references.lobster"
        self._test_runner.cmd_args.out = self.OUT_FILE
        self._test_runner.declare_input_file(self._data_directory / "no_references.cpp")
        self._test_runner.cmd_args.config = str(
            self._data_directory / "no_references_config.yaml")

        self._test_runner.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / self.OUT_FILE))
        self._test_runner.declare_output_file(self.output_dir / self.OUT_FILE)

        update_cpptest_output_file(
            Path(self.output_dir / self.OUT_FILE),
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(6, self.OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_one_reference_in_cpptest_file(self):
        # lobster-trace: UseCases.Incorrect_number_of_requirement_references_in_Output
        self.OUT_FILE = "1_reference.lobster"
        self._test_runner.cmd_args.out = self.OUT_FILE
        self._test_runner.declare_input_file(self._data_directory / "1_reference.cpp")
        self._test_runner.cmd_args.config = str(
            self._data_directory / "1_reference_config.yaml")

        self._test_runner.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / self.OUT_FILE))
        self._test_runner.declare_output_file(self.output_dir / self.OUT_FILE)

        update_cpptest_output_file(
            Path(self.output_dir / self.OUT_FILE),
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(7, self.OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_many_references_in_cpptest_file(self):
        # lobster-trace: UseCases.Incorrect_number_of_requirement_references_in_Output
        self.OUT_FILE = "many_references.lobster"
        self._test_runner.cmd_args.out = self.OUT_FILE
        self._test_runner.declare_input_file(
            self._data_directory / "many_references.cpp")
        self._test_runner.cmd_args.config = str(
            self._data_directory / "many_references_config.yaml")

        self._test_runner.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / self.OUT_FILE))
        self._test_runner.declare_output_file(self.output_dir / self.OUT_FILE)

        update_cpptest_output_file(
            Path(self.output_dir / self.OUT_FILE),
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(13, self.OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def tearDown(self):
        super().tearDown()
        if hasattr(self, "output_dir") and self.output_dir.is_dir():
            shutil.rmtree(self.output_dir)
