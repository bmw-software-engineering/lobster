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

import json
import subprocess
import sys


def update_json(filename, expected_location=None, out=None):
    # lobster-trace: system_test.Enrich_With_Hash
    # Load the JSON data from the file
    with open(filename, 'r') as file:
        data = json.load(file)

    commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

    # Traverse the JSON structure and update the 'loc' values
    for level in data['levels']:
        for item in level['items']:
            location = item['location']
            if 'file' in location:
                location['commit'] = commit
                if expected_location:
                    location['file'] = expected_location

    # Save the updated JSON data into the output file
    if not out:
        out = filename
    with open(out, 'w') as fd:
        json.dump(data, fd, indent=2)
        fd.write("\n")

    print(f"JSON data updated and saved to '{out}'.")


if __name__ == "__main__":
    update_json(sys.argv[1], out=sys.argv[2])
