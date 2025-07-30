from pathlib import Path
from .lobster_meta_data_tool_base_test_runner import LobsterMetaDataToolBaseTestRunner
from ..system_test_case_base import SystemTestCaseBase


class LobsterMetaDataToolBaseSystemTestCaseBase(SystemTestCaseBase):
    def create_test_runner(self) -> LobsterMetaDataToolBaseTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterMetaDataToolBaseTestRunner(
            tool_name,
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner
