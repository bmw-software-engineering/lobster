#!/usr/bin/env python3
#
# lobster_ci_report - Visualise LOBSTER issues for CI
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

import sys
import os.path
import argparse

from lobster.report import Report
from lobster.items import Tracing_Status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lobster_report",
                    nargs="?",
                    default="report.lobster")
    options = ap.parse_args()

    if not os.path.isfile(options.lobster_report):
        if options.lobster_report == "report.lobster":
            ap.error("specify report file")
        else:
            ap.error("%s is not a file" % options.lobster_report)

    report = Report()
    report.load_report(options.lobster_report)

    for uid in sorted(report.items):
        item = report.items[uid]
        if item.tracing_status not in (Tracing_Status.OK,
                                       Tracing_Status.JUSTIFIED):
            for message in item.messages:
                report.mh.error(item.location,
                                message,
                                fatal = False)

    if report.mh.errors:
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
