import os
from pathlib import Path
from .lobster_UI_test_runner import LobsterUITestRunner
import importlib

system_test_case_base = importlib.import_module('tests-system.system_test_case_base')


class LobsterUISystemTestCaseBase(system_test_case_base.SystemTestCaseBase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterUITestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterUITestRunner(
            tool_name,
            self.create_temp_dir(prefix=f"test-{tool_name}-", dir_path=os.getcwd()),
        )
        return test_runner
