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

# Reads a YAML tracing policy file into a RawPolicy, validating it against
# lobster/common/tracing_policy.yamale first (same precedent as
# lobster/tools/trlc/lobster_trlc_config.py).

from pathlib import Path

import yaml

from lobster.common.location import File_Reference
from lobster.common.raw_policy import (
    RawLevel, RawPolicy, RawRequiresCandidate, RawSource, RawTraceTo,
)
from lobster.common.yaml_validation import validate_yaml_file

SCHEMA_FILE = Path(__file__).parent / "tracing_policy.yamale"


def read_yaml_policy(filename: str) -> RawPolicy:
    validate_yaml_file(schema_file=SCHEMA_FILE, filename=filename)

    with open(filename, "r", encoding="UTF-8") as f:
        data = yaml.safe_load(f)

    loc = File_Reference(filename)
    levels = []
    for level_data in data.get("levels", []):
        level = RawLevel(name=level_data["name"],
                          name_loc=loc,
                          kind=level_data["kind"])
        for source_file in level_data.get("source", []):
            level.source.append(RawSource(file=source_file, loc=loc))
        for target in level_data.get("trace-to", []):
            level.trace_to.append(RawTraceTo(target=target, loc=loc))
        for or_group in level_data.get("requires", []):
            level.requires.append(
                [RawRequiresCandidate(name=name, loc=loc)
                 for name in or_group])
        levels.append(level)

    return RawPolicy(levels=levels)
