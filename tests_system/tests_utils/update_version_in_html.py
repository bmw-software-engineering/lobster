# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
Script to update LOBSTER version in HTML footer
"""

import re
import sys

from lobster.common.version import LOBSTER_VERSION


def update_version_in_html_file(file_path):
    """
    Update the LOBSTER version in the HTML footer if present

    Args:
        file_path (str): Path to the HTML file
        new_version (str): New version string to replace

    Returns:
        bool: True if version was found and updated, False otherwise
    """

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the pattern to match <p>LOBSTER Version: any_version</p>
    version_pattern = r'<p>LOBSTER Version: [^<]+</p>'

    # Check if the version tag is present
    if not re.search(version_pattern, content, re.IGNORECASE):
        print(f"LOBSTER version tag not found in {file_path}")
        return False

    print(f"Found LOBSTER version tag in {file_path}")

    # Replace the version in the <p> tag
    updated_content = re.sub(
        r'(<p>LOBSTER Version: )[^<]+</p>',
        rf'\g<1>{LOBSTER_VERSION}</p>',
        content,
        flags=re.IGNORECASE
    )

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Successfully updated LOBSTER version to {LOBSTER_VERSION} in {file_path}")
    return True


if __name__ == "__main__":
    update_version_in_html_file(sys.argv[1])
