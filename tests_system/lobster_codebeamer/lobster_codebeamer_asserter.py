import math
from typing import Optional
from ..asserter import Asserter


class LobsterCodebeamerAsserter(Asserter):
    def assertStdOutNumAndFile(
            self,
            num_items: int,
            page_size: int,
            out_file: str = "codebeamer.lobster",
            import_query: Optional[int] = None,
    ):
        if num_items == 0:
            if import_query is None:
                self._test_case.fail("Invalid assertion call: If zero items are "
                                     "expected then the import query must be provided!")
            if not isinstance(import_query, int):
                # The URL is constructed in a different way for string import_query
                # and this function does not support this yet.
                raise NotImplementedError("Having a string as import_query is not "
                                          "supported yet by the test framework.")
            message = (
                f"Fetching page 1 of query...\n"
                f"This query doesn't generate items. Please check:\n"
                f" * is the number actually correct?\n"
                f" * do you have permissions to access it?\n"
                f"You can try to access 'https://localhost:8999/api/v3/reports"
                f"/{import_query}/items?page=1&pageSize={page_size}' manually to "
                f"check.\n"
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
