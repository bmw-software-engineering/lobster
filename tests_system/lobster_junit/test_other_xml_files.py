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
from tests_system.lobster_junit.lobster_junit_system_test_case_base import (
    LobsterJunitSystemTestCaseBase,
)
from tests_system.lobster_junit.lobster_junit_asserter import (
    LobsterJunitAsserter as Asserter,
)


class OtherXmlFilesTest(LobsterJunitSystemTestCaseBase):
    def test_other_xml_file_is_ignored(self):
        """Test that an XML file which is not a test report is ignored."""
        # lobster-trace: junit_req.Other_Xml_Files_Ignored
        # GIVEN an XML file whose root element is neither testsuites nor testsuite
        test_runner = self.create_test_runner()
        test_runner.declare_input_file(self._data_directory / "other.xml")
        test_runner.cmd_args.files = ["other.xml"]
        test_runner.cmd_args.out = "other.lobster"
        test_runner.declare_output_file(self._data_directory / "other.lobster")

        # WHEN the tool is run
        completed_process = test_runner.run_tool_test()

        # THEN no item is written, nothing is printed to stderr, and the tool
        # succeeds
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(0, "other.lobster")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
