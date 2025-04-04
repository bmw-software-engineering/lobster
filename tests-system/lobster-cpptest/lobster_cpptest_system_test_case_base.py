from pathlib import Path
from .lobster_cpptest_test_runner import LobsterCpptestTestRunner
from ..system_test_case_base import SystemTestCaseBase


class LobsterCpptestSystemTestCaseBase(SystemTestCaseBase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterCpptestTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterCpptestTestRunner(
            tool_name,
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
