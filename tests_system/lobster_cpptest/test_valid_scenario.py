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
from tests_system.asserter import Asserter
from tests_system.tests_utils.\
    update_cpptest_expected_output import update_cpptest_output_file


class InputFileCpptestTest(LobsterCpptestSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self.output_dir = Path(Path(__file__).parents[0])

    def test_valid_input_cpptest_file(self):
        """
        This test checks that the valid C++ test file is processed correctly
        by the lobster-cpptest tool.
        """
        # lobster-trace: cpptest_req.Output_File_Config_Option
        OUT_FILE = "report.lobster"
        self._test_runner.declare_input_file(self._data_directory / "1_reference.cpp")
        self._test_runner.cmd_args.config = str(
            self._data_directory / "valid_cpptest_flow.yaml")

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
        # asserter.assertStdOutNumAndFile(7, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
