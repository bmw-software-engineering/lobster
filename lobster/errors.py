#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Tracability Evidence Report
# Copyright (C) 2022-2023 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

from lobster.exceptions import LOBSTER_Exception
from lobster.location import Location


class LOBSTER_Error(LOBSTER_Exception):
    def __init__(self, location, message):
        super().__init__(message)
        assert isinstance(location, Location)
        assert isinstance(message, str)
        self.location = location
        self.message  = message

    def dump(self):
        print(self.location.to_string() + ": " + self.message)


class Message_Handler:
    def __init__(self):
        self.warnings = 0
        self.errors   = 0

    def emit(self, location, severity, message):
        assert isinstance(location, Location)
        assert severity in ("warning", "lex error", "error")
        assert isinstance(message, str)

        if severity == "warning":
            self.warnings += 1
        else:
            self.errors += 1

        print("%s: lobster %s: %s" % (location.to_string(),
                                      severity,
                                      message))

    def lex_error(self, location, message):
        assert isinstance(location, Location)
        assert isinstance(message, str)

        self.emit(location, "lex error", message)
        raise LOBSTER_Error(location, message)

    def error(self, location, message, fatal=True):
        assert isinstance(location, Location)
        assert isinstance(message, str)

        self.emit(location, "error", message)
        if fatal:
            raise LOBSTER_Error(location, message)

    def warning(self, location, message):
        assert isinstance(location, Location)
        assert isinstance(message, str)

        self.emit(location, "warning", message)
