#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Tracability Evidence Report
# Copyright (C) 2022 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

# Helper script to remove "-dev" from current version; update
# changelog/docs; and commit.

import os

import util.changelog

# Update version.py to remove the -dev (or if given) use a different
# version number.

VERSION_FILE = os.path.join("lobster-core", "lobster", "version.py")

tmp = ""
with open(VERSION_FILE, "r") as fd:
    for raw_line in fd:
        if raw_line.startswith("VERSION_SUFFIX"):
            raw_line = 'VERSION_SUFFIX = ""\n'
        tmp += raw_line

with open(VERSION_FILE, "w") as fd:
    fd.write(tmp)

from lobster.version import LOBSTER_VERSION
print(LOBSTER_VERSION)

# Update last CHANGELOG entry and documentation to use the new
# version.

util.changelog.set_current_title(LOBSTER_VERSION)

# Commit & tag

os.system("git add CHANGELOG.md lobster-core/lobster/version.py")
os.system('git commit -m "LOBSTER Release %s"' % LOBSTER_VERSION)
