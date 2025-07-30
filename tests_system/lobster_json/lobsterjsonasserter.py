from ..asserter import Asserter


# Setting this flag will tell unittest not to print tracebacks from this frame.
# This way our custom assertions will show the interesting line number from the caller
# frame, and not from this boring file.
__unittest = True


class LobsterJsonAsserter(Asserter):
    def assertStdOutNumAndFile(self, num_items: int, out_file: str):
        self.assertStdOutText(
            f"lobster-json: wrote {num_items} items to {out_file}\n"
        )
