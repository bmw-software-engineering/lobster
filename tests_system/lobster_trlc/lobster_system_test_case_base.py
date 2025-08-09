from pathlib import Path
from .lobster_trlc_test_runner import LobsterTrlcTestRunner
from ..system_test_case_base import SystemTestCaseBase


class LobsterTrlcSystemTestCaseBase(SystemTestCaseBase):
    # conversion rules for the "namaste" record type
    NAMASTE_CONVERSION_RULE = {
        "package": "test_default",
        "record_type": "namaste",
        "namespace": "req",
        "description_fields": ["description"],
    }

    BERRY_CONVERSION_RULE = {
        "package": "sweet_fruits",
        "record_type": "berry",
        "namespace": "req",
        "description_fields": ["description"],
    }

    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterTrlcTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterTrlcTestRunner(
            tool_name,
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
