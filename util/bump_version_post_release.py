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

import util.changelog

from lobster.common.version import VERSION_TUPLE

major, minor, release = VERSION_TUPLE
release += 1

# Bump version and update version.py

VERSION_FILE = os.path.join("lobster", "version.py")

# pylint: disable=invalid-name
tmp = ""
with open(VERSION_FILE, "r", encoding="UTF-8") as fd:
    for raw_line in fd:
        if raw_line.startswith("VERSION_TUPLE"):
            raw_line = 'VERSION_TUPLE = (%u, %u, %u)\n' % (major,
                                                           minor,
                                                           release)
        elif raw_line.startswith("VERSION_SUFFIX"):
            raw_line = 'VERSION_SUFFIX = "dev"\n'

        tmp += raw_line
with open(VERSION_FILE, "w", encoding="UTF-8") as fd:
    fd.write(tmp)

LOBSTER_VERSION = "%u.%u.%u-dev" % (major, minor, release)

# Update changelog and docs, adding a new entry

util.changelog.add_new_section(LOBSTER_VERSION)

# Assemble commit

os.system("git add CHANGELOG.md lobster/version.py ")
os.system('git commit -m "Bump version to %s after release"' % LOBSTER_VERSION)
