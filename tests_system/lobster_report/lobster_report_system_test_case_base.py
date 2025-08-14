from pathlib import Path

from tests_system.lobster_report.lobster_report_test_runner import (
    LobsterReportTestRunner)
from tests_system.system_test_case_base import SystemTestCaseBase


class LobsterReportSystemTestCaseBase(SystemTestCaseBase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterReportTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterReportTestRunner(
            tool_name,
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
