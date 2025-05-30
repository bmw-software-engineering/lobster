#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2023-2024 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
import json
from collections import OrderedDict
from dataclasses import dataclass

from lobster.items import Tracing_Status, Requirement, Implementation, Activity
from lobster.config.parser import load as load_config
from lobster.errors import Message_Handler
from lobster.io import lobster_read
from lobster.location import File_Reference


@dataclass
class Coverage:
    level    : str
    items    : int
    ok       : int
    coverage : None


class Report:
    def __init__(self):
        self.mh       = Message_Handler()
        self.config   = OrderedDict()
        self.items    = {}
        self.coverage = {}
        self.custom_data = {}

    def parse_config(self, filename):
        """
        Function parses the lobster config file to generate a .lobster file.
        Parameters
        ----------
        filename - configuration file

        Returns - Nothing
        -------

        """
        assert isinstance(filename, str)
        assert os.path.isfile(filename)

        # Load config
        self.config = load_config(self.mh, filename)

        # Load requested files
        for level in self.config:
            for source in self.config[level]["source"]:
                lobster_read(self.mh, source["file"], level, self.items,
                             source)

        # Resolve references for items
        self.resolve_references_for_items()

        # Compute status and items count
        self.compute_item_count_and_status()

        # Compute coverage for items
        self.compute_coverage_for_items()

    def resolve_references_for_items(self):
        for src_item in self.items.values():
            while src_item.unresolved_references:
                dst_tag = src_item.unresolved_references.pop()
                if dst_tag.key() not in self.items:
                    src_item.error("unknown tracing target %s" % dst_tag.key())
                    continue
                dst_item = self.items[dst_tag.key()]
                # TODO: Check if policy allows this link
                src_item.ref_up.append(dst_tag)
                dst_item.ref_down.append(src_item.tag)

                # Check versions match, if specified
                if dst_tag.version is not None:
                    if dst_item.tag.version is None:
                        src_item.error("tracing destination %s is unversioned"
                                       % dst_tag.key())
                    elif dst_tag.version != dst_item.tag.version:
                        src_item.error("tracing destination %s has version %s"
                                       " (expected %s)" %
                                       (dst_tag.key(),
                                        dst_item.tag.version,
                                        dst_tag.version))

    def compute_coverage_for_items(self):
        for level_obj in self.coverage.values():
            if level_obj.items == 0:
                level_obj.coverage = 0.0
            else:
                level_obj.coverage = float(level_obj.ok * 100) / float(level_obj.items)

    def compute_item_count_and_status(self):
        for level in self.config:
            coverage = Coverage(level=level, items=0, ok=0, coverage=None)
            self.coverage.update({level: coverage})
        for item in self.items.values():
            item.determine_status(self.config, self.items)
            self.coverage[item.level].items += 1
            if item.tracing_status in (Tracing_Status.OK,
                                       Tracing_Status.JUSTIFIED):
                self.coverage[item.level].ok += 1

    def write_report(self, filename):
        assert isinstance(filename, str)

        levels = []
        for level_config in self.config.values():
            level = {
                "name"     : level_config["name"],
                "kind"     : level_config["kind"],
                "items"    : [item.to_json()
                              for item in self.items.values()
                              if item.level == level_config["name"]],
                "coverage" : self.coverage[level_config["name"]].coverage
            }
            levels.append(level)

        report = {
            "schema"    : "lobster-report",
            "version"   : 2,
            "generator" : "lobster_report",
            "levels"    : levels,
            "policy"    : self.config,
            "matrix"    : [],
        }

        with open(filename, "w", encoding="UTF-8") as fd:
            json.dump(report, fd, indent=2)
            fd.write("\n")

    def load_report(self, filename):
        assert isinstance(filename, str)

        loc = File_Reference(filename)

        # Read and validate JSON
        with open(filename, "r", encoding="UTF-8") as fd:
            try:
                data = json.load(fd)
            except json.decoder.JSONDecodeError as err:
                self.mh.error(File_Reference(filename,
                                             err.lineno,
                                             err.colno),
                              err.msg)

        # Validate basic structure
        self.validate_basic_structure_of_lobster_file(data, loc)

        # Validate indicated schema
        self.validate_indicated_schema(data, loc)

        # Validate and parse custom data
        self.validate_and_parse_custom_data(data, loc)

        # Read in data
        self.compute_items_and_coverage_for_items(data)

    def compute_items_and_coverage_for_items(self, data):
        """
        Function calculates items and coverage for the items
        Parameters
        ----------
        data - contents of lobster json file.

        Returns - Nothing
        -------

        """
        self.config = data["policy"]
        for level in data["levels"]:
            assert level["name"] in self.config
            coverage = Coverage(
                level=level["name"], items=0, ok=0, coverage=level["coverage"]
            )
            self.coverage.update({level["name"]: coverage})

            for item_data in level["items"]:
                if level["kind"] == "requirements":
                    item = Requirement.from_json(level["name"],
                                                 item_data,
                                                 3)
                elif level["kind"] == "implementation":
                    item = Implementation.from_json(level["name"],
                                                    item_data,
                                                    3)
                else:
                    assert level["kind"] == "activity"
                    item = Activity.from_json(level["name"],
                                              item_data,
                                              3)

                self.items[item.tag.key()] = item
                self.coverage[item.level].items += 1
                if item.tracing_status in (Tracing_Status.OK,
                                           Tracing_Status.JUSTIFIED):
                    self.coverage[item.level].ok += 1

    def validate_and_parse_custom_data(self, data, loc):
        """
        Function validates the optional 'custom_data' field in the lobster report.
        Ensures that if present, it is a dictionary with string keys and string values.

        Parameters
        ----------
        data - contents of lobster json file.
        loc  - location from where the error was raised.

        Returns - Nothing
        -------
        """
        self.custom_data = data.get('custom_data', None)
        if self.custom_data:
            if not isinstance(self.custom_data, dict):
                self.mh.error(loc, "'custom_data' must be an object (dictionary).")

            for key, value in self.custom_data.items():
                if not isinstance(key, str):
                    self.mh.error(loc,
                                  f"Key in 'custom_data' must be a "
                                  f"string, got {type(key).__name__}.")
                if not isinstance(value, str):
                    self.mh.error(loc,
                                  f"Value for key '{key}' in 'custom_data' "
                                  f"must be a string, got {type(value).__name__}.")

    def validate_indicated_schema(self, data, loc):
        """
        Function validates the schema and version.
        Parameters
        ----------
        data - contents of lobster json file.
        loc  - location from where the error was raised.

        Returns - Nothing
        -------

        """
        supported_schema = {
            "lobster-report": set([2]),
        }
        if data["schema"] not in supported_schema:
            self.mh.error(loc, "unknown schema kind %s" % data["schema"])
        if data["version"] not in supported_schema[data["schema"]]:
            self.mh.error(loc,
                          "version %u for schema %s is not supported" %
                          (data["version"], data["schema"]))

    def validate_basic_structure_of_lobster_file(self, data, loc):
        """
        Function validates the basic structure of lobster file. All the first level
        keys of the lobster json file are validated here.
        Parameters
        ----------
        data - contents of lobster json file.
        loc  - location from where the error was raised.

        Returns - Nothing
        -------

        """
        if not isinstance(data, dict):
            self.mh.error(loc, "parsed json is not an object")

        rkey_dict = {"schema": str, "version": int, "generator": str, "levels": list,
                     "policy": dict, "matrix": list}
        type_dict = {int: "an integer", str: "a string", list: "an array",
                     dict: "an object"}
        for rkey, rvalue in rkey_dict.items():
            if rkey not in data:
                self.mh.error(loc, "required top-levelkey %s not present" % rkey)
            if not isinstance(data[rkey], rvalue):
                self.mh.error(loc, "%s is not %s." % (rkey, type_dict[rvalue]))
