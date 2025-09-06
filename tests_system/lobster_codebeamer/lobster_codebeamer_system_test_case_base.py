from pathlib import Path
from tests_system.lobster_codebeamer.lobster_codebeamer_test_runner import (
    LobsterCodebeamerTestRunner)
from tests_system.system_test_case_base import SystemTestCaseBase


class LobsterCodebeamerSystemTestCaseBase(SystemTestCaseBase):
    MULTIPLICATOR = 100

    def __init__(self, methodName):
        super().__init__(methodName)
        self._data_directory = Path(__file__).parents[0] / "data"

    def create_test_runner(self) -> LobsterCodebeamerTestRunner:
        tool_name = Path(__file__).parents[0].name
        test_runner = LobsterCodebeamerTestRunner(
            self.create_temp_dir(prefix=f"test-{tool_name}-"),
        )
        return test_runner

    def create_item(self, item_id: int):
        return {
            "id": item_id,
            "name": f"Requirement {item_id}: Dynamic name",
            "status": {
                "id": item_id,
                "name": f"Status {item_id}",
                "type": "ChoiceOptionReference",
            },
            'tracker': {
                'id': item_id * self.MULTIPLICATOR * self.MULTIPLICATOR,
                'name': f'Tracker_{item_id}',
                'type': 'TrackerReference',
            },
            'version': item_id * self.MULTIPLICATOR
        }

    def create_mock_response_items(self,
                                   page: int,
                                   page_size: int,
                                   total: int,
                                   is_query_id: bool):
        """Create a mock response like codebeamer API paginated items."""
        if (total > self.MULTIPLICATOR):
            self.fail(
                f"Total items {total} exceeds multiplicator {self.MULTIPLICATOR}.")
        if is_query_id:
            items = [
                {
                    "item": self.create_item(i)
                }
                for i in range(
                    (page - 1) * page_size + 1, min(page * page_size, total) + 1)
            ]
        else:
            items = [
                self.create_item(i)
                for i in range(
                    (page - 1) * page_size + 1, min(page * page_size, total) + 1)
            ]
        return {
            "page": page,
            "pageSize": page_size,
            "total": total,
            "items": items
        }
