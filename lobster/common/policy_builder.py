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

# Format-agnostic validation + construction layer: turns a RawPolicy (built
# by a format-specific reader) into the OrderedDict[str, LevelDefinition]
# consumed by lobster/common/report.py. This is where all semantic checks
# (duplicate names, missing source files, self-trace, unknown trace
# targets/requires levels) live, so they apply identically regardless of
# which config file format was parsed.

import os.path
import collections

from lobster.common.level_definition import LevelDefinition
from lobster.common.raw_policy import RawPolicy


def build_tracing_policy(mh, raw_policy: RawPolicy):
    levels = collections.OrderedDict()

    # First pass: create every level up front, so later passes can refer to
    # a level regardless of whether it is declared before or after the
    # level referencing it.
    for raw_level in raw_policy.levels:
        if raw_level.name in levels:
            mh.error(raw_level.name_loc, "duplicate declaration")
        levels[raw_level.name] = LevelDefinition(
            name=raw_level.name,
            kind=raw_level.kind,
        )

    # Second pass: validate and populate source files and trace-to targets.
    for raw_level in raw_policy.levels:
        item = levels[raw_level.name]

        for raw_source in raw_level.source:
            if not os.path.isfile(raw_source.file):
                mh.error(raw_source.loc, f"cannot find file {raw_source.file}")
            item.source.append({"file": raw_source.file})

        for raw_trace in raw_level.trace_to:
            if raw_trace.target == raw_level.name:
                mh.error(raw_trace.loc, "cannot trace to yourself")
            elif raw_trace.target not in levels:
                mh.error(raw_trace.loc, f"unknown item {raw_trace.target}")
            else:
                levels[raw_trace.target].needs_tracing_down = True
            item.traces.append(raw_trace.target)
            item.needs_tracing_up = True

    # Third pass: resolve "requires" links now that every level's `traces`
    # list (populated above) is complete.
    for raw_level in raw_policy.levels:
        item = levels[raw_level.name]
        item.breakdown_requirements = []
        if raw_level.requires:
            for chain in raw_level.requires:
                new_chain = []
                for alt in chain:
                    if alt.name not in levels:
                        mh.error(alt.loc, f"unknown level {alt.name}")
                    if item.name not in levels[alt.name].traces:
                        mh.error(alt.loc,
                                 f"{alt.name} cannot trace to {item.name} items")
                    new_chain.append(alt.name)
                item.breakdown_requirements.append(new_chain)
        else:
            for src in levels.values():
                if item.name in src.traces:
                    item.breakdown_requirements.append([src.name])

    return levels
