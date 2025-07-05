import shutil
from pathlib import Path
from .lobster_cpptest_asserter import LobsterCppTestAsserter as Asserter
from .lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from ..tests_utils.update_cpptest_expected_output import update_cpptest_output_file


class MultipleFilesCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self.output_dir = Path(Path(__file__).parents[0])

    def test_multiple_files(self):
        """
        Test case for processing multiple input files.
        Test to ensure that the tool runs on the files
        specified in the configuration file
        and generates the expected output file.
        """
        # lobster-trace: Usecases.Incorrect_Number_of_Cpp_Tests_in_Output
        # lobster-trace: Usecases.Incorrect_number_of_requirement_references_in_Output
        OUT_FILE = "multiple_files.lobster"
        self._test_runner.cmd_args.config = str(
            self._data_directory / "multiple_files_config.yaml")
        self._test_runner.declare_input_file(self._data_directory / "multi1.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi2.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi3.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi4.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi5.cpp")

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / OUT_FILE))
        self._test_runner.declare_output_file(Path(self.output_dir.name) /
                                              OUT_FILE)

        update_cpptest_output_file(
            Path(self.output_dir.name) / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(22, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_multiple_valid_invalid_files(self):
        """
        Test case for processing multiple input files in a directory
        that contain valid and invalid extensions.
        Test to ensure that the tool runs on all files in the specified directory
        and generates the expected output file.
        """
        # lobster-trace: Usecases.Incorrect_Number_of_Cpp_Tests_in_Output
        # lobster-trace: Usecases.Incorrect_number_of_requirement_references_in_Output
        OUT_FILE = "valid_invalid_files.lobster"
        self._test_runner.cmd_args.config = str(
            self._data_directory / "valid_invalid_files_config.yaml")
        self._test_runner.declare_input_file(self._data_directory / "multi1.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi2.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi3.cpp")
        self._test_runner.declare_input_file(self._data_directory / "dir_file1.abc")
        self._test_runner.declare_input_file(self._data_directory / "dir_file2.ppp")

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / OUT_FILE))
        self._test_runner.declare_output_file(Path(self.output_dir.name) /
                                              OUT_FILE)

        update_cpptest_output_file(
            Path(self.output_dir.name) / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(33, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_no_input_file(self):
        """
        Test case for handling the scenario where
        the input file does not exist.
        This test ensures that the tool correctly identifies
        the absence of the input file
        and returns an appropriate error message.
        """
        # lobster-trace: Usecases.Incorrect_Number_of_Cpp_Tests_in_Output
        self._test_runner.cmd_args.config = str(
            self._data_directory / "no_input_file_config.yaml")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            f'usage: lobster-cpptest [-h] [-v] [--config CONFIG]\n'
            f'lobster-cpptest: error: "no_input_file.cpp" is not a file or directory.\n'
        )
        asserter.assertExitCode(2)
