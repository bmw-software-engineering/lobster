# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025-2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

from collections import defaultdict
from pathlib import Path


class FileTagGenerator:
    def __init__(self):
        self._basenames_to_lookup = defaultdict(dict)

    def get_tag(self, file_name: str) -> str:
        """Generates a unique tag for the given file based on its basename.
           The tag is in the format 'basename:index', where index is the
           number of times the basename has been encountered so far.
        """
        basename = Path(file_name).name
        lookup = self._basenames_to_lookup[basename]
        return lookup.setdefault(file_name, f"{basename}:{len(lookup) + 1}")
