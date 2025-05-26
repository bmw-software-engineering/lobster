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

    def set_config_file_data(self, retry_codes=None, num_retries=None):
        cfg = self._test_runner.config_file_data
        cfg.import_query = 1234458
        cfg.root = "https://localhost:8999"
        cfg.token = "abcdef1234567890"
        cfg.out = "codebeamer.lobster"
        if retry_codes is not None:
            cfg.retry_error_codes = retry_codes
        if num_retries is not None:
            cfg.num_request_retry = num_retries

    def create_mock_response_items(self, page: int, page_size: int, total: int):
        """Create a mock response like codebeamer API paginated items."""
        MULTIPLICATOR = 100
        if (total > MULTIPLICATOR):
            self.fail(
                f"Total items {total} exceeds multiplicator {MULTIPLICATOR}.")
        items = [
            {
                "item": {
                    "id": i,
                    "name": f"Requirement {i}: Dynamic name",
                    "description": f"Dynamic description for requirement {i}.",
                    "status": {
                        "id": i,
                        "name": f"Status {i}",
                        "type": "ChoiceOptionReference",
                    },
                    'tracker': {
                        'id': i * MULTIPLICATOR * MULTIPLICATOR,
                        'name': f'Tracker_{i}',
                        'type': 'TrackerReference',
                    },
                    'version': i * MULTIPLICATOR
                }
            }
            for i in range(
                (page - 1) * page_size + 1, min(page * page_size, total) + 1)
        ]
        return {
            "page": page,
            "pageSize": page_size,
            "total": total,
            "items": items
        }
