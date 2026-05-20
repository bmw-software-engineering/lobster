from pathlib import Path
from tests_system.lobster_rst_report.lobster_rst_report_test_runner import (
    LobsterRstReportTestRunner,
)
from tests_system.system_test_case_base import SystemTestCaseBase


class LobsterRstReportSystemTestCaseBase(SystemTestCaseBase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterRstReportTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterRstReportTestRunner(
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
