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

import os.path


class Source_Reference:
    def __init__(self, json=None, file_name=None, line_no=None):
        self.ref_kind   = None
        self.target     = None
        self.is_precise = True

        if json is None:
            assert isinstance(file_name, str)
            assert line_no is None or isinstance(line_no, int)
            self.ref_kind = "file"
            self.target   = {
                "file" : file_name,
                "line" : line_no
            }

        else:
            assert isinstance(json, dict)
            assert file_name is None
            assert line_no is None
            self.ref_kind   = json.get("ref", "file")
            self.is_precise = json.get("precise", True)
            assert self.ref_kind in ("file", "codebeamer")

            if self.ref_kind == "file":
                self.target = {
                    "file" : json["file"],
                    "line" : json["line"],
                }
            else:
                assert self.ref_kind == "codebeamer"
                self.target = {
                    "instance" : json["instance"],
                    "tracker"  : json["tracker"],
                    "item"     : json["item"],
                    "version"  : json.get("version", "HEAD"),
                }

    def to_report_json(self):
        rv = {"ref"     : self.ref_kind,
              "precise" : self.is_precise}
        rv.update(self.target)
        return rv

    def __str__(self):
        if self.ref_kind == "file":
            if self.target["line"] is None:
                return self.target["file"]
            else:
                return "%s:%s" % (self.target["file"], self.target["line"])
        else:
            assert self.ref_kind == "codebeamer"
            return "codebeamer item %u" % self.target["item"]


class LOBSTER_Error(Exception):
    def __init__(self, location, message):
        super().__init__()
        assert isinstance(location, Source_Reference)
        assert isinstance(message, str)
        self.location = location
        self.message  = message


class Message_Handler:
    def __init__(self):
        pass

    def emit(self, location, severity, message):
        assert isinstance(location, Source_Reference)
        assert severity in ("warning", "lex error", "error")
        assert isinstance(message, str)

        print("%s: %s: %s" % (str(location),
                              severity,
                              message))

    def lex_error(self, location, message):
        assert isinstance(location, Source_Reference)
        assert isinstance(message, str)

        self.emit(location, "lex error", message)
        raise LOBSTER_Error(location, message)

    def error(self, location, message, fatal=True):
        assert isinstance(location, Source_Reference)
        assert isinstance(message, str)

        self.emit(location, "error", message)
        if fatal:
            raise LOBSTER_Error(location, message)

    def warning(self, location, message):
        assert isinstance(location, Source_Reference)
        assert isinstance(message, str)

        self.emit(location, "warning", message)
