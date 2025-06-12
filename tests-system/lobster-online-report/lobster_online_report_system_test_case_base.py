from pathlib import Path
from typing import Optional, Union
from .lobster_online_report_test_runner import LobsterOnlineReportTestRunner
from ..system_test_case_base import SystemTestCaseBase


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
            tool_name,
            self.create_temp_dir(prefix=f"test-{tool_name}-",
                                 dir_path=working_dir),
        )
        return test_runner
