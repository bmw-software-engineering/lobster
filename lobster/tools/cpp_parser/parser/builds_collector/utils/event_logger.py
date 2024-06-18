import logging as lg
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from os.path import dirname
from pathlib import Path
from typing import Any, Generator, NamedTuple

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.constants_utils import DATE_FORMAT
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.directory_utils import (
    ensure_directory,
)


class Event(NamedTuple):
    """This class is used to preserve message and severity of an event"""

    severity: int
    message: str


def singleton(cls: Any) -> Any:
    # Disabled since pylint is not compilent with singleton arch.
    # pylint: disable=global-variable-undefined
    """Returns a singleton object of a class

    Parameters
    ----------
    cls: Any
        Could be any class

    Returns
    -------
    INSTANCE
        Singleton instance of a class
    """
    levels = []
    global INSTANCE
    INSTANCE = cls(levels)
    return INSTANCE


@singleton
class logging:
    # Disabled since check does not like upper case level naming
    # pylint: disable=invalid-name
    """This class is used to log events with various levels"""

    def __init__(self, levels: list):
        if not levels:
            levels = [CRITICAL, ERROR, WARNING]
        self.events = []
        self.initialized = False
        self.levels = levels
        self.ERROR = ERROR
        self.CRITICAL = CRITICAL
        self.WARNING = WARNING
        self.INFO = INFO
        self.DEBUG = DEBUG

    def basicConfig(
        self,
        filename: str = None,
        level: int = DEBUG,
        filemode: str = "w",
        handler_format: str = "%(asctime)s %(levelname)-8s %(message)s",
        datefmt: str = DATE_FORMAT,
    ) -> None:
        """Do basic configuration for the logging system.

        Parameters
        ----------
        filename: str
            Specifies that a FileHandler be created, using the specified filename
        level: int
            Set the root logger level to the specified level
        filemode: str
            Specifies the mode to open the file, if filename is specified
            (if filemode is unspecified, it defaults to 'w')
        handler_format: str
            Use the specified format string for the handler.
        datefmt: str
            Use the specified date/time format.
        """
        if self.initialized:
            self._log_checked(
                ERROR,
                "logging may not be configured more than once, " "due to a restriction of the python logging library.",
            )
            return
        if filename is None:
            lg.basicConfig(
                format=handler_format,
                level=level,
                datefmt=datefmt,
            )
        else:
            ensure_directory(Path(dirname(filename)))
            lg.basicConfig(
                handlers=[lg.FileHandler(filename, mode=filemode), lg.StreamHandler()],
                format=handler_format,
                level=level,
                datefmt=datefmt,
            )
        self.initialized = True

    def critical(self, message: str) -> None:
        """Critical message to be logged

        Parameters
        ----------
        message: str
            Message text
        """
        self._log_checked(CRITICAL, message)

    def error(self, message: str) -> None:
        """Error message to be logged

        Parameters
        ----------
        message: str
            Message text
        """
        self._log_checked(ERROR, message)

    def warning(self, message: str) -> None:
        """Warning message to be logged

        Parameters
        ----------
        message: str
            Message text
        """
        self._log_checked(WARNING, message)

    def info(self, message: str) -> None:
        """Info message to be logged

        Parameters
        ----------
        message: str
            Message text
        """
        self._log_checked(INFO, message)

    def debug(self, message: str) -> None:
        """Debug message to be logged

        Parameters
        ----------
        message: str
            Message text
        """
        self._log_checked(DEBUG, message)

    def getLevelName(self, severity: int) -> str:
        # Disabled since pylint wants to make this method a function
        # but design is preserved
        # pylint: disable=no-self-use
        """Return the textual or numeric representation of logging level 'level'.

        The corresponding string representation of one of the levels is returned.

        Parameters
        ----------
        severity: int
            Numeric value representation of the level

        Returns
        ----------
        str
            String representation of the level
        """
        return lg.getLevelName(severity)

    def flush(self, level: int = DEBUG) -> Generator:
        """Clears events list

        Parameters
        ----------
        level: int
            Level of the log

        Returns
        ----------
        str
            Returns a generator consisting of logs whose severity is matching or higher
            than provided level.
        """
        for e in self.events:
            if e.severity >= level:
                yield e
        self.events = []

    def _log_checked(self, severity: int, message: str) -> None:
        """Logs the message with the specified severity.

        If logging class is not configured(initialized) the function will log also
        'not configured' message

        Parameters
        ----------
        severity: int
            Numeric value representation of the level
        message: str
            Text representation of the message
        """
        if not self.initialized:
            init_warning = "logging was not configured. Please call basicConfig() first."
            self._log_raw(WARNING, init_warning)
        self._log_raw(severity, message)

    def _log_raw(self, severity: int, message: str) -> None:
        """Logs the message with the specified severity.

        Parameters
        ----------
        severity: int
            Numeric value representation of the level
        message: str
            Text representation of the message
        """
        lg.log(severity, message)
        if severity in self.levels:
            self.events.append(Event(severity, message))
