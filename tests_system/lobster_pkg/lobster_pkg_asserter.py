from ..asserter import Asserter


# Setting this flag will tell unittest not to print tracebacks from this frame.
# This way our custom assertions will show the interesting line number from the caller
# frame, and not from this boring file.
__unittest = True


class LobsterPkgAsserter(Asserter):
    def assertStdOutNumAndFile(self, num_items: int, out_file: str):
        self.assertStdOutText(
            f"lobster-pkg: wrote {num_items} items to {out_file}\n"
        )

    def assertStdOutNumAndFileDeprecated(
            self,
            num_items: int,
            out_file: str,
            schema: str,
            version: int):
        self.assertStdOutText(
            f"Lobster file version {version} "
            f"containing 'schema' = '{schema}' is deprecated, "
            f"please migrate to version 5\n"
            f"lobster-pkg: wrote {num_items} items to {out_file}\n"
        )
