#!/usr/bin/env python3
#
# lobster_pkg - Extract tracing values from xml file for LOBSTER
# Copyright (C) 2024-2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
import os.path
from pathlib import Path
import xml.etree.ElementTree as ET
import json
import re
from typing import Dict, List
from xml.dom import minidom
from argparse import Namespace

from lobster.common.exceptions import LOBSTER_Exception
from lobster.common.io import lobster_write
from lobster.common.items import Activity, Tracing_Tag
from lobster.common.location import File_Reference
from lobster.common.meta_data_tool_base import MetaDataToolBase

NS = {
    "ecu": "http://www.tracetronic.de/xml/ecu-test",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}
TSBLOCK = "TsBlock"


def get_valid_files(
    file_dir: List[str]
) -> List[str]:
    file_list = []
    for item in file_dir:
        if os.path.isfile(item):
            file_list.append(item)
        elif os.path.isdir(item):
            for path, _, files in os.walk(item):
                for filename in files:
                    _, ext = os.path.splitext(filename)
                    if ext in (".pkg", ".ta"):
                        file_list.append(os.path.join(path, filename))
        else:
            raise FileNotFoundError("%s is not a file or directory" % item)
    return file_list


def write_to_file(options: Namespace, data: Dict[str, Activity]) -> None:
    with open(options.out, "w", encoding="UTF-8") as file:
        lobster_write(file, Activity, "lobster-pkg", data.values())
        print("Written output for %u items to %s" % (len(data), options.out))


def create_raw_entry(
    data: Dict[str, Activity], file_name: str, trace_list: list
) -> None:

    activity_list = json.loads(trace_list)
    # Collect all traces marked as "first"
    traces = []
    for item in activity_list:
        if item.get("activity") == "first":
            trace_parts = [s.strip() for s in re.split(r"[:,]", item.get("trace"))]
            traces.extend(trace_parts[1:])  # skip the "lobster-trace" prefix

    tag = Tracing_Tag("pkg", f"{file_name}")
    loc = File_Reference(file_name)
    data[tag.key()] = Activity(
        tag=tag, location=loc, framework="lobster-pkg", kind="test"
    )
    for trace_value in traces:
        data[tag.key()].add_tracing_target(Tracing_Tag("req", trace_value))

    # Handle other activities (if any)
    for item in activity_list:
        if item.get("activity") != "first":
            trace2 = [s.strip() for s in re.split(r"[:,]", item.get("trace"))]
            action = item.get("action")
            line = item.get("line")
            tag = Tracing_Tag("pkg", f"{file_name}::{action}::{line}")
            loc = File_Reference(file_name, int(item.get("line")))
            data[tag.key()] = Activity(
                tag=tag, location=loc, framework="lobster-pkg", kind="test"
            )
            for trace_value in trace2[1:]:
                data[tag.key()].add_tracing_target(Tracing_Tag("req", trace_value))


def create_default_activity(file_content, file_name: str,
                            data: Dict[str, Activity]) -> None:
    # Only create a default Activity entry for packages with
    # the TESTCASE tag
    # Check for TESTCASE tag in INFORMATION/TAGS
    tree = ET.fromstring(file_content)
    info = tree.find(".//ecu:INFORMATION", NS)
    is_testcase = False
    if info is not None:
        tags = info.find(
            ".//ecu:TAGS", NS
        )
        if tags is not None:
            for tag in tags.findall(
                ".//ecu:TAG", NS
            ):
                if (tag.text or "").strip().upper() == "TESTCASE":
                    is_testcase = True
                    break
    if is_testcase:
        tag = Tracing_Tag("pkg", f"{file_name}")
        loc = File_Reference(file_name)
        data[tag.key()] = Activity(
            tag=tag,
            location=loc,
            framework="lobster-pkg",
            kind="test",
        )


def xml_parser(file_content, filename):
    activity_list = []
    misplaced_lobster_lines = []
    tree = ET.fromstring(file_content)

    info = tree.find(".//ecu:INFORMATION", NS)
    is_testcase = False
    if info is not None:
        tags = info.find(".//ecu:TAGS", NS)
        if tags is not None:
            for tag in tags.findall(".//ecu:TAG", NS):
                if (tag.text or "").strip().upper() == "TESTCASE":
                    is_testcase = True
                    break
    if not is_testcase:
        return activity_list

    tag_teststep = f"{{{NS['ecu']}}}TESTSTEP"
    tag_value = f"{{{NS['ecu']}}}VALUE"

    # Find the parent TESTSTEPS element
    teststeps_parent = tree.find(
        ".//ecu:TESTSTEPS", NS
    )
    if teststeps_parent is None:
        return activity_list

    # Find the first relevant TsBlock (first level under TESTSTEPS)
    first_level_tsblocks = [
        elem
        for elem in teststeps_parent
        if elem.tag == tag_teststep and elem.attrib.get("name") == TSBLOCK
    ]
    if not first_level_tsblocks:
        return activity_list

    # The first TsBlock determines the allowed parent level
    allowed_parent = first_level_tsblocks[0]

    # Collect all TsBlocks that are direct children of the allowed parent
    # (i.e., one level deeper)
    allowed_tsblocks = [
        elem
        for elem in allowed_parent
        if elem.tag == tag_teststep and elem.attrib.get("name") == TSBLOCK
    ]

    # Also allow the first TsBlock itself
    allowed_tsblocks_set = set(allowed_tsblocks)
    allowed_tsblocks_set.add(allowed_parent)

    # Traverse all TsBlocks in the document
    for tsblock in tree.iter(tag_teststep):
        if tsblock.attrib.get("name") != TSBLOCK:
            continue

        # Check if this TsBlock is allowed
        # (first TsBlock or direct child of first TsBlock)
        is_allowed = False
        if tsblock is allowed_parent:
            is_allowed = True
        else:
            # xml.etree.ElementTree does not support getparent,
            # so we check by structure:
            # Is tsblock a direct child of allowed_parent?
            for child in allowed_parent:
                if child is tsblock:
                    is_allowed = True
                    break

        obj_value = tsblock.findall(".//" + tag_value)
        for trace_search in obj_value:
            if "lobster-trace:" in (trace_search.text or ""):
                if is_allowed:
                    # Allowed: add to activity_list
                    activity_obj = {"trace": trace_search.text, "activity": "first"}
                    activity_list.append(activity_obj)
                else:
                    # Misplaced: not at allowed nesting
                    search_string = trace_search.text
                    dom_tree = minidom.parseString(file_content)
                    xml_content = dom_tree.toxml()
                    start_index = xml_content.find(search_string)
                    line_number = xml_content.count("\n", 0, start_index) + 2
                    misplaced_lobster_lines.append(line_number)

        if misplaced_lobster_lines:
            raise LOBSTER_Exception(
                f"Misplaced LOBSTER tag(s) in file {filename}"
                f" at line(s): {misplaced_lobster_lines}"
            )

    return activity_list


def extract_lobster_traces_from_trace_analysis(tree, filename):
    """
    Extracts lobster traces from DESCRIPTION fields that are direct
    children of ANALYSISITEMs of type 'episode' which are themselves
    direct children of TRACE-ANALYSIS blocks.

    - A valid lobster-trace is only allowed in a DESCRIPTION element
    that is a direct child of an ANALYSISITEM with xsi:type="episode",
    which itself is a direct child of TRACE-ANALYSIS.
    - Any lobster-trace found in a DESCRIPTION elsewhere under
    TRACE-ANALYSIS (e.g., in nested ANALYSISITEMs or other locations)
    is considered misplaced and will generate a warning.

    Returns:
        tuple: (list of valid trace dicts, list of misplaced trace warning strings)
    """

    valid_traces = []
    misplaced_traces = []

    # Collect all valid DESCRIPTIONs (direct child of top-level episode)
    valid_descs = set()
    for trace_analysis in tree.findall(".//ecu:TRACE-ANALYSIS", NS):
        # Only consider ANALYSISITEMs of type 'episode' that are direct
        # children of TRACE-ANALYSIS
        for episode in trace_analysis.findall("ecu:ANALYSISITEM", NS):
            if (
                episode.attrib.get(f"{{{NS['xsi']}}}type") == "episode"
            ):
                # Only DESCRIPTION elements that are direct children of this episode
                for child in episode:
                    if (
                        child.tag == f"{{{NS['ecu']}}}DESCRIPTION" and
                        child.text and
                        "lobster-trace:" in child.text
                    ):
                        valid_traces.append(
                            {
                                "trace": child.text.strip(),
                                "activity": "first",
                                "name": episode.findtext(
                                    "ecu:NAME", default="", namespaces=NS
                                ),
                                "description": child.text.strip(),
                                "source": filename,
                            }
                        )
                        valid_descs.add(child)

        # Now check for misplaced traces: any DESCRIPTION with lobster-trace
        # under TRACE-ANALYSIS
        for desc in trace_analysis.findall(".//ecu:DESCRIPTION", NS):
            if desc.text and "lobster-trace:" in desc.text and desc not in valid_descs:
                msg = "WARNING: misplaced lobster-trace in " \
                      f"{filename}: {desc.text.strip()}"
                if msg not in misplaced_traces:
                    misplaced_traces.append(msg)

    return valid_traces, misplaced_traces


def lobster_pkg(options):
    """
    The main function to parse tracing information from .pkg files for LOBSTER.

    This function processes the input files or directories specified in 'options.files',
    extracts tracing tags and activities from XML content (including both standard and
    TRACE-ANALYSIS blocks), and writes the results to an output file

    Parameters
    ----------
        options (Namespace): Parsed command-line arguments with at least:
            - files: list of file or directory paths to process
            - out: output file path (optional; if not set, output is report.lobster)
    """
    file_list = get_valid_files(options.files)
    data = {}

    for file_path in file_list:
        filename = Path(file_path).name
        with open(file_path, "r", encoding="UTF-8") as file:
            try:
                file_content = file.read()

                tree = ET.fromstring(file_content)

                getvalues = xml_parser(file_content, filename)

                # Also extract from TRACE-ANALYSIS blocks
                valid_traces, misplaced_traces = (
                    extract_lobster_traces_from_trace_analysis(
                        tree, filename
                    )
                )
                getvalues.extend(valid_traces)
                for msg in misplaced_traces:
                    print(msg)

                if getvalues:
                    create_raw_entry(data, file.name, json.dumps(getvalues))
                else:
                    create_default_activity(file_content, filename, data)

            except ET.ParseError as err:
                print(f"Error parsing XML file '{filename}' : {err}")
                raise
            except LOBSTER_Exception as err:
                err.dump()
                raise

    # Set default output file if not specified
    output_file = getattr(options, "out", None)
    if not output_file:
        options.out = "report.lobster"

    write_to_file(options, data)

    return 0


class PkgTool(MetaDataToolBase):
    def __init__(self):
        super().__init__(
            name="pkg",
            description="Extract tracing tags from pkg files for LOBSTER",
            official=True,
        )
        self._argument_parser.add_argument(
            "files",
            nargs="+",
            metavar="FILE|DIR",
            help="Path to pkg file or directory.",
        )
        self._argument_parser.add_argument(
            "--out",
            default="report.lobster",
            help="write output to this file; otherwise output is report.lobster",
        )

    def _run_impl(self, options: Namespace) -> int:
        options = self._argument_parser.parse_args()

        try:
            lobster_pkg(options)

        except ValueError as exception:
            self._argument_parser.error(str(exception))

        return 0


def main() -> int:
    return PkgTool().run()
