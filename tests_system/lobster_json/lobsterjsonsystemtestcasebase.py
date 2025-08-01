from pathlib import Path
from .lobsterjsontestrunner import LobsterJsonTestRunner
from ..system_test_case_base import SystemTestCaseBase


class LobsterJsonSystemTestCaseBase(SystemTestCaseBase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterJsonTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterJsonTestRunner(
            tool_name,
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
