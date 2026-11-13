import unittest
from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase)


class ReportConfigAndDuplicateErrorsTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_duplicate_item_definition(self):
        # lobster-trace: core_report_req.Report_Input_Duplicate_Definition
        # lobster-trace: core_report_req.Legacy_Tracing_Policy_Deprecation_Warning
        """
        This test checks that the lobster report tool aborts with a non-zero exit
        code when the same tag is defined in more than one source file.
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "duplicate_definition.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "dup_req_a.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "dup_req_b.lobster")

        self._test_runner.cmd_args.lobster_config = "duplicate_definition.conf"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"{self.legacy_policy_deprecation_warning('duplicate_definition.conf')}"
            "dup_req_b.trlc:7:13: lobster error: duplicate definition of "
            "req example.duplicate, previously defined at dup_req_a.trlc:3:13\n\n"
            "lobster-report: aborting due to earlier errors.\n"
        )
        asserter.assertExitCode(1)

    def test_invalid_trace_to_target(self):
        # lobster-trace: core_report_req.Invalid_Trace_To
        # lobster-trace: core_report_req.Legacy_Tracing_Policy_Deprecation_Warning
        """
        This test checks that the lobster report tool aborts with a non-zero exit
        code when the configuration file's "trace to" entry references a level
        that is not defined in the configuration.
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "invalid_trace_to.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_ok.lobster")

        self._test_runner.cmd_args.lobster_config = "invalid_trace_to.conf"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"{self.legacy_policy_deprecation_warning('invalid_trace_to.conf')}"
            "invalid_trace_to.conf:3: lobster error: unknown item Nonexistent\n\n"
            "lobster-report: aborting due to earlier errors.\n"
        )
        asserter.assertExitCode(1)

    def test_invalid_yaml_policy(self):
        # lobster-trace: core_report_req.Invalid_Yaml_Tracing_Policy
        """
        This test checks that the lobster report tool reports the line of the problem
        and exits with code 1 when the YAML tracing policy violates the schema.
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "invalid_policy.yaml")

        out_file = "report_invalid_policy.lobster"
        self._test_runner.cmd_args.lobster_config = "invalid_policy.yaml"
        self._test_runner.cmd_args.out = out_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            "LOBSTER Error: invalid_policy.yaml:5: invalid tracing policy: "
            "levels.1.kind: 'bogus' not in "
            "('requirements', 'implementation', 'activity')\n"
        )
        asserter.assertExitCode(1)
        self.assertFalse((self._test_runner.working_dir / out_file).exists())


if __name__ == "__main__":
    unittest.main()
