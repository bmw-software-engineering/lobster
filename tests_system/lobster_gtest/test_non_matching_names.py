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


class NonMatchingNamesTest(LobsterGtestSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.declare_input_file(
            self._data_directory / "non_matching_names.xml"
        )
        self._test_runner.cmd_args.files = ["non_matching_names.xml"]
        self._out_file = "non_matching_names.lobster"
        self._test_runner.cmd_args.out = self._out_file
        self._test_runner.declare_output_file(
            self._data_directory / self._out_file
        )

    def _assert_unchanged_items(self):
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(7, self._out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_items_are_the_same_as_without_option(self):
        """Test that non-matching names leave the items unchanged."""
        # lobster-trace: gtest_req.No_Derivation_From_Non_Matching_Name
        # GIVEN test names which do not match the naming convention
        # AND the option to derive the specification from the name
        self._test_runner.cmd_args.derive_gwt_from_test_name = True

        # WHEN the tool is run
        # THEN the items are written as if the option was not given
        self._assert_unchanged_items()

    def test_expected_output_equals_output_without_option(self):
        """Test that the expected output is the output without the option."""
        # lobster-trace: gtest_req.No_Derivation_From_Non_Matching_Name
        # GIVEN test names which do not match the naming convention
        # AND no option to derive the specification from the name

        # WHEN the tool is run
        # THEN the items are identical to the expected output
        self._assert_unchanged_items()


if __name__ == "__main__":
    unittest.main()
