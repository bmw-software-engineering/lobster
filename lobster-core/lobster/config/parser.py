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

import sys
import os.path
import collections

from lobster.config import lexer
from lobster import errors
from lobster import location


class Parser:
    def __init__(self, mh, file_name):
        assert isinstance(mh, errors.Message_Handler)
        assert isinstance(file_name, str)
        assert os.path.isfile(file_name)

        self.lexer = lexer.Lexer(mh, file_name)

        self.ct = None
        self.nt = self.lexer.token()

        self.levels = collections.OrderedDict()

    def advance(self):
        self.ct = self.nt
        self.nt = self.lexer.token()

    def peek(self, kind, value=None):
        if self.nt is None:
            return kind is None
        elif kind is None:
            return False
        elif self.nt.kind == kind:
            if value is None:
                return True
            else:
                return self.nt.value() == value
        else:
            return False

    def match(self, kind, value=None):
        if self.peek(kind, value):
            self.advance()
        elif self.nt is None:
            self.error(
                location.File_Reference(filename = self.lexer.file_name),
                "expected %s, found EOF" % kind)
        elif value is None:
            self.error(self.nt.loc,
                       "expected %s, found %s %s" % (kind,
                                                     self.nt.kind,
                                                     self.nt.value()))
        else:
            self.error(self.nt.loc,
                       "expected %s, found %s" % (value, self.nt.value()))

    def warning(self, loc, message):
        self.lexer.mh.warning(loc, message)

    def error(self, loc, message):
        self.lexer.mh.error(loc, message)

    def parse(self):
        while self.nt:
            if self.peek("KEYWORD", "requirements") or \
               self.peek("KEYWORD", "implementation") or \
               self.peek("KEYWORD", "activity"):
                self.parse_level_declaration()
            else:
                self.error(self.nt.loc,
                           "expected: requirements|implementation|activity,"
                           " found %s instead" % self.nt.value())

        return self.levels

    def parse_level_declaration(self):
        self.match("KEYWORD")
        level_kind = self.ct.value()

        self.match("STRING")
        level_name = self.ct.value()
        if level_name in self.levels:
            self.error(self.ct.loc,
                       "duplicate declaration")

        item = {
            "name"                   : level_name,
            "kind"                   : level_kind,
            "traces"                 : [],
            "source"                 : [],
            "needs_tracing_up"       : False,
            "needs_tracing_down"     : False,
            "raw_trace_requirements" : []
        }
        self.levels[level_name] = item

        self.match("C_BRA")

        while not self.peek("C_KET"):
            if self.peek("KEYWORD", "source"):
                self.advance()
                self.match("COLON")
                self.match("STRING")
                source_info = {
                    "file"    : self.ct.value(),
                    "filters" : [],
                }
                if level_kind == "requirements":
                    source_info["valid_status"] = []
                if not os.path.isfile(source_info["file"]):
                    self.error(self.ct.loc,
                               "cannot find file %s" % source_info["file"])
                item["source"].append(source_info)

                if self.peek("KEYWORD", "with"):
                    self.match("KEYWORD", "with")

                    while not self.peek("SEMI"):
                        self.match("KEYWORD")
                        if self.ct.value() == "prefix":
                            self.match("STRING")
                            source_info["filters"].append(("prefix",
                                                           self.ct.value()))

                        elif self.ct.value() == "valid_status":
                            if level_kind != "requirements":
                                self.error(self.ct.loc,
                                           "property valid_status is only "
                                           "applicable for requirements")
                            self.match("C_BRA")
                            while True:
                                self.match("STRING")
                                value = self.ct.value()
                                if value in source_info["valid_status"]:
                                    self.warning(self.ct.loc,
                                                 "duplicate status %s" %
                                                 value)
                                else:
                                    source_info["valid_status"].append(value)
                                if self.peek("COMMA"):
                                    self.match("COMMA")
                                else:
                                    break
                            self.match("C_KET")

                        else:
                            self.error(self.ct.loc,
                                       "unknown property '%s'" %
                                       self.ct.value())

                self.match("SEMI")

            elif self.peek("KEYWORD", "trace"):
                self.match("KEYWORD", "trace")
                self.match("KEYWORD", "to")
                self.match("COLON")
                self.match("STRING")
                if self.ct.value() == level_name:
                    self.error(self.ct.loc,
                               "cannot trace to yourself")
                elif self.ct.value() not in self.levels:
                    self.error(self.ct.loc,
                               "unknown item %s" % self.ct.value())
                else:
                    self.levels[self.ct.value()]["needs_tracing_down"] = True
                item["traces"].append(self.ct.value())
                item["needs_tracing_up"] = True

                self.match("SEMI")

            elif self.peek("KEYWORD", "requires"):
                self.match("KEYWORD", "requires")
                self.match("COLON")

                req_list = []

                self.match("STRING")
                req_list.append(self.ct)

                while self.peek("KEYWORD", "or"):
                    self.match("KEYWORD", "or")
                    self.match("STRING")
                    req_list.append(self.ct)

                self.match("SEMI")

                item["raw_trace_requirements"].append(req_list)

            else:
                self.error(self.nt.loc,
                           "unexpected directive %s" % self.nt.value())

        self.match("C_KET")


def load(mh, file_name):
    parser = Parser(mh, file_name)
    ast = parser.parse()

    # Resolve requires links now
    for item in ast.values():
        item["breakdown_requirements"] = []
        if len(item["raw_trace_requirements"]) > 0:
            for chain in item["raw_trace_requirements"]:
                new_chain = []
                for tok in chain:
                    if tok.value() not in ast:
                        mh.error(tok.loc, "unknown level %s" % tok.value())
                    if item["name"] not in ast[tok.value()]["traces"]:
                        mh.error(tok.loc,
                                 "%s cannot trace to %s items" %
                                 (tok.value(),
                                  item["name"]))
                    new_chain.append(tok.value())
                item["breakdown_requirements"].append(new_chain)
        else:
            for src in ast.values():
                if item["name"] in src["traces"]:
                    item["breakdown_requirements"].append([src["name"]])
        del item["raw_trace_requirements"]

    return ast


def sanity_test():
    mh = errors.Message_Handler()

    try:
        config = load(mh, sys.argv[1])
        print(config)
    except errors.LOBSTER_Error:
        return 1
    return 0


if __name__ == "__main__":
    sanity_test()
