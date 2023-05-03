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

from enum import Enum, auto
from abc import ABCMeta
from hashlib import sha1

from lobster.location import Location


class Tracing_Tag:
    def __init__(self, namespace, tag, version=None):
        assert isinstance(namespace, str) and " " not in namespace
        assert isinstance(tag, str) and " " not in tag
        assert version is None or isinstance(version, (str, int))
        assert not isinstance(version, str) or version != "None"

        self.namespace = namespace
        self.tag       = tag
        self.version   = version
        self.hash_val  = None

    def __str__(self):
        rv = "%s %s" % (self.namespace,
                        self.tag)
        if self.version:
            rv += "@%s" % str(self.version)
        return rv

    def key(self):
        return self.namespace + " " + self.tag

    def to_json(self):
        return str(self)

    @classmethod
    def from_json(cls, json):
        assert isinstance(json, str)
        namespace, rest = json.split(" ", 1)
        return Tracing_Tag.from_text(namespace, rest)

    @classmethod
    def from_text(cls, namespace, text):
        assert isinstance(namespace, str)
        assert isinstance(text, str)

        if "@" in text:
            tag, version = text.split("@", 1)
        else:
            tag     = text
            version = None
        return Tracing_Tag(namespace, tag, version)

    def hash(self):
        if not self.hash_val:
            hfunc = sha1()
            hfunc.update(self.key().encode("UTF-8"))
            self.hash_val = hfunc.hexdigest()
        return self.hash_val


class Tracing_Status(Enum):
    OK        = auto()
    PARTIAL   = auto()
    MISSING   = auto()
    JUSTIFIED = auto()
    ERROR     = auto()


class Item(metaclass=ABCMeta):
    def __init__(self, tag, location):
        assert isinstance(tag, Tracing_Tag)
        assert isinstance(location, Location)

        self.level     = None
        self.tag       = tag
        self.location  = location
        self.name      = tag.tag

        self.ref_up   = []
        self.ref_down = []

        self.unresolved_references = []

        self.messages    = []
        self.just_up     = []
        self.just_down   = []
        self.just_global = []

        self.tracing_status = None
        self.has_error      = False

    def set_level(self, level):
        assert isinstance(level, str)
        self.level = level

    def error(self, message):
        assert isinstance(message, str)
        self.messages.append(message)
        self.has_error = True

    def add_tracing_target(self, target):
        assert isinstance(target, Tracing_Tag)
        self.unresolved_references.append(target)

    def perform_source_checks(self, source_info):
        assert isinstance(source_info, dict)

    def determine_status(self, config, stab):
        assert self.level in config
        assert self.tag.key() in stab

        level = config[self.level]

        has_up_ref    = len(self.ref_up) > 0
        has_just_up   = len(self.just_up) > 0 or len(self.just_global) > 0
        has_just_down = len(self.just_down) > 0 or len(self.just_global) > 0

        # Check up references
        ok_up = True
        if level["needs_tracing_up"]:
            if not has_up_ref and not has_just_up:
                ok_up = False
                self.messages.append("missing up reference")

        # Check set of down references
        ok_down = True
        if level["needs_tracing_down"]:
            has_trace = {name : False
                         for name in config
                         if self.level in config[name]["traces"]}
            for ref in self.ref_down:
                has_trace[stab[ref.key()].level] = True
            for chain in level["breakdown_requirements"]:
                if not any(has_trace[src] for src in chain) and \
                   not has_just_down:
                    ok_down = False
                    self.messages.append("missing reference to %s" %
                                         " or ".join(sorted(chain)))

        # Set status
        if self.has_error:
            self.tracing_status = Tracing_Status.MISSING
        elif ok_up and ok_down:
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

    def additional_data_from_json(self, level, data, schema_version):
        assert isinstance(level, str)
        assert isinstance(data, dict)
        assert schema_version >= 3

        self.set_level(level)
        for ref in data.get("refs", []):
            self.add_tracing_target(Tracing_Tag.from_json(ref))
        self.ref_up = [Tracing_Tag.from_json(ref)
                       for ref in data.get("ref_up", [])]
        self.ref_down = [Tracing_Tag.from_json(ref)
                         for ref in data.get("ref_down", [])]
        self.messages = data.get("messages", [])
        self.just_up  = data.get("just_up", [])
        self.just_down = data.get("just_down", [])
        self.just_global = data.get("just_global", [])
        if "tracing_status" in data:
            self.tracing_status = Tracing_Status[data["tracing_status"]]

    def to_json(self):
        rv = {
            "tag"         : self.tag.to_json(),
            "location"    : self.location.to_json(),
            "name"        : self.name,
            "messages"    : self.messages,
            "just_up"     : self.just_up,
            "just_down"   : self.just_down,
            "just_global" : self.just_global,
        }
        if self.unresolved_references:
            rv["refs"] = [tag.to_json()
                          for tag in self.unresolved_references]
        if self.ref_up or self.ref_down:
            rv["ref_up"]   = [tag.to_json() for tag in self.ref_up]
            rv["ref_down"] = [tag.to_json() for tag in self.ref_down]
        if self.tracing_status:
            rv["tracing_status"] = self.tracing_status.name
        return rv


class Requirement(Item):
    def __init__(self, tag, location, framework, kind, name,
                 text=None, status=None):
        super().__init__(tag, location)
        assert isinstance(framework, str)
        assert isinstance(kind, str)
        assert isinstance(name, str)
        assert isinstance(text, str) or text is None
        assert isinstance(status, str) or status is None

        self.framework = framework
        self.kind      = kind
        self.name      = name
        self.text      = text
        self.status    = status

    def to_json(self):
        rv = super().to_json()
        rv["framework"] = self.framework
        rv["kind"]      = self.kind
        rv["text"]      = self.text
        rv["status"]    = self.status
        return rv

    def perform_source_checks(self, source_info):
        assert isinstance(source_info, dict)
        if source_info["valid_status"]:
            if self.status not in source_info["valid_status"]:
                self.error("status is %s, expected %s" %
                           (self.status,
                            " or ".join(sorted(source_info["valid_status"]))))

    @classmethod
    def from_json(cls, level, data, schema_version):
        assert isinstance(level, str)
        assert isinstance(data, dict)
        assert schema_version in (3, 4)

        item = Requirement(tag       = Tracing_Tag.from_json(data["tag"]),
                           location  = Location.from_json(data["location"]),
                           framework = data["framework"],
                           kind      = data["kind"],
                           name      = data["name"],
                           text      = data.get("text", None),
                           status    = data.get("status", None))
        item.additional_data_from_json(level, data, schema_version)

        return item


class Implementation(Item):
    def __init__(self, tag, location, language, kind, name):
        super().__init__(tag, location)
        assert isinstance(language, str)
        assert isinstance(kind, str)
        assert isinstance(name, str)

        self.language = language
        self.kind     = kind
        self.name     = name

    def to_json(self):
        rv = super().to_json()
        rv["language"] = self.language
        rv["kind"]     = self.kind
        return rv

    @classmethod
    def from_json(cls, level, data, schema_version):
        assert isinstance(level, str)
        assert isinstance(data, dict)
        assert schema_version == 3

        item = Implementation(tag      = Tracing_Tag.from_json(data["tag"]),
                              location = Location.from_json(data["location"]),
                              language = data["language"],
                              kind     = data["kind"],
                              name     = data["name"])
        item.additional_data_from_json(level, data, schema_version)

        return item


class Activity(Item):
    def __init__(self, tag, location, framework, kind, status=None):
        super().__init__(tag, location)
        assert isinstance(framework, str)
        assert isinstance(kind, str)
        assert isinstance(status, str) or status is None

        self.framework = framework
        self.kind      = kind
        self.status    = status

    def to_json(self):
        rv = super().to_json()
        rv["framework"] = self.framework
        rv["kind"]      = self.kind
        rv["status"]    = self.status
        return rv

    @classmethod
    def from_json(cls, level, data, schema_version):
        assert isinstance(level, str)
        assert isinstance(data, dict)
        assert schema_version == 3

        item = Activity(tag       = Tracing_Tag.from_json(data["tag"]),
                        location  = Location.from_json(data["location"]),
                        framework = data["framework"],
                        kind      = data["kind"],
                        status    = data.get("status", None))
        item.additional_data_from_json(level, data, schema_version)

        return item
