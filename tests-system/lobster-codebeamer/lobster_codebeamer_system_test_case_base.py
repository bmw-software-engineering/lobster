from pathlib import Path
from .lobster_codebeamer_test_runner import LobsterCodebeamerTestRunner
from ..system_test_case_base import SystemTestCaseBase


class LobsterCodebeamerSystemTestCaseBase(SystemTestCaseBase):

    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterCodebeamerTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterCodebeamerTestRunner(
            tool_name,
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner

    def set_config_file(self, retry_codes=None, num_retries=None):
        cfg = self._test_runner.config_file_data
        cfg.import_query = 1234458
        cfg.root = "https://localhost:8999"
        cfg.token = "abcdef1234567890"
        cfg.out = "codebeamer.lobster"
        if retry_codes is not None:
            cfg.retry_error_codes = retry_codes
        if num_retries is not None:
            cfg.num_request_retry = num_retries
