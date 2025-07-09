from typing import List


class CmdArgs:
    def __init__(self) -> None:
        self._args: List[str] = []

    def reset(self):
        """Resets the command line arguments"""
        self._args = []

    def append_arg(self, arg: str):
        """Appends an argument to the command line arguments"""
        self._args.append(arg)

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        return self._args
