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
from typing import Optional

import yaml
from yamale import YamaleError

from lobster.common.exceptions import LOBSTER_Exception
from lobster.common.location import File_Reference
from lobster.common.raw_policy import (
    RawLevel, RawPolicy, RawRequiresCandidate, RawSource, RawTraceTo,
)
from lobster.common.yaml_validation import validate_yaml_file

SCHEMA_FILE = Path(__file__).parent / "tracing_policy.yamale"


# pylint: disable-next=too-many-ancestors
class UniqueKeyLoader(yaml.SafeLoader):
    """Safe loader that rejects duplicate mapping keys instead of keeping the last."""

    def construct_mapping(self, node, deep=False):
        seen = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=True)
            if key in seen:
                raise yaml.constructor.ConstructorError(
                    None, None, f"duplicate key {key!r}", key_node.start_mark)
            seen.add(key)
        return super().construct_mapping(node, deep)


def _line_of_path(filename: str, path: str) -> Optional[int]:
    """Return the 1-based line of a yamale error path like 'levels.0.kind'.

    Falls back to the deepest node that exists, e.g. for missing keys.
    """
    with open(filename, "r", encoding="UTF-8") as f:
        node = yaml.compose(f, Loader=yaml.SafeLoader)
    if node is None:
        return None
    for part in path.split("."):
        child = None
        if isinstance(node, yaml.MappingNode):
            for key_node, value_node in node.value:
                if key_node.value == part:
                    child = value_node
                    break
        elif isinstance(node, yaml.SequenceNode) and part.isdigit():
            index = int(part)
            if index < len(node.value):
                child = node.value[index]
        if child is None:
            break
        node = child
    return node.start_mark.line + 1


def _describe_error(filename: str, err: Exception) -> str:
    if isinstance(err, yaml.YAMLError):
        mark = getattr(err, "problem_mark", None)
        where = f"{filename}:{mark.line + 1}" if mark else filename
        return f"{where}: invalid tracing policy: {err}"

    messages = []
    for result in err.results:
        for error in result.errors:
            path, _, text = str(error).partition(": ")
            line = _line_of_path(filename, path) if text else None
            where = f"{filename}:{line}" if line else filename
            messages.append(f"{where}: invalid tracing policy: {error}")
    return "\n".join(messages) or f"{filename}: invalid tracing policy: {err}"


def read_yaml_policy(filename: str) -> RawPolicy:
    if not Path(filename).is_file():
        raise FileNotFoundError(f"Config file not found: {filename}")

    try:
        with open(filename, "r", encoding="UTF-8") as f:
            data = yaml.load(f, Loader=UniqueKeyLoader)
        validate_yaml_file(schema_file=SCHEMA_FILE, filename=filename)
    except (YamaleError, yaml.YAMLError) as err:
        raise LOBSTER_Exception(_describe_error(filename, err)) from err

    loc = File_Reference(filename)
    levels = []
    for level_data in data.get("levels", []):
        level = RawLevel(name=level_data["name"],
                          name_loc=loc,
                          kind=level_data["kind"])
        for source_file in level_data.get("source") or []:
            level.source.append(RawSource(file=source_file, loc=loc))
        for target in level_data.get("trace-to") or []:
            level.trace_to.append(RawTraceTo(target=target, loc=loc))
        for or_group in level_data.get("requires") or []:
            level.requires.append(
                [RawRequiresCandidate(name=name, loc=loc)
                 for name in or_group])
        levels.append(level)

    return RawPolicy(levels=levels)
