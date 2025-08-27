from pathlib import Path
from tests_system.lobster_trlc.lobster_trlc_test_runner import LobsterTrlcTestRunner
from tests_system.system_test_case_base import SystemTestCaseBase


class LobsterTrlcSystemTestCaseBase(SystemTestCaseBase):
    NAMASTE_CONVERSION_RULE = {
        "package": "test_default",
        "record-type": "namaste",
        "namespace": "req",
        "description-fields": ["description"],
    }

    BERRY_CONVERSION_RULE = {
        "package": "sweet_fruits",
        "record-type": "berry",
        "namespace": "req",
        "description-fields": ["description"],
    }

    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterTrlcTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterTrlcTestRunner(
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
