from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase,
)


class ReportMultipleInputTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_extra_input_files_are_ignored_by_policy(self):
        # lobster-trace: core_report_req.Input_Files_Policy_Based_Processing
        """
        This test checks that the lobster report tool can handle multiple input files.
        The tool should actually fetch input files provided in the tracing policy
        and avoid all extra lobster files
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_just.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_code.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_test.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "report_ok.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_missing.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_requirements.lobster")

        conf_file = "multiple_traces_just.conf"
        out_file = "report_multiple_traces_just.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_missing_required_files_cause_failure(self):
        # lobster-trace: core_report_req.Missing_Required_Files_Error
        """
        This test checks that the lobster report tool fails when required input files
        are missing. The tool should report an error and abort processing if any
        required lobster file is not found.
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_just.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "just_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "multiple_traces_code.lobster")

        conf_file = "multiple_traces_just.conf"
        out_file = "report_multiple_traces_just.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText("")
        asserter.assertStdOutText(
            "multiple_traces_just.conf:11: lobster error: cannot find file "
            "multiple_traces_test.lobster\n"
            "\n"
            "lobster-lobster-report: aborting due to earlier errors.\n"
        )
        asserter.assertExitCode(1)

    def test_multiple_source_files(self):
        # lobster-trace: core_report_req.Multi_Level_Source_Files
        # lobster-trace: core_report_req.Item_Data_Isolation
        """
        This test checks that the lobster report tool can handle multiple source files
        given at different levels of tracing policy.
        The tool should isolate item data of items and do not mix it.
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "octopus_policy.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "octopus_system.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "octopus_software.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "tentacle_commander_code.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "tentacle_toolkit_code.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "tentacle_commander_test.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "tentacle_toolkit_test.lobster")

        conf_file = "octopus_policy.conf"
        out_file = "report_octopus.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
