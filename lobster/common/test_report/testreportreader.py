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

import sys
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import ClassVar, Dict, Iterable, List, Optional, Set, Tuple

from lobster.common.items import Activity, Tracing_Tag
from lobster.common.location import File_Reference, Location, Void_Reference
from lobster.common.test_report.givenwhenthen import GivenWhenThen
from lobster.common.test_report.testcasedata import TestCaseData


class TestReportReader(ABC):
    """Converts the test cases of one dialect of JUnit XML into LOBSTER activities.

    GoogleTest, pytest and other test frameworks write their results as dialects
    of the JUnit XML format. The conversion of a report follows the same steps for
    every dialect, implemented once in the template method ``read``. The steps
    which differ between dialects are hooks that subclasses implement:
    ``accepts``, ``suites``, ``uid`` and ``is_executed`` (abstract), and
    ``testcases``, ``has_failed``, ``source_line``, ``test_name_for_spec`` and
    ``references`` (with defaults).
    """

    namespace: ClassVar[str]
    """Namespace of the tags of the items, e.g. ``gtest`` in ``gtest Suite:Test``."""

    framework: ClassVar[str]
    """Name of the test framework, written to the items."""

    def __init__(
        self,
        derive_gwt_from_test_name: bool = False,
        source_files: Optional[Dict[str, Set[str]]] = None,
    ) -> None:
        """Constructor

        :param derive_gwt_from_test_name: whether to derive the Given, When and
            Then parts of the item text from the test name
        :param source_files: source files found next to the reports, by file
            name, used to resolve the file name of a test case to its path
        """
        self._derive_gwt_from_test_name = derive_gwt_from_test_name
        self._source_files = source_files or {}

    # Hooks -------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def accepts(cls, root: ET.Element) -> bool:
        """Returns whether a report with this root element is in this dialect."""

    @abstractmethod
    def suites(self, root: ET.Element) -> Iterable[ET.Element]:
        """Returns the test suites of a report."""

    @abstractmethod
    def uid(self, suite: ET.Element, testcase: ET.Element) -> str:
        """Returns the unique name of a test case, used in the tag of its item."""

    @abstractmethod
    def is_executed(self, testcase: ET.Element) -> bool:
        """Returns whether the test case ran, as opposed to being skipped."""

    def testcases(self, suite: ET.Element) -> Iterable[ET.Element]:
        """Returns the test cases of a test suite."""
        return (child for child in suite if child.tag == "testcase")

    def has_failed(self, testcase: ET.Element) -> bool:
        """Returns whether an executed test case failed."""
        return any(child.tag == "failure" for child in testcase)

    def source_line(self, testcase: ET.Element) -> Optional[int]:
        """Returns the line of the test case reported by the test framework."""
        if "line" in testcase.attrib:
            return int(testcase.attrib["line"])
        return None

    def test_name_for_spec(self, testcase: ET.Element) -> str:
        """Returns the test name from which Given, When and Then are derived."""
        return testcase.attrib["name"]

    def references(self, value: str) -> List[Tracing_Tag]:
        """Returns the requirements named by a ``lobster-tracing`` property."""
        return [Tracing_Tag("req", reference.strip()) for reference in value.split(",")]

    # Template method -----------------------------------------------------------

    def read(self, root: ET.Element) -> List[Activity]:
        """Converts every test case of a report into a LOBSTER activity."""
        return [
            self._to_activity(suite, testcase)
            for suite in self.suites(root)
            for testcase in self.testcases(suite)
        ]

    def _to_activity(self, suite: ET.Element, testcase: ET.Element) -> Activity:
        uid = self.uid(suite, testcase)
        status = self._status(testcase)
        data = self._parse_testcase(testcase)
        location = self._resolve_source(data.source_file, data.source_line)
        properties = self._text_properties(testcase, data, uid, location)

        item = Activity(
            tag=Tracing_Tag(self.namespace, uid),
            location=location,
            framework=self.framework,
            kind="test",
            text="\n".join(f":{name}: {value}" for name, value in properties) or None,
            status=status,
        )
        for reference in data.references:
            item.add_tracing_target(reference)
        return item

    def _status(self, testcase: ET.Element) -> str:
        if not self.is_executed(testcase):
            return "not run"
        if self.has_failed(testcase):
            return "fail"
        return "ok"

    def _parse_testcase(self, testcase: ET.Element) -> TestCaseData:
        data = TestCaseData(
            source_file=testcase.attrib.get("file", None),
            source_line=self.source_line(testcase),
        )
        for properties in testcase:
            if properties.tag != "properties":
                continue
            for prop in properties:
                assert prop.tag == "property"
                name = prop.attrib["name"]
                value = prop.attrib["value"]
                if name == "lobster-tracing":
                    data.references += self.references(value)
                elif name == "lobster-tracing-file":
                    data.source_file = value
                elif name == "lobster-tracing-line":
                    data.source_line = int(value)
                else:
                    data.properties[name] = value
        return data

    def _resolve_source(
        self, source_file: Optional[str], source_line: Optional[int]
    ) -> Location:
        candidates = self._source_files.get(source_file, set())
        if len(candidates) == 1:
            return File_Reference(filename=list(candidates)[0], line=source_line)
        if source_file is None:
            return Void_Reference()
        return File_Reference(filename=source_file, line=source_line)

    def _text_properties(
        self,
        testcase: ET.Element,
        data: TestCaseData,
        uid: str,
        location: Location,
    ) -> List[Tuple[str, str]]:
        properties = [
            (name.capitalize(), value) for name, value in data.properties.items()
        ]
        spec = (
            GivenWhenThen.from_test_name(self.test_name_for_spec(testcase))
            if self._derive_gwt_from_test_name
            else GivenWhenThen()
        )
        if spec.conflicts_with(properties):
            print(
                f"{location.to_string()}: lobster warning: test {uid} records "
                f"Given/When/Then properties, ignoring its name",
                file=sys.stderr,
            )
            return properties
        return spec.merge_into(properties)
