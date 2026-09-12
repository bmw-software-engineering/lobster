#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2022-2024 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

from lobster.common import lexer
from lobster.common import errors
from lobster.common import location
from lobster.common.raw_policy import (
    RawLevel, RawPolicy, RawRequiresCandidate, RawSource, RawTraceTo,
)
from lobster.common.policy_builder import build_tracing_policy


class Parser:
    def __init__(self, mh, file_name):
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"Config file not found: {file_name}")

        self.lexer = lexer.Lexer(mh, file_name)

        self.ct = None
        self.nt = self.lexer.token()

    def advance(self):
        self.ct = self.nt
        self.nt = self.lexer.token()

    def peek(self, kind, value=None):
        if self.nt is None:
            return kind is None
        if kind is None:
            return False
        if self.nt.kind == kind:
            if value is None:
                return True
            return self.nt.value() == value
        return False

    def match(self, kind, value=None):
        if self.peek(kind, value):
            self.advance()
        elif self.nt is None:
            self.error(
                location.File_Reference(filename = self.lexer.file_name),
                f"expected {kind}, found EOF")
        elif value is None:
            self.error(self.nt.loc,
                       f"expected {kind}, found {self.nt.kind} {self.nt.value()}")
        else:
            self.error(self.nt.loc,
                       f"expected {value}, found {self.nt.value()}")

    def warning(self, loc, message):
        self.lexer.mh.warning(loc, message)

    def error(self, loc, message):
        self.lexer.mh.error(loc, message)

    def parse(self):
        levels = []

        while self.nt:
            if self.peek("KEYWORD", "requirements") or \
               self.peek("KEYWORD", "implementation") or \
               self.peek("KEYWORD", "activity"):
                levels.append(self.parse_level_declaration())
            else:
                self.error(self.nt.loc,
                           "expected: requirements|implementation|activity,"
                           f" found {self.nt.value()} instead")

        return RawPolicy(levels=levels)

    def parse_level_declaration(self):
        self.match("KEYWORD")
        level_kind = self.ct.value()

        self.match("STRING")
        level_name = self.ct.value()
        level = RawLevel(name=level_name, name_loc=self.ct.loc, kind=level_kind)

        self.match("C_BRA")

        while not self.peek("C_KET"):
            if self.peek("KEYWORD", "source"):
                self.advance()
                self.match("COLON")
                self.match("STRING")
                level.source.append(RawSource(file=self.ct.value(), loc=self.ct.loc))

                if self.peek("KEYWORD", "with"):
                    self.match("KEYWORD", "with")

                self.match("SEMI")

            elif self.peek("KEYWORD", "trace"):
                self.match("KEYWORD", "trace")
                self.match("KEYWORD", "to")
                self.match("COLON")
                self.match("STRING")
                level.trace_to.append(
                    RawTraceTo(target=self.ct.value(), loc=self.ct.loc))

                self.match("SEMI")

            elif self.peek("KEYWORD", "requires"):
                self.match("KEYWORD", "requires")
                self.match("COLON")

                req_list = []

                self.match("STRING")
                req_list.append(
                    RawRequiresCandidate(name=self.ct.value(), loc=self.ct.loc))

                while self.peek("KEYWORD", "or"):
                    self.match("KEYWORD", "or")
                    self.match("STRING")
                    req_list.append(
                        RawRequiresCandidate(name=self.ct.value(), loc=self.ct.loc))

                self.match("SEMI")

                level.requires.append(req_list)

            else:
                self.error(self.nt.loc,
                           f"unexpected directive {self.nt.value()}")

        self.match("C_KET")

        return level


def load(mh, file_name):
    parser = Parser(mh, file_name)
    raw_policy = parser.parse()
    return build_tracing_policy(mh, raw_policy)


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
