import math
from ..asserter import Asserter


class LobsterCodebeamerAsserter(Asserter):
    def assertStdOutNumAndFile(self, num_items: int = 1,
                               out_file: str = "codebeamer.lobster",
                               page_size: int = 1):
        if num_items == 0:
            message = (
                f"Fetching page 1 of query...\n"
                f"This query doesn't generate items. Please check:\n"
                f" * is the number actually correct?\n"
                f" * do you have permissions to access it?\n"
                f"You can try to access 'https://localhost:8999/api/v3/reports"
                f"/1234458/items?page=1&pageSize={page_size}' manually to check.\n"
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
