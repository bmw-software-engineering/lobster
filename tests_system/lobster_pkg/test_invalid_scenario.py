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
from tests_system.lobster_pkg.lobster_pkg_asserter import LobsterPkgAsserter
from tests_system.lobster_pkg.lobster_pkg_system_test_case_base import (
    LobsterPKGSystemTestCaseBase,
)


class InvalidInputFilePkgTest(LobsterPKGSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_not_existing_pkg_file(self):
        """Test that a missing input file causes non-zero exit code"""
        # lobster-trace: pkg_req.Input_Not_File_Not_Directory

        # GIVEN the user specifies a non-existing input file
        non_existing_file = str(
            self._data_directory / "not_existing.pkg")

        # WHEN the tool is run with the non-existing input file
        self._test_runner.cmd_args.files = [non_existing_file]
        self._test_runner.cmd_args.out = "will-not-be-generated.lobster"
        completed_process = self._test_runner.run_tool_test()

        # THEN the tool SHALL print an error message and exit with a non-zero return
        # code
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertInStdErr(f'{non_existing_file} is not a file or directory')
        asserter.assertExitCode(1)

    def test_missing_input_parameter(self):
        """Test that not specifying an input file causes non-zero exit code"""
        # lobster-trace: pkg_req.Pkg_No_Input_Files

        # GIVEN the user specifies no input files
        self._test_runner.cmd_args.files = []
        self._test_runner.cmd_args.out = "will-not-be-generated.lobster"

        # WHEN the tool is run
        completed_process = self._test_runner.run_tool_test()

        # THEN the tool SHALL print an error message and exit with a non-zero return
        # code
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertInStdErr('lobster-pkg: No input files found to process!\n')
        asserter.assertExitCode(1)

    def test_not_existing_output_path(self):
        """Test that a missing output path is created automatically"""
        # lobster-trace: pkg_req.Pkg_Output_Directory_Created
        INPUT_FILE = "valid_file1.pkg"
        OUT_FILE = self._data_directory / "to-be-created" / "on-the-fly" / "out.lobster"
        self._test_runner.declare_input_file(self._data_directory / INPUT_FILE)

        # GIVEN the user specifies an input file
        # AND an output path that does not yet exist
        self._test_runner.cmd_args.files = [
            str(self._data_directory / INPUT_FILE)
        ]
        self._test_runner.cmd_args.out = str(OUT_FILE)

        # WHEN the tool is run
        completed_process = self._test_runner.run_tool_test()
        self._test_runner.declare_output_file(OUT_FILE)

        # THEN the tool SHALL create the missing output path
        # AND write the output file
        # AND exit with a zero return code
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(1, str(OUT_FILE))
        asserter.assertExitCode(0)

    def test_misplaced_tags_in_analysis_node(self):
        """Test that a misplaced lobster-trace in an ANALYSISITEM node causes a warning
           but exit code 0"""
        # lobster-trace: pkg_req.Misplaced_Description_Node_Trace_Warning
        INPUT_FILE = "misplaced_tag_in_analysis_node.pkg"
        OUT_FILE = "report.lobster"
        misplaced_lobster_trace_file = str(
            self._data_directory / INPUT_FILE)

        # GIVEN the user specifies an input file containing a lobster-trace in an
        # ANALYSISITEM node (so the lobster-trace is misplaced)
        self._test_runner.cmd_args.files = [misplaced_lobster_trace_file]
        self._test_runner.cmd_args.out = OUT_FILE

        # WHEN the tool is run
        completed_process = self._test_runner.run_tool_test()

        # THEN the tool SHALL print a warning message to STDOUT identifying the file and
        # the misplaced tag
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        expected_output = (
            f'WARNING: misplaced lobster-trace in {INPUT_FILE}: '
            'lobster-trace: misplaced.req1,misplaced.req2\n'
            f'lobster-pkg: wrote 1 items to {OUT_FILE}\n'
        )
        asserter.assertStdOutText(expected_output)
        # AND SHALL continue processing the remaining input (despite the warning)
        asserter.assertExitCode(0)

    def test_misplaced_tags_in_value_node(self):
        """Test that a misplaced lobster-trace in TESTSTEPS causes non-zero exit code"""
        # lobster-trace: pkg_req.Misplaced_Value_Node_Trace_Error
        OUT_FILE = "report.lobster"
        MISPLACED_TAGS_FILENAME = "misplaced_tag_in_value_node.pkg"
        misplaced_tags_file_path = str(
            self._data_directory / MISPLACED_TAGS_FILENAME)

        # GIVEN the user specifies an input file containing a misplaced lobster-trace in
        # a VALUE node
        self._test_runner.cmd_args.files = [misplaced_tags_file_path]
        self._test_runner.cmd_args.out = OUT_FILE

        # WHEN the tool is run
        completed_process = self._test_runner.run_tool_test()

        # THEN the tool SHALL print an error message to STDOUT identifying the file and
        # the misplaced tag
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        expected_output = (
            f'LOBSTER Error: Misplaced LOBSTER tag(s) in file '
            f'{MISPLACED_TAGS_FILENAME} at line(s): [63]\n'
        )
        asserter.assertStdOutText(expected_output)
        asserter.assertExitCode(1)

    def test_invalid_xml_file(self):
        # lobster-trace: pkg_req.Pkg_Invalid_Xml
        OUT_FILE = "report.lobster"
        INVALID_XML_FILE = "invalid_xml.pkg"
        invalid_xml_file_path = str(
            self._data_directory / INVALID_XML_FILE)

        # GIVEN the user specifies an input file that contains invalid XML
        self._test_runner.cmd_args.files = [invalid_xml_file_path]
        self._test_runner.cmd_args.out = OUT_FILE

        # WHEN the tool is run
        completed_process = self._test_runner.run_tool_test()

        # THEN the tool SHALL print an error message to STDOUT indicating the XML
        # parsing error
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        expected_output = (
            f"Error parsing XML file '{INVALID_XML_FILE}' : "
            f"mismatched tag: line 13, column 2\n"
        )
        asserter.assertStdOutText(expected_output)
        asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
