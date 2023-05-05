#!/usr/bin/env python3
#
# lobster_gtest - Extract GoogleTest tracing tags for LOBSTER
# Copyright (C) 2022 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
import argparse
import os.path
import xml.etree.ElementTree as ET

from lobster.items import Tracing_Tag, Activity
from lobster.location import File_Reference
from lobster.io import lobster_write


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files",
                    nargs="+",
                    metavar="FILE|DIR")
    ap.add_argument("--out", default=None)

    options = ap.parse_args()

    c_files_rel = {}
    file_list = []
    for item in options.files:
        if os.path.isfile(item):
            file_list.append(item)
        elif os.path.isdir(item):
            for path, _, files in os.walk(item, followlinks=True):
                for filename in files:
                    if not os.path.isfile(os.path.join(path, filename)):
                        continue
                    _, ext = os.path.splitext(filename)
                    if ext in (".xml", ):
                        file_list.append(os.path.join(path, filename))
                    elif ext in (".cpp", ".cc", ".c"):
                        fullname = os.path.relpath(
                            os.path.realpath(os.path.join(path, filename)))
                        if ".cache" in fullname:
                            continue
                        if filename not in c_files_rel:
                            c_files_rel[filename] = set()
                        c_files_rel[filename].add(fullname)

        else:
            ap.error("%s is not a file or directory" % item)

    file_list = {os.path.realpath(os.path.abspath(f))
                 for f in file_list}

    items = []

    for filename in file_list:
        tree = ET.parse(filename)
        root = tree.getroot()
        if root.tag != "testsuites":
            continue
        for suite in root:
            assert suite.tag == "testsuite"
            suite_name = suite.attrib["name"]
            for testcase in suite:
                assert testcase.tag == "testcase"
                test_name     = testcase.attrib["name"]
                test_executed = testcase.attrib["status"] == "run"
                test_ok       = True
                test_tags     = []
                source_file   = testcase.attrib["file"]
                source_line   = int(testcase.attrib["line"])
                for props in testcase:
                    if props.tag == "failure":
                        test_ok = False
                    elif props.tag == "properties":
                        for prop in props:
                            assert prop.tag == "property"
                            if prop.attrib["name"] == "lobster-tracing":
                                test_tags += [
                                    x.strip()
                                    for x in prop.attrib["value"].split(",")]
                            elif prop.attrib["name"] == "lobster-tracing-file":
                                source_file = prop.attrib["value"]
                            elif prop.attrib["name"] == "lobster-tracing-line":
                                source_line = int(prop.attrib["value"])

                if source_file in c_files_rel and \
                   len(c_files_rel[source_file]) == 1:
                    test_source = File_Reference(
                        filename = list(c_files_rel[source_file])[0],
                        line     = source_line)
                else:
                    test_source = File_Reference(
                        filename = source_file,
                        line     = source_line)

                uid = "%s:%s" % (suite_name, test_name)
                if test_executed:
                    if test_ok:
                        status = "ok"
                    else:
                        status = "fail"
                else:
                    status = "not run"

                tag  = Tracing_Tag("gtest", uid)
                item = Activity(tag       = tag,
                                location  = test_source,
                                framework = "GoogleTest",
                                kind      = "test",
                                status    = status)
                for ref in test_tags:
                    item.add_tracing_target(Tracing_Tag("req", ref))

                items.append(item)

    if options.out:
        with open(options.out, "w", encoding="UTF-8") as fd:
            lobster_write(fd, Activity, "lobster_gtest", items)
        print("Written output for %u items to %s" % (len(items),
                                                     options.out))
    else:
        lobster_write(fd, Activity, "lobster_gtest", items)
        print()


if __name__ == "__main__":
    sys.exit(main())
