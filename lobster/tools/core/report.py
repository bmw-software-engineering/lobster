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

import os
import sys
import argparse

from lobster.exceptions import LOBSTER_Exception
from lobster.errors import LOBSTER_Error
from lobster.report import Report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lobster-config",
                    metavar="FILE",
                    default="lobster.conf")

    options = ap.parse_args()

    if not os.path.isfile(options.lobster_config):
        print("error: cannot read config file '%s'" % options.lobster_config)
        return 0

    report = Report()

    try:
        report.parse_config(options.lobster_config)
    except LOBSTER_Error:
        print("lobster: aborting due to earlier errors.")
        return 1
    except LOBSTER_Exception as err:
        print("lobster: aborting due to earlier errors.")
        print("lobster: Additional data for debugging:")
        err.dump()
        return 1

    report.write_report("report.lobster")
    return 0


if __name__ == "__main__":
    sys.exit(main())
