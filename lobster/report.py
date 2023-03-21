#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Tracability Evidence Report
# Copyright (C) 2023 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

from lobster.items import Tracing_Status, Requirement, Implementation, Activity
from lobster.config.parser import load as load_config
from lobster.errors import Message_Handler
from lobster.io import lobster_read
from lobster.location import File_Reference


class Report:
    def __init__(self):
        self.mh       = Message_Handler()
        self.config   = OrderedDict()
        self.items    = {}
        self.coverage = {}

    def parse_config(self, filename):
        assert isinstance(filename, str)
        assert os.path.isfile(filename)

        # Load config
        self.config = load_config(self.mh, filename)

        # Load requested files
        for level in self.config:
            for source in self.config[level]["source"]:
                lobster_read(self.mh, source["file"], level, self.items,
                             source)

        # Resolve references
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

        # Compute status and coverage for items
        self.coverage = {level: {"items"    : 0,
                                 "ok"       : 0,
                                 "coverage" : None}
                         for level in self.config}
        for item in self.items.values():
            item.determine_status(self.config, self.items)
            self.coverage[item.level]["items"] += 1
            if item.tracing_status in (Tracing_Status.OK,
                                       Tracing_Status.JUSTIFIED):
                self.coverage[item.level]["ok"] += 1

        # Compute coverage for levels
        for data in self.coverage.values():
            if data["ok"] == data["items"]:
                data["coverage"] = 100.0
            else:
                data["coverage"] = \
                    float(data["ok"] * 100) / float(data["items"])

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
                "coverage" : self.coverage[level_config["name"]]["coverage"]
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
        if not isinstance(data, dict):
            self.mh.error(loc, "parsed json is not an object")

        for rkey in ("schema", "version", "generator",
                     "levels", "policy", "matrix"):
            if rkey not in data:
                self.mh.error(loc,
                              "required top-levelkey %s not present" % rkey)
            if rkey in ("levels", "matrix"):
                if not isinstance(data[rkey], list):
                    self.mh.error(loc, "%s is not an array" % rkey)
            elif rkey == "policy":
                if not isinstance(data[rkey], dict):
                    self.mh.error(loc, "policy is not an object")
            elif rkey == "version":
                if not isinstance(data[rkey], int):
                    self.mh.error(loc, "version is not an integer")
            else:
                if not isinstance(data[rkey], str):
                    self.mh.error(loc, "%s is not a string" % rkey)

        # Validate indicated schema
        supported_schema = {
            "lobster-report" : set([2]),
        }
        if data["schema"] not in supported_schema:
            self.mh.error(loc, "unknown schema kind %s" % data["schema"])
        if data["version"] not in supported_schema[data["schema"]]:
            self.mh.error(loc,
                          "version %u for schema %s is not supported" %
                          (data["version"], data["schema"]))

        # Read in data
        self.config = data["policy"]
        for level in data["levels"]:
            assert level["name"] in self.config
            self.coverage[level["name"]] = {
                "items"    : 0,
                "ok"       : 0,
                "coverage" : level["coverage"]
            }
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
                self.coverage[item.level]["items"] += 1
                if item.tracing_status in (Tracing_Status.OK,
                                           Tracing_Status.JUSTIFIED):
                    self.coverage[item.level]["ok"] += 1
