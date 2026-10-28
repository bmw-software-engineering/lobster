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

import xml.etree.ElementTree as ET
from typing import Optional

from lobster.common.test_report.junitreportreader import JunitReportReader


class PytestReportReader(JunitReportReader):
    """Reads JUnit XML reports written by pytest (``--junitxml``).

    pytest names the root element ``pytest tests`` (``pytest`` before pytest
    5.1), reports the 0-based line of a test function, and appends the parameters
    of a parametrized test to its name as ``[<parameters>]``.
    """

    framework = "pytest"

    @classmethod
    def accepts(cls, root: ET.Element) -> bool:
        return super().accepts(root) and root.attrib.get("name", "").startswith(
            "pytest"
        )

    def source_line(self, testcase: ET.Element) -> Optional[int]:
        line = super().source_line(testcase)
        return None if line is None else line + 1

    def test_name_for_spec(self, testcase: ET.Element) -> str:
        return super().test_name_for_spec(testcase).split("[", 1)[0]
