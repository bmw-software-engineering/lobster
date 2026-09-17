# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

from abc import ABCMeta, abstractmethod
from lobster.common.version import FULL_NAME
from tests_system.asserter import Asserter
from tests_system.lobster_meta_data_tool_base.\
    lobster_meta_data_tool_base_test_runner import IMPLEMENTATION_MESSAGE


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
