#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Tracability Evidence Report
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

import json
import os.path
from enum import Enum, auto

from lobster.report.errors import (Source_Reference,
                                   Message_Handler)


def open_lobster_file(mh, file_name):
    assert isinstance(mh, Message_Handler)
    assert isinstance(file_name, str)

    loc = Source_Reference(file_name = file_name)

    if not os.path.isfile(file_name):
        mh.error(loc, "is not a file")

    with open(file_name, "r") as fd:
        try:
            data = json.load(fd)
        except Exception as err:
            mh.error(loc, "does not contain JSON: %s" % str(err))

    if not isinstance(data, dict):
        mh.error(loc, "invalid data: top-level JSON item must be an object")

    if data.get("schema", None) not in ("lobster-req-trace",
                                        "lobster-imp-trace",
                                        "lobster-act-trace"):
        mh.error(loc,
                 "invalid data: schema %s is not supported" %
                 data.get("schema", "None"))
    else:
        schema = data["schema"].split("-", 2)[1]

    versions_supported = {
        "req" : set([1]),
        "imp" : set([1, 2]),
        "act" : set([1]),
    }

    version = data.get("version", None)
    if not isinstance(version, int):
        mh.error(loc,
                 "invalid data: version is not an integer")
    if version < 1:
        mh.error(loc,
                 "invalid data: version is less than 1")
    if version not in versions_supported[schema]:
        mh.error(loc,
                 "invalid data: version %u is not supported for %s,"
                 " only %s is supported"
                 % (version,
                    schema,
                    " or ".join(sorted(map(str, versions_supported[schema])))))

    if "data" not in data or \
       not isinstance(data["data"], dict):
        mh.error(loc,
                 "invalid data: no data object")

    if "generator" not in data or \
       not isinstance(data["generator"], str):
        mh.error(loc,
                 "invalid data: no generator string")

    return data


class Tracing_Status(Enum):
    OK        = auto()
    PARTIAL   = auto()
    MISSING   = auto()
    JUSTIFIED = auto()
    ERROR     = auto()


class Item:
    def __init__(self, name, source):
        assert isinstance(name, str)
        assert isinstance(source, Source_Reference)
        self.name           = name
        self.source         = source
        self.ref_up         = []
        self.ref_down       = []
        self.level          = None
        self.messages       = []
        self.tracing_status = None
        self.just_global    = []
        self.just_up        = []
        self.just_down      = []

    def trace_up(self, target):
        self.ref_up.append(target)

    def trace_down(self, target):
        self.ref_down.append(target)

    def set_level(self, level):
        assert isinstance(level, str)
        self.level = level

    def justify(self, reason):
        assert isinstance(reason, str)
        self.just_global.append(reason)

    def justify_up(self, reason):
        assert isinstance(reason, str)
        self.just_up.append(reason)

    def justify_down(self, reason):
        assert isinstance(reason, str)
        self.just_down.append(reason)

    def to_report_json(self):
        return {
            "name"             : self.name,
            "source"           : self.source.to_report_json(),
            "ref_up"           : self.ref_up,
            "ref_down"         : self.ref_down,
            "tracing_status"   : self.tracing_status.name,
            "tracing_messages" : self.messages,
            "just_global"      : self.just_global,
            "just_up"          : self.just_up,
            "just_down"        : self.just_down,
        }

    def resolve_status(self, config, stab):
        assert self.level in config
        level = config[self.level]

        has_up_ref    = len(self.ref_up) > 0
        has_down_ref  = len(self.ref_down) > 0
        has_just_up   = len(self.just_up) > 0 or len(self.just_global) > 0
        has_just_down = len(self.just_down) > 0 or len(self.just_global) > 0

        ok_up = True
        if level["needs_tracing_up"]:
            if not has_up_ref and not has_just_up:
                ok_up = False
                self.messages.append("missing up reference")

        ok_down = True
        if level["needs_tracing_down"]:
            has_trace = {name : False
                         for name in config
                         if self.level in config[name]["traces"]}
            for ref in self.ref_down:
                has_trace[stab[ref].level] = True
            for chain in level["breakdown_requirements"]:
                if not any(has_trace[src] for src in chain) and \
                   not has_just_down:
                    ok_down = False
                    self.messages.append("missing reference to %s" %
                                         " or ".join(sorted(chain)))

        if ok_up and ok_down:
            if has_just_up or has_just_down:
                self.tracing_status = Tracing_Status.JUSTIFIED
            else:
                self.tracing_status = Tracing_Status.OK
        elif (ok_up or ok_down) and \
             level["needs_tracing_up"] and \
             level["needs_tracing_down"]:
            self.tracing_status = Tracing_Status.PARTIAL
        else:
            self.tracing_status = Tracing_Status.MISSING


class Requirement_Item(Item):
    # Requirements or spec
    def __init__(self, name, source, kind, framework):
        super().__init__(name, source)
        assert isinstance(kind, str)
        assert isinstance(framework, str)
        self.kind      = kind
        self.framework = framework
        self.text      = None

    def set_text(self, text):
        assert isinstance(text, str)
        self.text = text.strip()

    def __repr__(self):
        return "Requirement_Item(%s, %s, %s)" % (self.name,
                                                 self.source,
                                                 self.kind)

    def to_report_json(self):
        rv = super().to_report_json()
        rv.update({
            "class"     : "requirement",
            "framework" : self.framework,
            "kind"      : self.kind,
            "text"      : self.text,
        })
        return rv

    @classmethod
    def parse(cls, mh, file_name):
        assert isinstance(mh, Message_Handler)
        assert os.path.isfile(file_name)
        assert file_name.endswith(".lobster")
        items = {}
        references = []
        data = open_lobster_file(mh, file_name)
        if data["schema"] not in ("lobster-req-trace",):
            mh.error(Source_Location(file_name = file_name),
                     "schema must be lobster-req-trace, found %s instead" %
                     data["schema"])

        try:
            for item_name, data in data["data"].items():
                items[item_name] = Requirement_Item(
                    name      = item_name,
                    source    = Source_Reference(json=data["source"]),
                    kind      = data["kind"],
                    framework = data["framework"])
                if "text" in data:
                    items[item_name].set_text(data["text"])
                for tag in data["tags"]:
                    references.append((item_name, tag))
        except Exception:
            mh.error(Source_Reference(file_name = file_name),
                     "malformed data")

        return items, references


class Implementation_Item(Item):
    # Code
    def __init__(self, name, source, kind, language):
        super().__init__(name, source)
        assert isinstance(kind, str)
        assert isinstance(language, str)
        self.kind     = kind
        self.language = language

    def __repr__(self):
        return "Implementation_Item(%s, %s, %s, %s)" % (self.name,
                                                        self.source,
                                                        self.kind,
                                                        self.language)

    def to_report_json(self):
        rv = super().to_report_json()
        rv.update({
            "class"    : "implementation",
            "kind"     : self.kind,
            "language" : self.language,
        })
        return rv

    @classmethod
    def parse(cls, mh, file_name):
        assert isinstance(mh, Message_Handler)
        assert os.path.isfile(file_name)
        assert file_name.endswith(".lobster")
        items = {}
        references = []
        data = open_lobster_file(mh, file_name)
        if data["schema"] not in ("lobster-imp-trace",):
            mh.error(Source_Location(file_name = file_name),
                     "schema must be lobster-impl-trace, found %s instead" %
                     data["schema"])

        try:
            for item_name, data in data["data"].items():
                items[item_name] = Implementation_Item(
                    name     = item_name,
                    source   = Source_Reference(json=data["source"]),
                    kind     = data["kind"],
                    language = data["language"])
                for tag in data["tags"]:
                    references.append((item_name, tag))
                if "justification" in data:
                    for reason in data["justification"]:
                        items[item_name].justify(reason)
                if "justification_up" in data:
                    for reason in data["justification_up"]:
                        items[item_name].justify_up(reason)
                if "justification_down" in data:
                    for reason in data["justification_down"]:
                        items[item_name].justify_down(reason)
        except Exception:
            mh.error(Source_Reference(file_name = file_name),
                     "malformed data")

        return items, references


class Activity_Item(Item):
    # Tests, proofs, and argumentation for correctness

    def __init__(self, name, source, kind, framework, status):
        super().__init__(name, source)
        assert isinstance(kind, str)
        assert isinstance(framework, str)
        assert status in ("ok", "fail", "not run", "unknown")
        self.kind        = kind
        self.framework   = framework
        self.test_status = status

    def __repr__(self):
        return "Activity_Item(%s, %s, %s, %s, %s)" % (self.name,
                                                      self.source,
                                                      self.kind,
                                                      self.framework,
                                                      self.test_status)

    def to_report_json(self):
        rv = super().to_report_json()
        rv.update({
            "class"       : "activity",
            "kind"        : self.kind,
            "framework"   : self.framework,
            "test_status" : self.test_status,
        })
        return rv

    @classmethod
    def parse(cls, mh, file_name):
        assert isinstance(mh, Message_Handler)
        assert os.path.isfile(file_name)
        assert file_name.endswith(".lobster")
        items = {}
        references = []

        data = open_lobster_file(mh, file_name)
        if data["schema"] not in ("lobster-act-trace",):
            mh.error(Source_Location(file_name = file_name),
                     "schema must be lobster-ver-trace, found %s instead" %
                     data["schema"])

        try:
            for item_name, data in data["data"].items():
                items[item_name] = Activity_Item(
                    name      = item_name,
                    source    = Source_Reference(json=data["source"]),
                    kind      = data["kind"],
                    framework = data["framework"],
                    status    = data.get("status", "ok"))
                for tag in data["tags"]:
                    references.append((item_name, tag))
        except Exception:
            mh.error(Source_Reference(file_name = file_name),
                     "malformed data")

        return items, references
