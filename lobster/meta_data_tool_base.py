from abc import abstractmethod, ABCMeta
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from lobster.version import FULL_NAME


BUG_URL = "https://github.com/bmw-software-engineering/lobster/issues"


class MetaDataToolBase(metaclass=ABCMeta):
    def __init__(
            self,
            name: str,
            description: str,
            official: bool,
    ) -> None:
        """Base class for LOBSTER tools.

           It provides an ArgumentParser and implements the --version and --help
           features.

        params:
            name (str): The name of the tool, without the 'lobster-' prefix.
            description (str): A brief description of the tool.
              It will be used in the help message.
            official (bool): Whether the tool is an official LOBSTER tool.
               This flag determines the URL for the bug ticker."""

        self._name = f"lobster-{name}"
        self._argument_parser = ArgumentParser(
            prog = self._name,
            description = description,
            epilog = (f"Part of {FULL_NAME}, licensed under the AGPLv3."
                      f" Please report bugs to {BUG_URL}."
                      if official else None),
            allow_abbrev = False,
            formatter_class=RawTextHelpFormatter,
        )
        self._argument_parser.add_argument(
            "-v",
            "--version",
            action="version",
            default=None,
            help="print version and exit",
            version=FULL_NAME,
        )

    @property
    def name(self) -> str:
        """The name of the tool, prefixed with 'lobster-'."""
        return self._name

    def run(self) -> int:
        """
        Parse the command line arguments and return the parsed namespace.

        If the --version or --help flag is set, it prints those messages.
        Otherwise it calls the _run_impl method with the parsed arguments.
        """
        args = self._argument_parser.parse_args()
        return self._run_impl(args)

    @abstractmethod
    def _run_impl(self, options: Namespace) -> int:
        """This method should be implemented by subclasses to run the tool.

           The return value shall be an exit code.
        """
