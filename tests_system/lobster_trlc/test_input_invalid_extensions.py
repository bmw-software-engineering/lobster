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
from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)
from tests_system.asserter import Asserter


class TrlcInvalidExtensionsTest(LobsterTrlcSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.conversion_rules = [
            self.NAMASTE_CONVERSION_RULE,
        ]

    def test_invalid_extensions_inputs_files_list(self):
        # lobster-trace: trlc_req.Invalid_File_Extension
        self._test_runner.declare_input_file(self._data_directory /
                                             "rsl_invalid_extension.slr")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_invalid_extension.clrt")
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            "lobster-trlc: File rsl_invalid_extension.slr does not have a valid "
            "extension. Expected one of .rsl, .trlc, .trlc.md.\n"
        )
        asserter.assertExitCode(1)

    def test_invalid_extensions_input_from_file(self):
        # lobster-trace: trlc_req.Invalid_File_Extension
        self._test_runner.declare_inputs_from_file(self._data_directory /
                                                   "invalid_ext_inputs_from_file.txt",
                                                   self._data_directory)
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertStdErrText(
            "lobster-trlc: File rsl_invalid_extension.slr does not have a valid "
            "extension. Expected one of .rsl, .trlc, .trlc.md.\n"
        )
        asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
