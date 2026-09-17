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

"""
Script to update LOBSTER version in a generated RST report file.

Mirrors the pattern used by update_version_in_html.py for HTML reports.
"""

import re

from lobster.common.version import LOBSTER_VERSION


def update_version_in_rst_file(file_path) -> bool:
    """Update the LOBSTER version line in a golden RST file.

    The generated RST header contains a line of the form::

        | LOBSTER Version: X.Y.Z

    This function replaces the version token with the currently installed
    LOBSTER version so that the golden file matches actual tool output
    regardless of which release is under test.

    Args:
        file_path: Path to the RST file to update (str or :class:`pathlib.Path`).

    Returns:
        ``True`` if the version line was found and updated, ``False`` otherwise.
    """
    with open(file_path, "r", encoding="utf-8") as fh:
        content = fh.read()

    version_pattern = r"\| LOBSTER Version: [^\n]+"

    if not re.search(version_pattern, content):
        print(f"LOBSTER version line not found in {file_path}")
        return False

    updated_content = re.sub(
        r"(\| LOBSTER Version: )[^\n]+",
        rf"\g<1>{LOBSTER_VERSION}",
        content,
    )

    with open(file_path, "w", encoding="utf-8") as fh:
        fh.write(updated_content)

    print(
        f"Updated LOBSTER version to {LOBSTER_VERSION} in {file_path}"
    )
    return True
