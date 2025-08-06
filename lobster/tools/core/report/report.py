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
import sys

from lobster.exceptions import LOBSTER_Exception
from lobster.errors import LOBSTER_Error
from lobster.meta_data_tool_base import MetaDataToolBase
from lobster.report import Report


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

        report = Report()

        try:
            report.parse_config(options.lobster_config)
        except FileNotFoundError as e:
            print(f"{e}")
        except TypeError as e:
            print(f"{e}")
        except LOBSTER_Error as e:
            raise LOBSTER_Exception(
                f"{self.name}: aborting due to earlier errors."
            ) from e
        except LOBSTER_Exception as err:
            err.dump()
            raise

        report.write_report(options.out)
        return 0


def generate_report_file(lobster_config_file: str, output_file: str) -> dict:
    # This is an API function to run the lobster report tool
    report = Report()
    report.parse_config(lobster_config_file)
    report.write_report(output_file)


def main() -> int:
    return ReportTool().run()


if __name__ == "__main__":
    sys.exit(main())
