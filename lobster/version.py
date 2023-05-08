#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Tracability Evidence Report
# Copyright (C) 2023 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

VERSION_TUPLE = (0, 9, 2)
VERSION_SUFFIX = ""

LOBSTER_VERSION = ("%u.%u.%u" % VERSION_TUPLE) + \
    ("-%s" % VERSION_SUFFIX if VERSION_SUFFIX else "")

FULL_NAME = "LOBSTER %s" % LOBSTER_VERSION
