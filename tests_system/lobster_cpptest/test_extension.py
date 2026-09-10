# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

from pathlib import Path
import unittest
from tests_system.lobster_cpptest.\
    lobster_cpptest_system_test_case_base import LobsterCpptestSystemTestCaseBase
from tests_system.lobster_cpptest.\
    lobster_cpptest_asserter import LobsterCppTestAsserter as Asserter
from tests_system.tests_utils.\
    update_cpptest_expected_output import update_cpptest_output_file


class ExtensionCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self.output_dir = Path(Path(__file__).parents[0])

    def test_valid_extension_file(self):
        """
        Test checks that the C++ files with valid extensions are processed correctly.
        """
        # lobster-trace: cpptest_req.All_Recognized_Tests_Extracted
        # lobster-trace: cpptest_req.Requirement_References_Extracted_As_Tags
        self._test_runner.cmd_args.config = str(
            self._data_directory / "valid_extension_config.yaml")
        self._test_runner.declare_input_file(
            self._data_directory / "valid_extension.cpp"
        )
        OUT_FILE = "valid_extension.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / OUT_FILE))
        self._test_runner.declare_output_file(self.output_dir /
                                              OUT_FILE)

        update_cpptest_output_file(
            self.output_dir / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(41, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_invalid_extension_file(self):
        """
        Test processing of C++ files with invalid extensions but valid data.
        Hence, the tool should still be able to process the files correctly.
        """
        # lobster-trace: cpptest_req.Explicit_File_Ignores_Extension
        self._test_runner.cmd_args.config = str(
            self._data_directory / "invalid_extension_config.yaml")
        self._test_runner.declare_input_file(
            self._data_directory / "invalid_extension.xyz"
        )
        OUT_FILE = "invalid_extension.lobster"

        self.output_dir = self.create_output_directory_and_copy_expected(
            self.output_dir, Path(self._data_directory / OUT_FILE))
        self._test_runner.declare_output_file(self.output_dir /
                                              OUT_FILE)

        update_cpptest_output_file(
            self.output_dir / OUT_FILE,
            self._test_runner.working_dir
        )

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(40, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_no_input_file(self):
        """
        Test processing of C++ files with no input files.
        Input file provided in YAML config file does not exist.
        """
        # lobster-trace: cpptest_req.Input_Not_File_Not_Directory
        self._test_runner.cmd_args.config = str(
            self._data_directory / "no_input_file_config.yaml")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            'lobster-cpptest: "no_input_file.cpp" is not a file or directory.\n'
        )
        asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
