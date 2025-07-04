from pathlib import Path
from .lobster_tool_base_test_runner import LobsterToolBaseTestRunner
from ..system_test_case_base import SystemTestCaseBase


class LobsterToolBaseSystemTestCaseBase(SystemTestCaseBase):
    def create_test_runner(self) -> LobsterToolBaseTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterToolBaseTestRunner(
            tool_name,
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
