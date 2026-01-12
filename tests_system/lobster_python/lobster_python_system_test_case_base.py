from pathlib import Path
from tests_system.lobster_python.\
    lobster_python_test_runner import LobsterPythonTestRunner
from tests_system.system_test_case_base import SystemTestCaseBase


class LobsterPythonSystemTestCaseBase(SystemTestCaseBase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterPythonTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterPythonTestRunner(
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
