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

# Shared yamale-based validation for LOBSTER's YAML config files.

from pathlib import Path

import yamale


def validate_yaml_file(schema_file, filename: str):
    """Validates a YAML file against a yamale schema file."""
    schema = yamale.make_schema(schema_file)
    # Read as UTF-8 ourselves, since yamale would use the platform's default encoding.
    # The resolved path is attached so that yamale prints it in validation errors.
    resolved = str(Path(filename).resolve())
    with open(filename, "r", encoding="UTF-8") as f:
        content = f.read()
    data = [(item, resolved) for item, _ in yamale.make_data(content=content)]
    yamale.validate(schema, data)
