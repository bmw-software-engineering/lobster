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

from argparse import Namespace
import os

from lobster.exceptions import LOBSTER_Exception
from lobster.errors import LOBSTER_Error
from lobster.report import generate_report_file
from lobster.meta_data_tool_base import MetaDataToolBase


class ReportTool(MetaDataToolBase):
    def __init__(self):
        super().__init__(
            name="lobster-report",
            description="Generate a LOBSTER report from a lobster.conf file",
            official=True,
        )
        self._argument_parser.add_argument(
            "--lobster-config",
            metavar="FILE",
            default="lobster.conf",
        )
        self._argument_parser.add_argument(
            "--out",
            metavar="FILE",
            default="report.lobster",
        )

    def _run_impl(self, options: Namespace) -> int:

        if not os.path.isfile(options.lobster_config):
            raise LOBSTER_Exception(
                f"Cannot read config file '{options.lobster_config}'"
            )

        if os.path.exists(options.out) and not os.path.isfile(options.out):
            raise LOBSTER_Exception(
                f"Cannot write to '{options.out}': exists and is not a file"
            )

        try:
            generate_report_file(
                lobster_config=options.lobster_config,
                output_file=options.out
            )
        except LOBSTER_Error as err:
            raise LOBSTER_Exception(
                f"{self.name}: aborting due to earlier errors."
            ) from err
        except LOBSTER_Exception as err:
            err.dump()
            raise LOBSTER_Exception(
                f"{self.name}: aborting due to earlier errors. "
                "See additional data above."
            ) from err

        return 0


def main() -> int:
    return ReportTool().run()
