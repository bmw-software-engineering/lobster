from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)
from tests_system.asserter import Asserter


class InvalidConfigTest(LobsterTrlcSystemTestCaseBase):
    """These tests verify the behavior when the YAML configuration file is invalid."""

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_nonconformant_yaml(self):
        """Test that non-conformant YAML file results in error."""
        # lobster-trace: UseCases.TRLC_Config_File_Syntax_Error
        # lobster-trace: UseCases.TRLC_Config_File_Key_Error
        self._test_runner.cmd_args.out = "will-not-be-generated.lobster"
        self.assertFalse(
            self._test_runner.config_file_data.conversion_rules,
            "Invalid test setup: Conversion rules should be empty for this test case. "
            "The goal is to prepare a scenario where the YAML config file does not "
            "conform to the schema.",
        )
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertInStdErr("conversion-rules: Required field missing")
        asserter.assertNoStdOutText()
        asserter.assertExitCode(1)


class MissingConfigTest(LobsterTrlcSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner_without_config_file_data()

    def test_missing_config_parameter(self):
        # lobster-trace: UseCases.TRLC_Config_File_Missing
        out_file = "missing_config_file.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)

        # assertInStdErr is being used instead of assertStdErrText because the output is
        # truncated when Python version is 3.9 and above.
        # But for Python version 3.8 the full output is shown.

        # Incase of Python >-3.9 the error message is:
        # 'usage: lobster-trlc [-h] [-v] [--out OUT] --config CONFIG [DIR|FILE ...]\n'
        # 'lobster-trlc: error: the following arguments are required: --config\n'

        # For Python 3.8 the full error message is:
        # 'usage: lobster-trlc [-h] [-v] [--out OUT] --config CONFIG
        # [DIR|FILE [DIR|FILE ...]]\n'
        # 'lobster-trlc: error: the following arguments are required: --config\n'
        asserter.assertInStdErr("usage: lobster-trlc [-h] [-v] [--out OUT] "
                                "--config CONFIG")
        asserter.assertInStdErr("lobster-trlc: error: the following arguments "
                                "are required: --config")
        asserter.assertExitCode(2)

    def test_missing_config_file(self):
        # lobster-trace: UseCases.TRLC_Config_File_Missing
        out_file = "missing_config_file.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.cmd_args.config = str(
            self._test_runner.working_dir / "non_existant.yaml")
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertInStdErr("lobster-trlc: File or directory not found: "
                                "[Errno 2] No such file or directory:",
                                completed_process.stderr)
        asserter.assertExitCode(1)
