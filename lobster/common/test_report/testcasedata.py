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


from dataclasses import dataclass, field
from typing import Dict, List, Optional

from lobster.common.items import Tracing_Tag


@dataclass
class TestCaseData:
    """The parts of a test case which do not depend on the report dialect."""

    references: List[Tracing_Tag] = field(default_factory=list)
    source_file: Optional[str] = None
    source_line: Optional[int] = None
    properties: Dict[str, str] = field(default_factory=dict)
