import math
from typing import Optional
from tests_system.asserter import Asserter, is_valid_json, sort_json
from pathlib import Path


class LobsterCodebeamerAsserter(Asserter):
    def __init__(self, system_test_case, completed_process, test_runner,
                 port: int = 8999):
        super().__init__(system_test_case, completed_process, test_runner)
        self._port = port

    def apply_replacements(self, content: str) -> str:
        """
        Override to add MOCK_SERVER_PORT replacement in addition to base replacements.
        """
        # First apply parent replacements (CURRENT_WORKING_DIRECTORY)
        content = super().apply_replacements(content)
        # Then add codebeamer-specific replacement (MOCK_SERVER_PORT)
        return content.replace(
            "MOCK_SERVER_PORT",
            str(self._port),
        )

    def assertStdOutNumAndFile(
            self,
            num_items: int,
            page_size: int,
            out_file: str = "codebeamer.lobster",
            import_query: Optional[int] = None,
            port: int = 8999,
    ):
        if num_items == 0:
            if import_query is None:
                self._test_case.fail("Invalid assertion call: If zero items are "
                                     "expected then the import query must be provided!")
            if isinstance(import_query, int):
                message = (
                    f"Fetching page 1 of query...\n"
                    f"This query doesn't generate items. Please check:\n"
                    f" * is the number actually correct?\n"
                    f" * do you have permissions to access it?\n"
                    f"You can try to access 'https://localhost:{port}/api/v3/reports"
                    f"/{import_query}/items?page=1&pageSize={page_size}' manually to "
                    f"check.\n"
                    f"Written 0 requirements to {out_file}\n"
                )
            else:
                message = (
                    f"Fetching page 1 of query...\n"
                    f"This query doesn't generate items. Please check:\n"
                    f" * is the number actually correct?\n"
                    f" * do you have permissions to access it?\n"
                    f"You can try to access 'https://localhost:{port}/api/v3/items"
                    f"/query?page=1&pageSize={page_size}&queryString={import_query}' "
                    f"manually to check.\n"
                    f"Written 0 requirements to {out_file}\n"
                )
        else:
            total_pages = math.ceil(num_items / page_size)
            fetch_messages = ''.join(
                f"Fetching page {i} of query...\n" for i in range(1, total_pages + 1)
            )
            message = (
                fetch_messages +
                f"Written {num_items} requirements "
                f"to {out_file}\n"
            )
        self.assertStdOutText(message)
