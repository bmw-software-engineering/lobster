from pathlib import Path
import unittest
from tests_system.lobster_cpptest.\
    lobster_cpptest_asserter import LobsterCppTestAsserter as Asserter
from tests_system.lobster_cpptest.\
    lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from tests_system.tests_utils.\
    update_cpptest_expected_output import update_cpptest_output_file


class MultipleFilesCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self.output_dir = Path(Path(__file__).parents[0])

    def test_multiple_files(self):
        """
        Test case for processing multiple input files.
        Ensures the tool runs on files specified in the yaml config file and
        generates expected output.
        """
        # lobster-trace: UseCases.Incorrect_Number_of_Cpp_Tests_in_Output
        # lobster-trace: UseCases.Incorrect_number_of_requirement_references_in_Output
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
        self._test_runner.declare_output_file(self.output_dir /
                                              OUT_FILE)

        update_cpptest_output_file(
            self.output_dir / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFileDeprecated(22, OUT_FILE, "lobster-act-trace", 3)
        asserter.assertExitCode(0)
        # asserter.assertOutputFiles()

    def test_multiple_files_no_schema(self):
        """
        Test case for processing multiple input files.
        Ensures the tool runs on files specified in the yaml config file and
        generates expected output.
        """
        # lobster-trace: UseCases.Incorrect_Number_of_Cpp_Tests_in_Output
        # lobster-trace: UseCases.Incorrect_number_of_requirement_references_in_Output
        OUT_FILE = "multiple_files_no_schema.lobster"
        self._test_runner.cmd_args.config = str(
            self._data_directory / "multiple_files_config_no_kind.yaml")
        self._test_runner.declare_input_file(self._data_directory / "multi1.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi2.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi3.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi4.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi5.cpp")

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / OUT_FILE))
        self._test_runner.declare_output_file(self.output_dir /
                                              OUT_FILE)

        update_cpptest_output_file(
            self.output_dir / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(22, OUT_FILE)
        asserter.assertExitCode(0)
        # asserter.assertOutputFiles()

    def test_multiple_valid_invalid_files(self):
        """
        Test for processing multiple input files in a directory with valid and invalid
        extensions. Ensures the tool runs on all files in the directory and generates
        output for all valid files in the directory.
        """
        # lobster-trace: UseCases.Incorrect_Number_of_Cpp_Tests_in_Output
        # lobster-trace: UseCases.Incorrect_number_of_requirement_references_in_Output
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
        self._test_runner.declare_output_file(self.output_dir /
                                              OUT_FILE)

        update_cpptest_output_file(
            self.output_dir / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFileDeprecated(33, OUT_FILE, "lobster-act-trace", 3)
        asserter.assertExitCode(0)
        # asserter.assertOutputFiles()

    def test_multiple_valid_invalid_files_no_schema(self):
        """
        Test for processing multiple input files in a directory with valid and invalid
        extensions. Ensures the tool runs on all files in the directory and generates
        output for all valid files in the directory.
        """
        # lobster-trace: UseCases.Incorrect_Number_of_Cpp_Tests_in_Output
        # lobster-trace: UseCases.Incorrect_number_of_requirement_references_in_Output
        OUT_FILE = "valid_invalid_files_no_schema.lobster"
        self._test_runner.cmd_args.config = str(
            self._data_directory / "valid_invalid_files_config_no_kind.yaml")
        self._test_runner.declare_input_file(self._data_directory / "multi1.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi2.cpp")
        self._test_runner.declare_input_file(self._data_directory / "multi3.cpp")
        self._test_runner.declare_input_file(self._data_directory / "dir_file1.abc")
        self._test_runner.declare_input_file(self._data_directory / "dir_file2.ppp")

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / OUT_FILE))
        self._test_runner.declare_output_file(self.output_dir /
                                              OUT_FILE)

        update_cpptest_output_file(
            self.output_dir / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(33, OUT_FILE)
        asserter.assertExitCode(0)
        # asserter.assertOutputFiles()

    def test_no_input_file(self):
        """
        Test case for handling the scenario where the input file does not exist.
        An input file provided in YAML config file which does not exist in working
        directory.
        """
        # lobster-trace: UseCases.Incorrect_Number_of_Cpp_Tests_in_Output
        self._test_runner.cmd_args.config = str(
            self._data_directory / "no_input_file_config.yaml")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            'lobster-cpptest: "no_input_file.cpp" is not a file or directory.\n'
        )
        asserter.assertExitCode(1)

    def test_no_input_file_no_kind(self):
        """
        Test case for handling the scenario where the input file does not exist.
        An input file provided in YAML config file which does not exist in working
        directory.
        """
        # lobster-trace: UseCases.Incorrect_Number_of_Cpp_Tests_in_Output
        self._test_runner.cmd_args.config = str(
            self._data_directory / "no_input_file_config_no_kind.yaml")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            'lobster-cpptest: "no_input_file.cpp" is not a file or directory.\n'
        )
        asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
