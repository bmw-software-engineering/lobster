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

import os
import sys
import xml.etree.ElementTree as ET
from argparse import Namespace
from typing import Dict, List, Optional, Sequence, Set, Tuple, Type

from lobster.common.io import ensure_output_directory, lobster_write
from lobster.common.items import Activity
from lobster.common.meta_data_tool_base import MetaDataToolBase
from lobster.common.test_report.testreportreader import TestReportReader


class TestReportTool(MetaDataToolBase):
    """Command line tool which converts XML test reports into LOBSTER activities.

    The tool collects the reports given as files or found in directories, and
    reads each report with the first of its readers that accepts it. Reports which
    no reader accepts are skipped.
    """

    def __init__(
        self,
        name: str,
        description: str,
        readers: Sequence[Type[TestReportReader]],
        generator: str,
    ) -> None:
        """Constructor

        :param name: name of the tool, without the 'lobster-' prefix
        :param description: description of the tool, used in the help message
        :param readers: readers of the supported report dialects, in the order in
            which they are tried
        :param generator: name of the generator written to the output file
        """
        super().__init__(name=name, description=description, official=True)
        self._readers = list(readers)
        self._generator = generator
        self._argument_parser.add_argument(
            "files",
            nargs="+",
            metavar="FILE|DIR",
        )
        self._argument_parser.add_argument("--out", default=None)
        self._argument_parser.add_argument(
            "--derive-gwt-from-test-name",
            action="store_true",
            help="derive the Given, When and Then parts of the item text "
            "from the test name, unless the test records one of them "
            "itself",
        )

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
        c_files_rel: Dict[str, Set[str]],
        file_list: List[str],
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

    def _collect_input_files(
        self, options: Namespace
    ) -> Tuple[Dict[str, Set[str]], Set[str]]:
        c_files_rel: Dict[str, Set[str]] = {}
        file_list: List[str] = []
        for item in options.files:
            if os.path.isfile(item):
                file_list.append(item)
                continue
            if os.path.isdir(item):
                self._collect_directory_files(item, c_files_rel, file_list)
                continue
            self._argument_parser.error(f"{item} is not a file or directory")

        return c_files_rel, {os.path.realpath(os.path.abspath(f)) for f in file_list}

    def _select_reader(self, root: ET.Element) -> Optional[Type[TestReportReader]]:
        for reader in self._readers:
            if reader.accepts(root):
                return reader
        return None

    def _run_impl(self, options: Namespace) -> int:
        c_files_rel, file_list = self._collect_input_files(options)

        items: List[Activity] = []
        for filename in file_list:
            root = ET.parse(filename).getroot()
            reader = self._select_reader(root)
            if reader is None:
                continue
            items += reader(options.derive_gwt_from_test_name, c_files_rel).read(root)

        if options.out:
            ensure_output_directory(options.out)
            with open(options.out, "w", encoding="UTF-8") as fd:
                lobster_write(fd, Activity, self._generator, items)
            print(f"Written output for {len(items)} items to {options.out}")
        else:
            lobster_write(sys.stdout, Activity, self._generator, items)
            print()

        return 0
