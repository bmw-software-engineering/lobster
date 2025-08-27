from pathlib import Path
from .lobster_pkg_test_runner import LobsterPKGTestRunner
from ..system_test_case_base import SystemTestCaseBase


class LobsterPKGSystemTestCaseBase(SystemTestCaseBase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterPKGTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterPKGTestRunner(
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
