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


class LastMatchingNameSegmentTest(LobsterGtestSystemTestCaseBase):
    def test_last_matching_segment_is_used(self):
        """Test that the last matching segment of a test name is used."""
        # lobster-trace: gtest_req.Spec_Derived_From_Last_Matching_Name_Segment
        # GIVEN test names with several "/" separated segments,
        # of which more than one matches the naming convention
        test_runner = self.create_test_runner()
        test_runner.declare_input_file(
            self._data_directory / "name_segments.xml"
        )
        test_runner.cmd_args.files = ["name_segments.xml"]
        out_file = "name_segments.lobster"
        test_runner.cmd_args.out = out_file
        test_runner.cmd_args.derive_gwt_from_test_name = True
        test_runner.declare_output_file(self._data_directory / out_file)

        # WHEN the tool is run with the option to derive from the test name
        completed_process = test_runner.run_tool_test()

        # THEN the specification is taken from the last matching segment
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(2, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
