#!/usr/bin/env python3
#
# lobster-trlc-system-test - Extract tracing tags for LOBSTER
# Copyright (C) 2023 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This component of TRLC program is free software: you can
# redistribute it and/or modify it under the terms of the GNU Affero
# General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.
# pylint: disable=invalid-name
import os
import sys
from lobster.items import Tracing_Tag, Activity
from lobster.location import File_Reference
from lobster.io import lobster_write
from trlc.trlc import Source_Manager
from trlc.errors import Message_Handler

tool_name = (sys.argv[1].split("/")[1] if "core/" in sys.argv[1]
    else sys.argv[1]).replace("_", "-")
TEST_DIR = f"tests-system/lobster-{tool_name}"
TARGET   = "system-tests.lobster"

def process(test_name_orig: str, mapping: dict):
    test_name = test_name_orig
    test_dir = os.path.join(TEST_DIR, test_name)
    assert os.path.isdir(test_dir)
    assert isinstance(mapping, dict)
    tag_file = os.path.join(test_dir, "tracing")

    items = []
    for test_case_dir_entry in os.scandir(test_dir):
        if not test_case_dir_entry.is_dir():
            continue
        test_name = test_name_orig + "." + test_case_dir_entry.name
        item = Activity(
            tag       = Tracing_Tag(namespace = "trlc-st",
                                    tag       = test_name),
            location  = File_Reference(filename = test_dir),
            framework = "TRLCST",
            kind      = "Test Directory")
        include_test = False
        if os.path.isfile(tag_file):
            include_test = True
            with open(tag_file, "r", encoding="UTF-8") as fd:
                tags = [Tracing_Tag(namespace = "req",
                                    tag       = line.strip())
                        for line in fd.read().splitlines()
                        if line.strip()]
            for tag in tags:
                item.add_tracing_target(tag)
        if test_name.startswith("rbt-"):
            include_test = True
            components = test_name[4:].lower().split("-")
            if len(components) >= 2:
                try:
                    int(components[-1])
                    components.pop()
                except ValueError:
                    pass
            requirement = mapping.get("-".join(components),
                                    "_".join(item.capitalize()
                                            for item in components))
            item.add_tracing_target(
                Tracing_Tag(namespace = "req",
                            tag       = f"{sys.argv[1]}_req.{requirement}"))
        if include_test:
            items.append(item)
    return items


def main():
    sm = Source_Manager(mh = Message_Handler(),
                        lint_mode   = False,
                        parse_trlc  = True,
                        verify_mode = False)
    sm.register_directory("lobster/tools/" + str(sys.argv[1]))
    sm.register_file("lobster/tools/requirements.rsl")
    stab = sm.process()
    pkg_req = stab.lookup_assuming(sm.mh, str(sys.argv[1]).replace("/","_") + "_req")
    mapping = {}
    for item in pkg_req.symbols.iter_record_objects():
        mapping[item.name.lower().replace("_", "-")] = item.name

    items = []
    for dir_entry in sorted(os.scandir(TEST_DIR),
                         key=lambda de: de.name):
        if dir_entry.is_dir():
            if dir_entry.name == "htmlcov":
                continue
            items += process(dir_entry.name, mapping)

    with open(TARGET, "w", encoding="UTF-8") as fd:
        lobster_write(fd, Activity, f"lobster-{str(sys.argv[1])}-system-test", items)

    print("Written %u items to %s" % (len(items), TARGET))
    return 0


if __name__ == "__main__":
    sys.exit(main())
