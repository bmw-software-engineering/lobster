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
from tests_system.lobster_json.lobsterjsontestrunner import LobsterJsonTestRunner
from tests_system.system_test_case_base import SystemTestCaseBase


class LobsterJsonSystemTestCaseBase(SystemTestCaseBase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner_without_config_file_data(self) -> LobsterJsonTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterJsonTestRunner(
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
            use_config_file_data=False
        )
        return test_runner

    def create_test_runner(self) -> LobsterJsonTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterJsonTestRunner(
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
