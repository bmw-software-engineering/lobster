import unittest
from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)
from tests_system.asserter import Asserter


class ZeroInputTest(LobsterTrlcSystemTestCaseBase):
    """These tests verify the behavior when there are no TRLC record objects in the
       input."""

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_rsl_input_only(self):
        """Test that output is empty if no *.trlc inputs are provided, only *.rsl."""
        # lobster-trace: UseCases.Default_Path_Warning_Test
        self._test_runner.config_file_data.conversion_rules = [
            self.BERRY_CONVERSION_RULE,
        ]
        OUT_FILE = "zero_items.lobster"
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)
        self._test_runner.declare_input_file(self._data_directory /
                                             "fruits.rsl")
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"lobster-trlc: wrote 0 items to "
                                  f"{OUT_FILE}\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_no_inputs_at_all(self):
        """Test that output is not generated if no inputs are provided at all.

           Note: This only works if additionally no conversion rules are defined.
                 If conversion rules are defined, then the tool will try to map
                 those to TRLC record types, and will fail if no such types
                 are found (because the input is empty).
        """
        # lobster-trace: trlc_req.No_Inputs_At_All
        # lobster-trace: UseCases.Default_Path_Warning_Test
        # lobster-trace: UseCases.Incorrect_data_Extraction_from_TRLC
        self._test_runner.config_file_data.conversion_rules = []
        OUT_FILE = "zero_items.lobster"
        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"lobster-trlc: wrote 0 items to "
                                  f"{OUT_FILE}\n")
        asserter.assertExitCode(0)

    def test_orphan_conversion_rules(self):
        """
        Test that when conversion rules are not provided
        then the tool shall raise an error
        """
        # lobster-trace: trlc_req.No_Inputs_At_All
        # lobster-trace: UseCases.TRLC_Config_File_Key_Error
        self._test_runner.config_file_data.conversion_rules = [
            self.BERRY_CONVERSION_RULE,
            self.NAMASTE_CONVERSION_RULE,
        ]
        OUT_FILE = "will-not-be-generated.lobster"
        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            "lobster-trlc: Invalid conversion rule defined in config.yaml: The "
            "following conversion rules do not match any record type in the TRLC "
            "symbol table: sweet_fruits.berry, test_default.namaste. "
            "The TRLC symbol table contains no record types at all. "
            "The following conversion rules were successfully mapped to TRLC types: "
            "none.\n"
        )
        asserter.assertNoStdOutText()
        asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
