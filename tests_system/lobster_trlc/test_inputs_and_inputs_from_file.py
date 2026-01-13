import unittest
from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)
from tests_system.asserter import Asserter


class InputFromFilesAndInputsTest(LobsterTrlcSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._setup_basic_test_runner()

    def _setup_basic_test_runner(self):
        """
        Helper function to set up a test runner with common configuration.
        This can be reused and extended by individual tests as needed.
        """
        self._test_runner = self.create_test_runner()
        self._test_runner.declare_input_file(self._data_directory / "default_file.rsl")
        self._test_runner.declare_input_file(self._data_directory / "default_file.trlc")

    def test_input_from_files_and_inputs_list(self):
        """
        Test that inputs from files and inputs list can be processed together.
        """
        # lobster-trace: trlc_req.Input_list_Of_File_And_Inputs_From_File
        # lobster-trace: UseCases.Incorrect_data_Extraction_from_TRLC
        self._test_runner.config_file_data.conversion_rules = [
            self.BERRY_CONVERSION_RULE,
            self.NAMASTE_CONVERSION_RULE,
        ]
        OUT_FILE = "input_from_files_and_inputs.lobster"
        for extra_file in (False, True):
            with self.subTest(f"{extra_file=}"):
                if extra_file:
                    self._test_runner.copy_files_in_working_directory(
                        [self._data_directory / "fruits.trlc"]
                    )
                self._test_runner.cmd_args.out = OUT_FILE
                self._test_runner.declare_output_file(self._data_directory / OUT_FILE)
                self._test_runner.declare_inputs_from_file(
                    self._data_directory / "input_from_files_and_inputs.txt",
                    self._data_directory
                )
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        lobster_schema = "lobster-req-trace"
        lobster_version = 4
        asserter.assertStdOutText(
            f"Lobster file version {lobster_version} containing 'schema' = '{lobster_schema}' is deprecated, "
            f"please migrate to version 5\n"
            f"lobster-trlc: wrote 2 items to "
            f"{OUT_FILE}\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_input_from_files_and_inputs_list_no_schema(self):
        """
        Test that inputs from files and inputs list can be processed together.
        """
        # lobster-trace: trlc_req.Input_list_Of_File_And_Inputs_From_File
        # lobster-trace: UseCases.Incorrect_data_Extraction_from_TRLC
        self._test_runner.config_file_data.conversion_rules = [
            self.BERRY_CONVERSION_RULE_NO_SCHEMA,
            self.NAMASTE_CONVERSION_RULE_NO_SCHEMA,
        ]
        OUT_FILE = "input_from_files_and_inputs_no_schema.lobster"
        for extra_file in (False, True):
            with self.subTest(f"{extra_file=}"):
                if extra_file:
                    self._test_runner.copy_files_in_working_directory(
                        [self._data_directory / "fruits.trlc"]
                    )
                self._test_runner.cmd_args.out = OUT_FILE
                self._test_runner.declare_output_file(self._data_directory / OUT_FILE)
                self._test_runner.declare_inputs_from_file(
                    self._data_directory / "input_from_files_and_inputs.txt",
                    self._data_directory
                )
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"lobster-trlc: wrote 2 items to "
                                  f"{OUT_FILE}\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_duplicate_contents_input_from_files_and_inputs_list(self):
        """
        Test that duplicates in inputs from files and inputs list cause an error
        """
        # lobster-trace: trlc_req.Duplicate_Input_list_Of_File_And_Inputs_From_File
        self._test_runner.config_file_data.conversion_rules = [
            self.BERRY_CONVERSION_RULE,
            self.NAMASTE_CONVERSION_RULE,
        ]
        self._test_runner.declare_inputs_from_file(
            self._data_directory / "input_from_files_and_inputs_duplicate_contents.txt",
            self._data_directory)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            "lobster-trlc: TRLC processing failed: aborting due to TRLC error\n"
        )
        asserter.assertStdOutText('package test_default\n'
                                  '        ^^^^^^^^^^^^ default_file_copy.rsl:1: '
                                  'error: duplicate definition, previous definition at'
                                  ' default_file.rsl:1\n'
                                  'namaste goodname {\n'
                                  '        ^^^^^^^^ default_file_copy.trlc:3: '
                                  'error: duplicate definition, previous definition at'
                                  ' default_file.trlc:3\n'
                                  )
        asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
