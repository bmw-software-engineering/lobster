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

import re
from pathlib import Path
from lobster.tools.core.html_report.html_report import get_commit_timestamp_utc


def update_html_output_file(filename: Path, working_dir: Path) -> None:
    """Update timestamp in LOBSTER HTML file with git commit timestamp."""
    if not filename.exists():
        raise FileNotFoundError(f"HTML file not found: {filename}")
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()
    git_timestamp = get_commit_timestamp_utc("HEAD", str(working_dir))
    updated_content = re.sub(
        r'Timestamp:\s*[^<]+',
        f'Timestamp: {git_timestamp}',
        html_content
    )
    if updated_content != html_content:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(updated_content)
