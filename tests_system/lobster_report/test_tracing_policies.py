# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025-2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

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
        # lobster-trace: core_report_req.Tracing_Policy_Written_To_Output_File
        # lobster-trace: core_report_req.Report_Generation_For_Valid_Config_And_Inputs
        # lobster-trace: core_report_req.Item_Status_Ok_When_Required_References_Present
        # lobster-trace: core_report_req.Level_Coverage_Percentage_From_Item_Status
        # lobster-trace: core_report_req.Legacy_Tracing_Policy_Deprecation_Warning
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
        asserter.assertStdOutText(self.legacy_policy_deprecation_warning(conf_file))
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_pizza_policy(self):
        # lobster-trace: core_report_req.Tracing_Policy_Written_To_Output_File
        # lobster-trace: core_report_req.Report_Generation_For_Valid_Config_And_Inputs
        # lobster-trace: core_report_req.Item_Status_Ok_When_Required_References_Present
        # lobster-trace: core_report_req.Level_Coverage_Percentage_From_Item_Status
        # lobster-trace: core_report_req.Coverage_Computed_From_Yaml_Tracing_Policy
        # lobster-trace: core_report_req.Legacy_Tracing_Policy_Deprecation_Warning
        """
        This test checks that the lobster report tool can handle a pizza policy
        which consists of 5 levels: system requirements, software requirements,
        code, unit tests, and component tests. It runs once with the policy
        declared in the legacy format and once in the YAML format, both
        producing identical output.
        """
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

        out_file = "report_pizza.lobster"
        self._test_runner.declare_output_file(self._data_directory / out_file)

        for conf_file, expected_stdout in (
            ("pizza_policy.conf",
             self.legacy_policy_deprecation_warning("pizza_policy.conf")),
            ("pizza_policy.yaml", ""),
        ):
            with self.subTest(conf_file=conf_file):
                self._test_runner.declare_input_file(self._data_directory /
                                                     conf_file)
                self._test_runner.cmd_args.lobster_config = conf_file
                self._test_runner.cmd_args.out = out_file

                completed_process = self._test_runner.run_tool_test()
                asserter = Asserter(self, completed_process, self._test_runner)
                asserter.assertNoStdErrText()
                asserter.assertStdOutText(expected_stdout)
                asserter.assertExitCode(0)
                asserter.assertOutputFiles()

    def test_codebeamer_links(self):
        # lobster-trace: core_report_req.Codebeamer_Reference_Propagated_To_Output
        # lobster-trace: core_report_req.Report_Generation_For_Valid_Config_And_Inputs
        # lobster-trace: core_report_req.Item_Status_Ok_When_Required_References_Present
        # lobster-trace: core_report_req.Level_Coverage_Percentage_From_Item_Status
        # lobster-trace: core_report_req.Legacy_Tracing_Policy_Deprecation_Warning
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
        asserter.assertStdOutText(self.legacy_policy_deprecation_warning(conf_file))
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
