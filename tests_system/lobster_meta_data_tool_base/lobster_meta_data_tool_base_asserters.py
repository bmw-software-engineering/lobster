from abc import ABCMeta, abstractmethod
from lobster.common.version import FULL_NAME
from tests_system.asserter import Asserter


IMPLEMENTATION_MESSAGE = "This is the AppleBanana tool."


class SpecificAsserter(Asserter, metaclass=ABCMeta):
    """This class is an abstract base class. Implementors shall provide an
       implementation for the `assert_result` method.
    """

    @abstractmethod
    def assert_result(self):
        """Asserts the result of the tool execution.

           This function shall assert all relevant aspects of the tool's output,
           including stdout, stderr, and the exit code.
        """


class HelpAsserter(SpecificAsserter):
    def assert_result(self):
        """Assert that
          - the help message is printed correctly
          - the exit code is 0
        """

        self.assertNoStdErrText()

        self._test_case.assertIn(
            "usage: lobster-apple [-h] [-v]",
            self._completed_process.stdout,
        )

        self._test_case.assertIn("banana", self._completed_process.stdout)

        self._test_case.assertIn(
            f"Part of {FULL_NAME}, licensed under the AGPLv3. "
            f"Please report bugs to "
            f"https://github.com/bmw-software-engineering/lobster/issues.",
            self._completed_process.stdout,
        )

        self._test_case.assertNotIn(
            IMPLEMENTATION_MESSAGE,
            self._completed_process.stdout,
        )

        self.assertExitCode(0)


class VersionAsserter(SpecificAsserter):
    def assert_result(self):
        """Assert that
          - the version message is printed correctly
          - the exit code is 0
        """
        self.assertNoStdErrText()
        self.assertStdOutText(f"{FULL_NAME}\n")
        self.assertExitCode(0)
