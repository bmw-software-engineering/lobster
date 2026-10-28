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

"""A test which writes its result as a JUnit XML report, like pytest does.

pytest is no dependency of LOBSTER, so this test writes the report itself. Like
a pytest test it gets no command line arguments, but finds the location of the
report in the environment variable XML_OUTPUT_FILE. It also needs its runfiles
and the environment of its target.
"""

import os
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


class RunfilesTest(unittest.TestCase):
    def test_GivenRunfiles_ExpectDataFileReadable(self):
        runfile = Path(__file__).parent / "runfile.txt"
        self.assertEqual(runfile.read_text(encoding="UTF-8").strip(),
                         "content provided as runfile")


def write_report(path: str, successful: bool):
    testsuites = ET.Element("testsuites", name="integration tests")
    testsuite = ET.SubElement(testsuites, "testsuite", name="junit_writing_test")
    testcase = ET.SubElement(
        testsuite,
        "testcase",
        classname="junit_writing_test.RunfilesTest",
        name="test_GivenRunfiles_ExpectDataFileReadable",
    )
    properties = ET.SubElement(testcase, "properties")
    ET.SubElement(properties, "property", name="lobster-tracing",
                  value="stack.runfiles")
    ET.SubElement(properties, "property", name="environment",
                  value=os.environ.get("TARGET_ENVIRONMENT", ""))
    if not successful:
        ET.SubElement(testcase, "failure", message="test failed")
    ET.ElementTree(testsuites).write(path, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    result = unittest.main(exit=False).result
    if "XML_OUTPUT_FILE" in os.environ:
        write_report(os.environ["XML_OUTPUT_FILE"], result.wasSuccessful())
    sys.exit(0 if result.wasSuccessful() else 1)
