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

import unittest
from tests_system.asserter import Asserter
from tests_system.lobster_json.lobsterjsonsystemtestcasebase import (
    LobsterJsonSystemTestCaseBase
)


class ValidInputTest(LobsterJsonSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_input_with_specific_schema(self):
        # lobster-trace: UseCases.Incorrect_number_of_requirement_refs_in_JSON_Output
        out_file = "specific_schema.lobster"
        self._test_runner.cmd_args.out = out_file

        self._test_runner.config_file_data.tag_attribute = "requirements"
        self._test_runner.config_file_data.name_attribute = "description"

        self._test_runner.declare_output_file(self._data_directory / out_file)
        self._test_runner.declare_input_file(self._data_directory /
                                             "specific_schema.json")

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            "lobster-json: wrote 2 items to specific_schema.lobster\n"
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
