#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2023-2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
import sys
from argparse import ArgumentParser

VERSION_TUPLE = (0, 13, 0)
VERSION_SUFFIX = ""

LOBSTER_VERSION = ("%u.%u.%u" % VERSION_TUPLE) + (
    "-%s" % VERSION_SUFFIX if VERSION_SUFFIX else ""
)

FULL_NAME = "LOBSTER %s" % LOBSTER_VERSION


def get_version(obj):
    """
    This decorator function is used on function wherever we are parsing
    the command line arguments which then adds a version argument to the function.
    If a version flag is passed to the command line arguments then the LOBSTER version
    is printed.
    Parameters
    ----------
    obj - obj can be an ArgumentParser object or a Function object.

    Returns - Nothing
    -------

    """
    if isinstance(obj, ArgumentParser):
        obj.add_argument("-v, --version", action="store_true",
                         default=None,
                         help="Get version for the tool")

        def version(func):
            def execution():
                if (len(sys.argv)  > 1 and
                        (sys.argv[1] == "--version" or sys.argv[1] == "-v")):
                    print(FULL_NAME)
                    return sys.exit(0)
                else:
                    return func()
            return execution
        return version
    else:
        def version(func):
            if not isinstance(obj, ArgumentParser):
                func.ap.add_argument("-v, --version", action="store_true",
                                     default=None,
                                     help="Get version for the tool")
                if (len(sys.argv)  > 1 and
                        (sys.argv[1] == "--version" or sys.argv[1] == "-v")):
                    print(FULL_NAME)
                    return sys.exit(0)
            return obj(func)
        return version
