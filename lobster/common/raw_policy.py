#!/usr/bin/env python3
#
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

# Format-agnostic, unvalidated intermediate representation of a tracing
# policy, produced by a format-specific reader (e.g.
# lobster/common/parser.py) and consumed by
# lobster/common/policy_builder.py.

from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class RawSource:
    file: str
    loc: Any


@dataclass
class RawTraceTo:
    target: str
    loc: Any


@dataclass
class RawRequiresAlternative:
    name: str
    loc: Any


@dataclass
class RawLevel:
    name: str
    name_loc: Any
    kind: str
    source: List[RawSource] = field(default_factory=list)
    trace_to: List[RawTraceTo] = field(default_factory=list)
    # One entry per "requires" directive; each entry is the OR-list of
    # alternatives (one "requires: A or B;" line == one entry).
    requires: List[List[RawRequiresAlternative]] = field(default_factory=list)


@dataclass
class RawPolicy:
    levels: List[RawLevel] = field(default_factory=list)
