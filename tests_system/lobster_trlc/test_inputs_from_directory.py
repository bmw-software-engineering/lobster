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

import os
import shutil
import unittest
from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)
from tests_system.asserter import Asserter


class InputFromDirectory(LobsterTrlcSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.conversion_rules = [
            self.BERRY_CONVERSION_RULE,
            self.NAMASTE_CONVERSION_RULE,
        ]

    def test_input_from_directory(self):
        """Test that a directory is processed"""
        # lobster-trace: trlc_req.Input_Directory_Traversal

        # TODO: the test folder structure is not recursive, but it should be
        OUT_FILE = "input_from_working_directory.lobster"
        self._test_runner.cmd_args.out = OUT_FILE
        self._test_runner.declare_output_file(self._data_directory / OUT_FILE)
        file_paths = [
            self._data_directory / "fruits.trlc",
            self._data_directory / "fruits.rsl",
            self._data_directory / "default_file.trlc",
            self._data_directory / "default_file.rsl"
        ]
        self._test_runner.copy_files_in_working_directory(file_paths)
        os.makedirs(self._test_runner.working_dir / "nested", exist_ok=True)
        shutil.copy(
            self._data_directory / "fruits_nested.trlc",
            self._test_runner.working_dir / "nested" / "fruits_nested.trlc"
        )
        self._test_runner.config_file_data.inputs = ["."]
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"lobster-trlc: wrote 3 items to "
                                  f"{OUT_FILE}\n")
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
