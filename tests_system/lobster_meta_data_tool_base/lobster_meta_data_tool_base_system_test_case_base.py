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
from tests_system.lobster_meta_data_tool_base.\
    lobster_meta_data_tool_base_test_runner import LobsterMetaDataToolBaseTestRunner
from tests_system.system_test_case_base import SystemTestCaseBase


class LobsterMetaDataToolBaseSystemTestCaseBase(SystemTestCaseBase):
    def create_test_runner(self) -> LobsterMetaDataToolBaseTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterMetaDataToolBaseTestRunner(
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
