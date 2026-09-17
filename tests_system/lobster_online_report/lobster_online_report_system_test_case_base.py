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
from typing import Optional, Union
from tests_system.lobster_online_report.\
    lobster_online_report_test_runner import LobsterOnlineReportTestRunner
from tests_system.system_test_case_base import SystemTestCaseBase


class LobsterOnlineReportSystemTestCaseBase(SystemTestCaseBase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self, working_dir: Optional[Union[str, Path]] = None) -> (
            LobsterOnlineReportTestRunner):
        tool_name = Path(__file__).parents[0].name
        if not working_dir:
            working_dir = Path(__file__).parents[2]
        test_runner = LobsterOnlineReportTestRunner(
            self.create_temp_dir(prefix=f"test-{tool_name}-",
                                 dir_path=working_dir),
        )
        return test_runner
