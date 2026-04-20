#!/usr/bin/env python3
#
# lobster_gtest - Extract GoogleTest tracing tags for LOBSTER
# Copyright (C) 2022-2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
import os
from typing import Optional, Sequence
import xml.etree.ElementTree as ET

from lobster.common.items import Tracing_Tag, Activity
from lobster.common.location import Void_Reference, File_Reference
from lobster.common.io import lobster_write, ensure_output_directory
from lobster.common.meta_data_tool_base import MetaDataToolBase


class GtestTool(MetaDataToolBase):
    def __init__(self):
        super().__init__(
            name = "gtest",
            description = "Extract tracing tags from GoogleTest XML output",
            official = True,
        )
        self._argument_parser.add_argument(
            "files",
            nargs="+",
            metavar="FILE|DIR",
        )
        self._argument_parser.add_argument("--out", default=None)

    @staticmethod
    def _is_xml_file(filename: str) -> bool:
        return os.path.splitext(filename)[1] == ".xml"

    @staticmethod
    def _is_c_file(filename: str) -> bool:
        return os.path.splitext(filename)[1] in (".cpp", ".cc", ".c")

    @classmethod
    def _collect_directory_files(
            cls,
            item: str,
            c_files_rel,
            file_list,
    ) -> None:
        for path, _, files in os.walk(item, followlinks=True):
            for filename in files:
                full_path = os.path.join(path, filename)
                if not os.path.isfile(full_path):
                    continue
                if cls._is_xml_file(filename):
                    file_list.append(full_path)
                    continue
                if not cls._is_c_file(filename):
                    continue
                fullname = os.path.relpath(os.path.realpath(full_path))
                if ".cache" in str(fullname):
                    continue
                if filename not in c_files_rel:
                    c_files_rel[filename] = set()
                c_files_rel[filename].add(fullname)

    def _collect_input_files(self, options: Namespace):
        c_files_rel = {}
        file_list = []
        for item in options.files:
            if os.path.isfile(item):
                file_list.append(item)
                continue
            if os.path.isdir(item):
                self._collect_directory_files(item, c_files_rel, file_list)
                continue
            self._argument_parser.error(f"{item} is not a file or directory")

        file_list = {os.path.realpath(os.path.abspath(f)) for f in file_list}
        return c_files_rel, file_list

    @staticmethod
    def _parse_testcase_properties(testcase):
        test_ok = True
        test_tags = []
        source_file = testcase.attrib.get("file", None)
        source_line = int(testcase.attrib["line"]) \
            if "line" in testcase.attrib \
            else None

        for props in testcase:
            if props.tag == "failure":
                test_ok = False
                continue
            if props.tag != "properties":
                continue
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

        return test_ok, test_tags, source_file, source_line

    @staticmethod
    def _resolve_test_source(c_files_rel, source_file, source_line):
        if source_file in c_files_rel and len(c_files_rel[source_file]) == 1:
            return File_Reference(
                filename = list(c_files_rel[source_file])[0],
                line     = source_line)
        if source_file is None:
            return Void_Reference()
        return File_Reference(
            filename = source_file,
            line     = source_line)

    @staticmethod
    def _resolve_test_status(test_executed: bool, test_ok: bool) -> str:
        if not test_executed:
            return "not run"
        if test_ok:
            return "ok"
        return "fail"

    def _run_impl(self, options: Namespace) -> int:
        c_files_rel, file_list = self._collect_input_files(options)

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
                    if testcase.tag != "testcase":
                        continue
                    test_name     = testcase.attrib["name"]
                    test_executed = testcase.attrib["status"] == "run"
                    test_ok, test_tags, source_file, source_line = \
                        self._parse_testcase_properties(testcase)

                    test_source = self._resolve_test_source(
                        c_files_rel, source_file, source_line)

                    uid = f"{suite_name}:{test_name}"
                    status = self._resolve_test_status(test_executed, test_ok)

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
            ensure_output_directory(options.out)
            with open(options.out, "w", encoding="UTF-8") as fd:
                lobster_write(fd, Activity, "lobster_gtest", items)
            print(f"Written output for {len(items)} items to {options.out}")
        else:
            lobster_write(sys.stdout, Activity, "lobster_gtest", items)
            print()

        return 0


def main(args: Optional[Sequence[str]] = None) -> int:
    return GtestTool().run(args)
