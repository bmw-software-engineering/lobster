import unittest
from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase,
)


class ReportMultipleTracesTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_multiple_traces_justification(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: UseCases.Software_Test_to_Requirement_Mapping_in_output
        # lobster-trace: core_report_req.Multiple_Traces_Support
        # lobster-trace: core_report_req.Status_Justified_Up
        """
        This test checks that the lobster report tool can handle multiple lobster traces
         with justifications in code as well as tests
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_just.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_code.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_test.lobster")

        conf_file = "multiple_traces_just.conf"
        out_file = "report_multiple_traces_just.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"{conf_file}: lobster warning: configuration file format '.conf' "
                                  "is deprecated, please migrate to '.yaml' format\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_multiple_traces_justification_yaml(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: UseCases.Software_Test_to_Requirement_Mapping_in_output
        # lobster-trace: core_report_req.Multiple_Traces_Support
        # lobster-trace: core_report_req.Status_Justified_Up
        """
        This test checks that the lobster report tool can handle multiple lobster traces
         with justifications in code as well as tests
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_just.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_code.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_test.lobster")

        conf_file = "multiple_traces_just.yaml"
        out_file = "report_multiple_traces_just_yaml.lobster"
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
