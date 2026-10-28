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

import re
from dataclasses import dataclass
from typing import List, Tuple

_WORD = r"[A-Z0-9][A-Za-z0-9]*"

_TEST_NAME_PATTERN = re.compile(
    rf"(?:[A-Za-z0-9]+_)?Given(?P<given>{_WORD})"
    rf"(?:_When(?P<when>{_WORD}))?"
    rf"_(?:Expect|Then)(?P<then>{_WORD})"
)

_WORD_BOUNDARY = re.compile(
    r"(?<=[a-z0-9])(?=[A-Z])"
    r"|(?<=[A-Z])(?=[A-Z][a-z])"
    r"|(?<=[A-Za-z])(?=[0-9])"
)

_PART_NAMES = ("Given", "When", "Then")


def _camel_case_to_words(camel_case: str) -> str:
    return _WORD_BOUNDARY.sub(" ", camel_case).lower()


@dataclass(frozen=True)
class GivenWhenThen:
    """A Given-When-Then specification, where an unknown part is empty."""

    given: str = ""
    when: str = ""
    then: str = ""

    @classmethod
    def from_test_name(cls, test_name: str) -> "GivenWhenThen":
        """Derive the specification from a GoogleTest test name.

        The name must match
        ``(<Prefix>_)?Given<X>(_When<Y>)?_(Expect|Then)<Z>``,
        with every part in CamelCase. A ``/`` separates the segments of the
        name of a value-parameterized test. The last matching segment is used.
        If no segment matches, the result is empty.
        """
        result = cls()
        for segment in test_name.split("/"):
            match = _TEST_NAME_PATTERN.fullmatch(segment)
            if match:
                result = cls(
                    given=_camel_case_to_words(match["given"]),
                    when=_camel_case_to_words(match["when"] or ""),
                    then=_camel_case_to_words(match["then"]),
                )
        return result

    def is_empty(self) -> bool:
        return not (self.given or self.when or self.then)

    def conflicts_with(self, properties: List[Tuple[str, str]]) -> bool:
        """Return whether the properties already specify Given, When or Then.

        This is the case if this specification is not empty and any Given,
        When or Then property has a non-blank value.
        """
        return not self.is_empty() and any(
            name in _PART_NAMES and value.strip() for name, value in properties
        )

    def merge_into(
        self, properties: List[Tuple[str, str]]
    ) -> List[Tuple[str, str]]:
        """Add the non-empty parts to the properties.

        A property of the same name is replaced. Added parts are appended in
        the order Given, When, Then.
        """
        merged = list(properties)
        for name, value in zip(_PART_NAMES, (self.given, self.when, self.then)):
            if not value:
                continue
            merged = [(k, v) for k, v in merged if k != name]
            merged.append((name, value))
        return merged
