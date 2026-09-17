# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2024-2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

import re


class Constants:
    def __init__(self, codebeamer_url = ''):

        self.codebeamer_link = codebeamer_url + "/issue/"
        self.requirement = re.compile(r'@requirement[\s\S]*?(?=@|\Z)')
        self.requirement_tag_http = (
            rf"([@\\]requirement(\s+(CB-#\d+\s+)*"
            rf"({self.codebeamer_link}\d+\s*,?\s*/*\*?)+)+)"
        )
        self.requirement_tag_http_named = rf"({self.codebeamer_link}(?P<number>\d+))"

    NON_EXISTING_INFO = "---"

    LOBSTER_GENERATOR = "lobster-cpptest"

    VALID_TESTMETHODS = [
        "TM_EQUIVALENCE",
        "TM_PAIRWISE",
        "TM_GUESSING",
        "TM_BOUNDARY",
        "TM_CONDITION",
        "TM_REQUIREMENT",
        "TM_TABLE",
    ]

    VALID_TEST_MACROS = [
        "TEST",
        "TEST_P",
        "TEST_F",
        "TYPED_TEST",
        "TYPED_TEST_P",
        "TYPED_TEST_SUITE",
        "TEST_P_INSTANCE",
        "TEST_F_INSTANCE",
    ]

    TEST_CASE_INTRO = re.compile(r"^\s*(" +
                                 "|".join(VALID_TEST_MACROS) +
                                 r")\s*\(")
    TEST_CASE_INFO = re.compile(
        r"^\s*(" + "|".join(VALID_TEST_MACROS) +
        r")\s*\(\s*(?P<suite_name>\w+),\s*(?P<test_name>\w+)\)"
    )
    REQUIREMENT_TAG = r"(CB-#\d+)"

    REQUIRED_BY = re.compile(r".*[@\\]requiredby\s+([\s*/]*(\w*::\w+),?\s*)+")
    REQUIRED_BY_TAG = r"(\w*::\w+)"
    DEFECT = re.compile(
        r"(@defect\s+)(((?:(CB-#\d+)|(OCT-#\d+)),?\s*)+)" +
        r"(?:///|/)\s+(((?:(CB-#\d+)|(OCT-#\d+)),?\s)+)?"
    )
    BRIEF = re.compile(r"(@brief\s+)([^@]+)")
    VERSION = re.compile(r"(@version\s+)(\d+([,]? \d+)*)+")
    OCT_TAG = r"(OCT-#\d+)"
    TESTMETHODS = re.compile(r"(@testmethods\s+)([^@]+)")
    TEST = re.compile(r"(@test\s+)([^@]+)")
