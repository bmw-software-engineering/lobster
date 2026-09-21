# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2024-2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

"""
This script verifies if the test files of a given
target contains @requirement tag or not
"""
import logging
from pathlib import Path
from typing import List

from lobster.tools.cpptest.testcase import TestCase


class ParserForRequirements:
    @staticmethod
    def collect_test_cases_for_test_files(
            test_files: List[Path],
            codebeamer_url: str = "",
    ) -> List:
        """
        Parse a list of source files for test cases

        Parameters
        ----------
        test_files: List[Path]
            Source files to parse
        codebeamer_url: str

        Returns
        -------
        List[TestCase]
           List of parsed TestCase
        """
        test_cases = []

        for file in set(test_files):
            file_test_cases = (
                ParserForRequirements.collect_test_cases(file, codebeamer_url))
            test_cases.extend(file_test_cases)

        return test_cases

    @staticmethod
    def collect_test_cases(
            file: Path,
            codebeamer_url: str = "",
    ) -> List[TestCase]:
        """
        Parse a source file for test cases

        Parameters
        ----------
        file: Path
            Source file to parse
        codebeamer_url: str

        Returns
        -------
        List[TestCase]
           List of parsed TestCase
        """

        try:
            with open(file, "r", encoding="UTF-8", errors="ignore") as f:
                lines = f.readlines()

        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.error("exception %s", e)
            return []

        test_cases = []

        for i in range(0, len(lines)):
            test_case = TestCase.try_parse(file, lines, i, codebeamer_url)

            if test_case:
                test_cases.append(test_case)
        return test_cases
