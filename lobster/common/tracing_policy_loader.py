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

# Picks the tracing-policy reader based on the config file's extension, then
# hands the resulting RawPolicy to build_tracing_policy() regardless of
# which reader produced it.

from pathlib import Path
from typing import OrderedDict

from lobster.common.level_definition import LevelDefinition
from lobster.common.parser import Parser
from lobster.common.policy_builder import build_tracing_policy
from lobster.common.yaml_policy_reader import read_yaml_policy

YAML_EXTENSIONS = (".yaml", ".yml")


def load_tracing_policy(
    mh,
    filename: str,
) -> OrderedDict[str, LevelDefinition]:
    """Load a tracing policy and return its level definitions by name.

    Returns:
        An ordered mapping from each level's name to its ``LevelDefinition``.
    """
    if Path(filename).suffix.lower() in YAML_EXTENSIONS:
        raw_policy = read_yaml_policy(filename)
    else:
        print(f"{filename}: warning: the tracing-policy in the LOBSTER configuration "
              "language is deprecated and will be removed in a future "
              "release. Use a .yaml file instead")
        raw_policy = Parser(mh, filename).parse()
    return build_tracing_policy(raw_policy)
