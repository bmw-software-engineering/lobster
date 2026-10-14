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

import json
import unittest
from tests_system.lobster_gtest.lobster_gtest_system_test_case_base import (
    LobsterGtestSystemTestCaseBase,
)
from tests_system.lobster_gtest.lobster_gtest_asserter import (
    LobsterGtestAsserter as Asserter,
)


def warning(location: str, test: str) -> str:
    return (
        f"{location}: lobster warning: test {test} records "
        "Given/When/Then properties, ignoring its name\n"
    )


class RecordPropertiesTest(LobsterGtestSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.cmd_args.derive_gwt_from_test_name = True

    def _declare(self, name: str):
        self._test_runner.declare_input_file(
            self._data_directory / f"{name}.xml"
        )
        self._test_runner.cmd_args.files = [f"{name}.xml"]

    def test_record_properties_take_precedence_and_blank_ones_are_replaced(
        self,
    ):
        """Test precedence of recorded properties over the test name."""
        # lobster-trace: gtest_req.Record_Properties_Take_Precedence_Over_Test_Name
        # lobster-trace: gtest_req.Blank_Record_Properties_Replaced_By_Test_Name
        # lobster-trace: gtest_req.Warning_If_Record_Properties_And_Test_Name_Given
        # GIVEN tests with conventional names, some of which record
        # non-blank Given, When or Then properties and some blank ones
        # AND the option to derive the specification from the name
        self._declare("record_properties")
        out_file = "record_properties.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        # WHEN the tool is run
        completed_process = self._test_runner.run_tool_test()

        # THEN tests with non-blank properties keep them and cause a warning,
        # AND tests with only blank properties get the derived lines
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            "".join(
                [
                    warning("cache.cpp:10", "Cache:GivenA_WhenB_ExpectC"),
                    warning("cache.cpp:20", "Cache:GivenD_ExpectE"),
                    warning("cache.cpp:40", "Cache:GivenH_ExpectI"),
                ]
            )
        )
        asserter.assertStdOutNumAndFile(6, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_warning_names_the_location_of_the_test_case(self):
        """Test the location shown in the warning."""
        # lobster-trace: gtest_req.Warning_If_Record_Properties_And_Test_Name_Given
        # GIVEN conflicting tests with file and line, with file only,
        # and without location
        # AND the option to derive the specification from the name
        self._declare("warning_locations")
        out_file = "warning_locations.lobster"
        self._test_runner.cmd_args.out = out_file

        # WHEN the tool is run
        completed_process = self._test_runner.run_tool_test()

        # THEN each warning names the most precise location which is known
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            "".join(
                [
                    warning("cache.cpp:10", "Cache:GivenA_ExpectB"),
                    warning("cache.cpp", "Cache:GivenC_ExpectD"),
                    warning("<unknown location>", "Cache:GivenE_ExpectF"),
                ]
            )
        )
        asserter.assertStdOutNumAndFile(3, out_file)
        asserter.assertExitCode(0)

    def test_warning_is_not_printed_to_stdout(self):
        """Test that the warning goes to stderr only."""
        # lobster-trace: gtest_req.Warning_If_Record_Properties_And_Test_Name_Given
        # GIVEN a conflicting test
        # AND the option to derive the specification from the name
        # AND no output file, so that the items are written to stdout
        self._declare("record_properties")

        # WHEN the tool is run
        completed_process = self._test_runner.run_tool_test()

        # THEN stdout contains only the items, and stderr the warning
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(0)
        asserter.assertInStdErr("lobster warning")
        with open(
            self._data_directory / "record_properties.lobster",
            encoding="UTF-8",
        ) as expected_file:
            expected = json.load(expected_file)
        self.assertEqual(expected, json.loads(completed_process.stdout))


if __name__ == "__main__":
    unittest.main()
