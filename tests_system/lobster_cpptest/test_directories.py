from pathlib import Path
import shutil
import unittest

from tests_system.lobster_cpptest.\
    lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from tests_system.lobster_cpptest.\
    lobster_cpptest_asserter import LobsterCppTestAsserter as Asserter
from tests_system.tests_utils.\
    update_cpptest_expected_output import update_cpptest_output_file


class DirectoriesCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_all_files_from_current_directory_consumed(self):
        """
        Tests that all C++ files in the current directory are consumed.
        It also picks files from nested directories.
        """
        # lobster-trace: UseCases.Incorrect_Number_of_Cpp_Tests_in_Output
        OUT_FILE = "nested_directories.lobster"

        self._test_runner.declare_input_file(self._data_directory / "no_references.cpp")
        self._test_runner.declare_input_file(
            self._data_directory / "many_references.cpp")
        self._test_runner.declare_input_file(self._data_directory / "1_reference.cpp")
        self._test_runner.declare_input_file(self._data_directory / "test_case.cpp")

        # Copy the "cpp_test_files" directory into the working directory
        source_dir = Path(self._data_directory / "cpp_test_files")
        dest_dir = Path(self._test_runner.working_dir / "cpp_test_files")
        shutil.copytree(source_dir, dest_dir)

        self.output_dir = Path(Path(__file__).parents[0])
        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / OUT_FILE))

        self._test_runner.declare_output_file(self.output_dir /
                                              OUT_FILE)
        self._test_runner.cmd_args.config = str(
            self._data_directory / "nested_directories.yaml")

        update_cpptest_output_file(
            self.output_dir / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(101, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_files_from_specified_directory_consumed(self):
        """
        Test for processing files from a specific directory.
        """
        # lobster-trace: UseCases.Incorrect_Number_of_Cpp_Tests_in_Output
        OUT_FILE = "specific_directory.lobster"

        # Copy the "cpp_test_files" directory into the working directory
        source_dir = Path(self._data_directory / "cpp_test_files")
        dest_dir = Path(self._test_runner.working_dir / "cpp_test_files")
        shutil.copytree(source_dir, dest_dir)

        self.output_dir = Path(Path(__file__).parents[0])
        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / OUT_FILE))

        self._test_runner.declare_output_file(self.output_dir /
                                              OUT_FILE)
        self._test_runner.cmd_args.config = str(
            self._data_directory / "specific_directory_config.yaml")

        update_cpptest_output_file(
            self.output_dir / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(30, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_specified_directory_and_files_consumed(self):
        """
        Test for processing files from a specific directory
        as well as files provided as input.
        """
        # lobster-trace: UseCases.Incorrect_Number_of_Cpp_Tests_in_Output
        OUT_FILE = "directory_files.lobster"

        self._test_runner.declare_input_file(self._data_directory / "no_references.cpp")
        self._test_runner.declare_input_file(self._data_directory / "1_reference.cpp")

        # Copy the "cpp_test_files" directory into the working directory
        source_dir = Path(self._data_directory / "cpp_test_files")
        dest_dir = Path(self._test_runner.working_dir / "cpp_test_files")
        shutil.copytree(source_dir, dest_dir)

        self.output_dir = Path(Path(__file__).parents[0])
        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / OUT_FILE))

        self._test_runner.declare_output_file(self.output_dir /
                                              OUT_FILE)
        self._test_runner.cmd_args.config = str(
            self._data_directory / "directory_files_config.yaml")

        update_cpptest_output_file(
            self.output_dir / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(43, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_no_cpptest_file(self):
        """
        Test case for handling the scenario where no .cpp test files are found.
        No input file provided in YAML config file or in working directory.
        """
        OUT_FILE = "no_cpptest_file.lobster"

        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)
        self._test_runner.cmd_args.config = str(
            self._data_directory / "cpptest-config.yaml")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            'lobster-cpptest: "[\'.\']" does not contain any test file.\n')
        asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
