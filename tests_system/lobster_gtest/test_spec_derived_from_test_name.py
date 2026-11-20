# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
from tests_system.lobster_gtest.lobster_gtest_system_test_case_base import (
    LobsterGtestSystemTestCaseBase,
)
from tests_system.lobster_gtest.lobster_gtest_asserter import (
    LobsterGtestAsserter as Asserter,
)


class SpecDerivedFromTestNameTest(LobsterGtestSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.declare_input_file(
            self._data_directory / "conventional_names.xml"
        )
        self._test_runner.cmd_args.files = ["conventional_names.xml"]

    def _run(self, out_file: str):
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(6, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_conventional_names_add_given_when_then(self):
        """Test that Given, When and Then lines are derived from the name."""
        # lobster-trace: gtest_req.Spec_Derived_From_Test_Name
        # GIVEN test names which follow the naming convention
        # AND the option to derive the specification from the name
        self._test_runner.cmd_args.derive_gwt_from_test_name = True

        # WHEN the tool is run
        # THEN the item texts contain the derived Given, When and Then lines
        self._run("conventional_names.lobster")

    def test_without_option_text_has_only_recorded_properties(self):
        """Test that without the option only recorded properties are used."""
        # lobster-trace: gtest_req.No_Derivation_Without_Option
        # GIVEN test names which follow the naming convention
        # AND no option to derive the specification from the name

        # WHEN the tool is run
        # THEN the item texts contain only the recorded properties
        self._run("conventional_names_without_option.lobster")


if __name__ == "__main__":
    unittest.main()
