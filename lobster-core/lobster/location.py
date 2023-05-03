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

from abc import ABCMeta, abstractmethod

from lobster.exceptions import LOBSTER_Exception


class Location(metaclass=ABCMeta):
    @abstractmethod
    def to_string(self):
        pass

    @abstractmethod
    def to_html(self):
        pass

    @abstractmethod
    def to_json(self):
        pass

    @classmethod
    def from_json(cls, json):
        if not isinstance(json, dict):
            raise LOBSTER_Exception("location data not an object",
                                    json)
        if "kind" not in json:
            raise LOBSTER_Exception("location data does not contain 'kind'",
                                    json)

        try:
            if json["kind"] == "file":
                return File_Reference.from_json(json)
            elif json["kind"] == "github":
                return Github_Reference.from_json(json)
            elif json["kind"] == "codebeamer":
                return Codebeamer_Reference.from_json(json)
            else:
                raise LOBSTER_Exception("unknown location kind %s" %
                                        json["kind"])
        except KeyError as err:
            raise LOBSTER_Exception(
                "malformed location data, missing %s" % err.args[0],
                json) from err
        except AssertionError:
            raise LOBSTER_Exception(
                "malformed %s location data" % json["kind"],
                json) from err


class File_Reference(Location):
    def __init__(self, filename, line=None, column=None):
        assert isinstance(filename, str)
        assert line is None or (isinstance(line, int) and
                                line >= 1)
        assert column is None or (line is not None and
                                  isinstance(column, int) and
                                  column >= 1)
        self.filename = filename
        self.line     = line
        self.column   = column

    def to_string(self):
        rv = self.filename
        if self.line:
            rv += ":%u" % self.line
        if self.column:
            rv += ":%u" % self.column
        return rv

    def to_html(self):
        return '<a href="%s" target="_blank">%s</a>' % (self.filename,
                                                        self.filename)

    def to_json(self):
        return {"kind"   : "file",
                "file"   : self.filename,
                "line"   : self.line,
                "column" : self.column}

    @classmethod
    def from_json(cls, json):
        assert isinstance(json, dict)
        assert json["kind"] == "file"

        filename = json["file"]
        line     = json.get("line", None)
        if line is not None:
            column = json.get("column", None)
        else:
            column = None
        return File_Reference(filename, line, column)


class Github_Reference(Location):
    def __init__(self, gh_root, commit, filename, line):
        assert isinstance(gh_root, str)
        assert gh_root.startswith("http")
        assert isinstance(commit, str)
        assert isinstance(filename, str)
        assert line is None or (isinstance(line, int) and
                                line >= 1)

        self.gh_root  = gh_root.rstrip("/")
        self.gh_repo  = self.gh_root.split("/")[-1]
        self.commit   = commit
        self.filename = filename
        self.line     = line

    def to_string(self):
        if self.line:
            return "%s:%u" % (self.filename,
                              self.line)
        else:
            return self.filename

    def to_html(self):
        file_ref = self.filename
        if self.line:
            file_ref += "#L%u" % self.line

        return '<a href="%s/blob/%s/%s" target="_blank">%s</a>' % (
            self.gh_root,
            self.commit,
            file_ref,
            self.to_string())

    def to_json(self):
        return {"kind"    : "github",
                "gh_root" : self.gh_root,
                "commit"  : self.commit,
                "file"    : self.filename,
                "line"    : self.line}

    @classmethod
    def from_json(cls, json):
        assert isinstance(json, dict)
        assert json["kind"] == "github"

        gh_root  = json["gh_root"]
        commit   = json["commit"]
        filename = json["file"]
        line     = json.get("line", None)
        return Github_Reference(gh_root, commit, filename, line)


class Codebeamer_Reference(Location):
    def __init__(self, cb_root, tracker, item, version, name=None):
        assert isinstance(cb_root, str)
        assert cb_root.startswith("http")
        assert isinstance(tracker, int) and tracker >= 1
        assert isinstance(item, int) and item >= 1
        assert version is None or (isinstance(version, int) and
                                   version >= 1)
        assert name is None or isinstance(name, str)

        self.cb_root  = cb_root
        self.tracker  = tracker
        self.item     = item
        self.version  = version
        self.name     = name

    def to_string(self):
        if self.name:
            return "cb item %u '%s'" % (self.item, self.name)
        else:
            return "cb item %u" % self.item

    def to_html(self):
        url = self.cb_root
        # This is supposed to open the document view, but it doesn't
        # always work.
        #
        # url += "/cb/tracker/%u" % self.tracker
        # url += "?view_id=-11&selectedItemId=%u" % self.item
        # url += "&forceDocumentViewLayout=true"

        # We can just open the item directly
        url += "/cb/issue/%u" % self.item
        return '<a href="%s" target="_blank">%s</a>' % (url, self.to_string())

    def to_json(self):
        return {"kind"    : "codebeamer",
                "cb_root" : self.cb_root,
                "tracker" : self.tracker,
                "item"    : self.item,
                "version" : self.version,
                "name"    : self.name}

    @classmethod
    def from_json(cls, json):
        assert isinstance(json, dict)
        assert json["kind"] == "codebeamer"

        cb_root = json["cb_root"]
        tracker = json["tracker"]
        item    = json["item"]
        version = json.get("version", None)
        name    = json.get("name", None)
        return Codebeamer_Reference(cb_root, tracker, item, version, name)
