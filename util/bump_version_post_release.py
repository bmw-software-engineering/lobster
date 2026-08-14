#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2022-2024 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

import os
import subprocess

import util.changelog

from lobster.common.version import VERSION_TUPLE

# Under `bazel run`, use the real workspace root so relative paths
# target repository files instead of Bazel runfiles/symlinks.
workspace_root = os.environ.get("BUILD_WORKSPACE_DIRECTORY")
if workspace_root:
    os.chdir(workspace_root)

major, minor, release = VERSION_TUPLE
release += 1

# Bump version and update version.py

VERSION_FILE = os.path.join("lobster", "common", "version.py")

# pylint: disable=invalid-name
tmp = ""
with open(VERSION_FILE, encoding="UTF-8") as fd:
    for raw_line in fd:
        if raw_line.startswith("VERSION_TUPLE"):
            raw_line = f'VERSION_TUPLE = ({major}, {minor}, {release})\n'
        elif raw_line.startswith("VERSION_SUFFIX"):
            raw_line = 'VERSION_SUFFIX = "dev"\n'

        tmp += raw_line
with open(VERSION_FILE, "w", encoding="UTF-8") as fd:
    fd.write(tmp)

LOBSTER_VERSION = f"{major}.{minor}.{release}-dev"

# Update changelog, adding a new entry

util.changelog.add_new_section(LOBSTER_VERSION)

# Assemble commit

subprocess.run(["git", "add", "CHANGELOG.md", VERSION_FILE], check=True)
subprocess.run(
    ["git", "commit", "-m", f"Bump version to {LOBSTER_VERSION} after release"],
    check=True,
)
