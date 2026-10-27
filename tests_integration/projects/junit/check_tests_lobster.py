# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

"""Checks the LOBSTER file which lobster_junit creates from the test reports."""

import json
import sys
import unittest

LOBSTER_FILE = sys.argv.pop()


class TestsLobsterTest(unittest.TestCase):
    def test_items_of_googletest_and_python_test(self):
        with open(LOBSTER_FILE, encoding="UTF-8") as lobster_file:
            items = {item["tag"]: item for item in json.load(lobster_file)["data"]}

        self.assertEqual(
            sorted(items),
            [
                "gtest Stack:GivenEmptyStack_ExpectSizeZero",
                "junit junit_writing_test.RunfilesTest:"
                "test_GivenRunfiles_ExpectDataFileReadable",
            ],
        )

        gtest_item = items["gtest Stack:GivenEmptyStack_ExpectSizeZero"]
        self.assertEqual(gtest_item["status"], "ok")
        self.assertEqual(gtest_item["refs"], ["req stack.size"])
        self.assertEqual(gtest_item["text"], ":Given: empty stack\n:Then: size zero")

        python_item = items[
            "junit junit_writing_test.RunfilesTest:"
            "test_GivenRunfiles_ExpectDataFileReadable"
        ]
        self.assertEqual(python_item["status"], "ok")
        self.assertEqual(python_item["framework"], "JUnit")
        self.assertEqual(python_item["refs"], ["req stack.runfiles"])
        self.assertEqual(
            python_item["text"],
            ":Environment: from target env\n"
            ":Given: runfiles\n"
            ":Then: data file readable",
        )


if __name__ == "__main__":
    unittest.main()
