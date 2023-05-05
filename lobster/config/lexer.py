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

from lobster import errors
from lobster import location


class Token:
    def __init__(self, kind, text, loc):
        self.kind = kind
        self.text = text
        self.loc  = loc

    def value(self):
        if self.kind == "STRING":
            return self.text[1:-1]
        else:
            return self.text

    def __repr__(self):
        return "Token(%s, %s, %s)" % (self.kind,
                                      self.text,
                                      self.loc)


class Lexer:
    def __init__(self, mh, file_name):
        assert isinstance(mh, errors.Message_Handler)
        assert isinstance(file_name, str)
        assert os.path.isfile(file_name)

        self.file_name = file_name
        self.mh        = mh

        with open(file_name, "r", encoding="UTF-8") as fd:
            self.content = fd.read()
            self.length  = len(self.content)

        self.lexpos = -1
        self.line_nr = 1
        self.cc = None
        self.nc = self.content[0] if self.length > 0 else None

    def advance(self):
        self.lexpos += 1
        if self.cc == "\n":
            self.line_nr += 1
        self.cc = self.nc
        if self.lexpos + 1 < self.length:
            self.nc = self.content[self.lexpos + 1]
        else:
            self.nc = None

    def error(self, message):
        loc = location.File_Reference(filename = self.file_name,
                                      line     = self.line_nr)
        self.mh.lex_error(loc, message)

    def token(self):
        # Skip comments and whitespace
        while True:
            while self.nc and self.nc.isspace():
                self.advance()
            if self.nc is None:
                return None
            self.advance()

            if self.cc == "#":
                while self.cc and self.cc != "\n":
                    self.advance()
            else:
                break

        kind    = None
        t_start = self.lexpos

        if self.cc == "{":
            kind = "C_BRA"
        elif self.cc == "}":
            kind = "C_KET"
        elif self.cc == ":":
            kind = "COLON"
        elif self.cc == ",":
            kind = "COMMA"
        elif self.cc == ";":
            kind = "SEMI"
        elif self.cc == '"':
            kind = "STRING"
            self.advance()
            while self.cc != '"':
                self.advance()
                if self.cc in (None, "\n"):
                    self.error("unterminated string")
        elif self.cc.isalpha():
            kind = "KEYWORD"
            while self.nc.isalpha() or self.nc == "_":
                self.advance()
        else:
            self.error("unexpected character: '%s'" % self.cc)

        t_end = self.lexpos

        return Token(
            kind = kind,
            text = self.content[t_start : t_end + 1],
            loc  = location.File_Reference(filename = self.file_name,
                                           line     = self.line_nr))


def sanity_test():
    mh = errors.Message_Handler()
    lexer = Lexer(mh, sys.argv[1])
    try:
        while True:
            tok = lexer.token()
            if tok is None:
                break
            print(tok)
    except errors.LOBSTER_Error:
        return 1
    return 0


if __name__ == "__main__":
    sanity_test()
