import unittest
from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase,
)


class ReportTracingStatusTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    # Tests for the report generation with different statuses
    # Status Ok with "lobster_ok.conf"
    def test_status_ok(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Status_Ok
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_ok.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_ok.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_ok.lobster")

        conf_file = "lobster_ok.conf"
        out_file = "report_ok.lobster"
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

    # Status Ok with "lobster_ok_no_schema.yaml" (no kind)
    def test_status_ok_yaml_no_schema(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Status_Ok
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_ok_no_schema.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_ok_no_schema.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_ok_no_schema.lobster")

        conf_file = "lobster_ok_no_schema.yaml"
        out_file = "report_ok_yaml_no_schema.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    # Status Missing with "lobster_missing.conf"
    def test_status_missing(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Status_Missing
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_missing.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_missing.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_missing.lobster")

        conf_file = "lobster_missing.conf"
        out_file = "report_missing.lobster"
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

    # Status Missing with "lobster_missing_no_schema.yaml"
    def test_status_missing_yaml_no_schema(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Status_Missing
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_missing_no_schema.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_missing_no_schema.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_missing_no_schema.lobster")

        conf_file = "lobster_missing_no_schema.yaml"
        out_file = "report_missing_yaml_no_schema.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_status_mixed(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Status_Missing
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_mixed.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_mixed.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_mixed.lobster")

        conf_file = "lobster_mixed.conf"
        out_file = "report_mixed.lobster"
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

    def test_status_mixed_yaml_no_schema(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Status_Missing
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_mixed_no_schema.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_mixed_no_schema.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_mixed_no_schema.lobster")

        conf_file = "lobster_mixed_no_schema.yaml"
        out_file = "report_mixed_yaml_no_schema.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    # Status Justified with "lobster_justified.conf"
    def test_status_justified(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Status_Justified_Global
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_justified.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_justified.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_justified.lobster")

        conf_file = "lobster_justified.conf"
        out_file = "report_justified.lobster"
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

    # Status Justified with "lobster_justified_no_schema.yaml"
    def test_status_justified_yaml_no_schema(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Status_Justified_Global
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_justified_no_schema.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_justified_no_schema.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_justified_no_schema.lobster")

        conf_file = "lobster_justified_no_schema.yaml"
        out_file = "report_justified_yaml_no_schema.lobster"
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
