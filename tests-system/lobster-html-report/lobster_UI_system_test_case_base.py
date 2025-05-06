from pathlib import Path
from .lobster_UI_test_runner import LobsterUITestRunner
from ..system_test_case_base import SystemTestCaseBase


class LobsterUISystemTestCaseBase(SystemTestCaseBase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterUITestRunner:
        tool_name = Path(__file__).parents[0].name
        working_dir = Path(__file__).parents[2]
        test_runner = LobsterUITestRunner(
            tool_name,
            self.create_temp_dir(prefix=f"test-{tool_name}-", dir_path=working_dir),
        )
        return test_runner
