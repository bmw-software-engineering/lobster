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
