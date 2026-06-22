import unittest
from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase
)


class ReportJustificationTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_justification_and_coverage(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: UseCases.Coverage_calculation_in_Output
        # lobster-trace: core_report_req.Status_Justified_Global
        # lobster-trace: core_report_req.Status_Justified_Up
        # lobster-trace: core_report_req.Status_Justified_Down
        """
        This test checks that the lobster report tool can handle justifications
        and coverage changes according to justifications and generate lobster report.
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_policy.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_usecases.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_system_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_software_requirements.lobster")

        conf_file = "just_policy.conf"
        out_file = "just_report.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"{conf_file}: lobster warning: configuration file format '.conf' "
            f"is deprecated, please migrate to '.yaml' format\n"
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_justification_and_coverage_yaml_no_schema(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: UseCases.Coverage_calculation_in_Output
        # lobster-trace: core_report_req.Status_Justified_Global
        # lobster-trace: core_report_req.Status_Justified_Up
        # lobster-trace: core_report_req.Status_Justified_Down
        """
        This test checks that the lobster report tool can handle justifications
        and coverage changes according to justifications and generate lobster report.
        """
        self._test_runner.declare_input_file(
            self._data_directory / "just_policy_no_schema.yaml"
        )
        self._test_runner.declare_input_file(
            self._data_directory / "just_usecases_no_schema.lobster"
        )
        self._test_runner.declare_input_file(
            self._data_directory / "just_system_requirements_no_schema.lobster"
        )
        self._test_runner.declare_input_file(
            self._data_directory / "just_software_requirements_no_schema.lobster"
        )

        conf_file = "just_policy_no_schema.yaml"
        out_file = "just_report_yaml_no_schema.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
