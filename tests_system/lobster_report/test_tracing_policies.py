import unittest
from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase,
)


class ReportTracingPoliciesTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_linear_policy(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Linear_Policy_Support
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
        asserter.assertStdOutText(f"{conf_file}: lobster warning: configuration file format '.conf' "
                                  "is deprecated, please migrate to '.yaml' format\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_linear_policy_yaml(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: core_report_req.Linear_Policy_Support
        """
        This test checks that the lobster report tool can handle a linear policy
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "linear_policy.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "linear_system_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "linear_software_requirements.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "code_linear.lobster")

        conf_file = "linear_policy.yaml"
        out_file = "report_linear_yaml.lobster"
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
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: UseCases.Requirement_to_software_Test_Mapping_in_Output
        # lobster-trace: UseCases.Software_Test_to_Requirement_Mapping_in_output
        # lobster-trace: core_report_req.Complex_Multi_Level_Policy_Support
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
        asserter.assertStdOutText(f"{conf_file}: lobster warning: configuration file format '.conf' "
                                  "is deprecated, please migrate to '.yaml' format\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_pizza_policy_yaml(self):
        # lobster-trace: UseCases.Tracing_Policy_Output_File
        # lobster-trace: UseCases.Requirement_to_software_Test_Mapping_in_Output
        # lobster-trace: UseCases.Software_Test_to_Requirement_Mapping_in_output
        # lobster-trace: core_report_req.Complex_Multi_Level_Policy_Support
        """
        This test checks that the lobster report tool can handle a pizza policy
        which consists of 5 levels: system requirements, software requirements,
        code, unit tests, and component tests.
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "pizza_policy.yaml")
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

        conf_file = "pizza_policy.yaml"
        out_file = "report_pizza_yaml.lobster"
        self._test_runner.cmd_args.lobster_config = conf_file
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertNoStdOutText()
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_codebeamer_links(self):
        # lobster-trace: UseCases.Correct_Item_Data_in_Output_File
        """
        This test checks that the report contains
        the Codebeamer items present in the input file.
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "codebeamer_links_policy.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "codebeamer_items.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "codebeamer_funny_impl.lobster")

        conf_file = "codebeamer_links_policy.conf"
        out_file = "report_codebeamer_links.lobster"
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

    def test_codebeamer_links_yaml(self):
        # lobster-trace: UseCases.Correct_Item_Data_in_Output_File
        """
        This test checks that the report contains
        the Codebeamer items present in the input file.
        """
        self._test_runner.declare_input_file(self._data_directory /
                                             "codebeamer_links_policy.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "codebeamer_items.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "codebeamer_funny_impl.lobster")

        conf_file = "codebeamer_links_policy.yaml"
        out_file = "report_codebeamer_links_yaml.lobster"
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
