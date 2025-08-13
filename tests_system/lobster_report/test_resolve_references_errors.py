from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase)


class ReportResolveReferencesErrorsTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_unknown_tracing_target(self):
        # lobster-trace: core_report_req.Unknown_Tracing_Target
        self._test_runner.declare_input_file(self._data_directory /
                                             "unknown_tracing_target.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_unknown_tracing_target.lobster")

        self._test_runner.cmd_args.lobster_config = "unknown_tracing_target.conf"
        self._test_runner.cmd_args.out = "report_unknown_tracing_target.lobster"
        self._test_runner.declare_output_file(self._data_directory /
                                              "report_unknown_tracing_target.lobster")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_tracing_destination_unversioned(self):
        # lobster-trace: core_report_req.Tracing_Destination_Unversioned
        self._test_runner.declare_input_file(self._data_directory /
                                             "unversioned_trace.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_unversioned_trace_dest.lobster")

        self._test_runner.cmd_args.lobster_config = "unversioned_trace.conf"
        self._test_runner.cmd_args.out = "report_unversioned_trace_dest.lobster"
        self._test_runner.declare_output_file(self._data_directory /
                                              "report_unversioned_trace_dest.lobster")

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_tracing_destination_version_mismatch(self):
        # lobster-trace: core_report_req.Tracing_Destination_Version_Mismatch
        self._test_runner.declare_input_file(self._data_directory /
                                             "version_mismatch_trace.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_ver_mismatch_trace_dest.lobster")

        self._test_runner.cmd_args.lobster_config = "version_mismatch_trace.conf"
        self._test_runner.cmd_args.out = "report_ver_mismatch_trace_dest.lobster"
        self._test_runner.declare_output_file(self._data_directory /
                                              "report_ver_mismatch_trace_dest.lobster")

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
