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

import os
import json

"""This helper script can generate the test data for the
   test_extract_requirements_scenarios test case"""

folder = "tests_system/lobster_codebeamer/data"

for filename in os.listdir(folder):
    if filename.endswith(".lobster") and filename != "codebeamer.lobster":
        path = os.path.join(folder, filename)
        total_items = int(filename.split("_")[0])
        items = []
        for i in range(1, total_items + 1):
            items.append({
                "tag": f"req {i}@{i * 100}",
                "location": {
                    "kind": "codebeamer",
                    "cb_root": "https://localhost:MOCK_SERVER_PORT",
                    "tracker": i * 10000,
                    "item": i,
                    "version": i * 100,
                    "name": f"Requirement {i}: Dynamic name"
                },
                "name": f"Requirement {i}: Dynamic name",
                "messages": [],
                "just_up": [],
                "just_down": [],
                "just_global": [],
                "framework": "codebeamer",
                "kind": "codebeamer item",
                "text": None,
                "status": f"Status {i}"
            })

        file_content = {
            "data": items,
            "generator": "lobster_codebeamer",
            "schema": "lobster-req-trace",
            "version": 4,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(file_content, f, indent=2)
            f.write("\n")
        print(f"Wrote {filename}")
