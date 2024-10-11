"""
This script verifies if the test files of a given
target contains @requirement tag or not
"""
import logging
from pathlib import Path
from typing import List

from lobster.tools.cpptest.parser.test_case import TestCase


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
