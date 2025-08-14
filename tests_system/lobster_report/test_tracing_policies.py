from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase,
)


class ReportTracingPoliciesTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_linear_policy(self):
        """
        This test checks that the lobster report tool can handle a linear policy
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "linear_policy.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "linear_system_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "linear_software_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "code_linear.lobster")

        conf_file = "linear_policy.conf"
        out_file = "report_linear.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_pizza_policy(self):
        """
        This test checks that the lobster report tool can handle a pizza policy
        which consists of 5 levels: system requirements, software requirements,
        code, unit tests, and component tests.
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "pizza_policy.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "pizza_system_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "pizza_software_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "pizza_code.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "pizza_component_tests.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "pizza_unit_tests.lobster")

        conf_file = "pizza_policy.conf"
        out_file = "report_pizza.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
