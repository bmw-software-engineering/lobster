#!/usr/bin/env python3
#
# lobster_cpp - Extract C/C++ tracing tags for LOBSTER
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

import sys
import argparse
import os.path
import subprocess
import re

from lobster.items import Tracing_Tag, Implementation
from lobster.location import File_Reference
from lobster.io import lobster_write


FILE_LINE_PATTERN = r"(.*):(\d+):\d+:"
KIND_PATTERN = r"(function|main function|method)"
NAME_PATTERN = r"([a-zA-Z0-9_:~]+)"
PREFIX = "^%s warning:" % FILE_LINE_PATTERN
SUFFIX = r"\[lobster-tracing\]$"

RE_NOTAGS = (PREFIX + " " +
             "%s %s has no tracing tags" % (KIND_PATTERN,
                                            NAME_PATTERN) +
             " " + SUFFIX)
RE_TAGS = (PREFIX + " " +
           r"%s %s traces to +(.+) +" % (KIND_PATTERN,
                                         NAME_PATTERN) +
           SUFFIX)
RE_JUST = (PREFIX + " " +
           r"%s %s exempt from tracing: +(.+) +" % (KIND_PATTERN,
                                                    NAME_PATTERN) +
           SUFFIX)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files",
                    nargs="+",
                    metavar="FILE|DIR")
    ap.add_argument("--clang-tidy",
                    default="clang-tidy",
                    metavar="FILE",
                    help=("use the specified clang-tidy; by default we"
                          " pick the one on PATH"))
    ap.add_argument("--out",
                    default=None,
                    help=("write output to this file; otherwise output to"
                          " to stdout"))

    options = ap.parse_args()

    file_list = []
    for item in options.files:
        if os.path.isfile(item):
            file_list.append(item)
        elif os.path.isdir(item):
            for path, _, files in os.walk(item):
                for filename in files:
                    _, ext = os.path.splitext(filename)
                    if ext in (".cpp", ".cc", ".c", ".h"):
                        file_list.append(os.path.join(path, filename))
        else:
            ap.error("%s is not a file or directory" % item)

    prefix = os.getcwd()

    # Test if the clang-tidy can be used

    rv = subprocess.run([os.path.expanduser(options.clang_tidy),
                         "-checks=-*,lobster-tracing",
                         "--list-checks"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        encoding="UTF-8",
                        check=False)

    if "No checks enabled." in rv.stderr:
        print("The provided clang-tidy does include the lobster-tracing check")
        print("> Please build from "
              "https://github.com/bmw-software-engineering/llvm-project")
        print("> Or make sure to provide the "
              "correct binary using the --clang-tidy flag")
        return 1

    rv = subprocess.run([os.path.expanduser(options.clang_tidy),
                         "-checks=-*,lobster-tracing"] +
                        file_list,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        encoding="UTF-8",
                        check=False)

    if rv.returncode != 0:
        found_reason = False
        for line in rv.stdout.splitlines():
            if "error: " in line:
                print(line)
                found_reason = True
        if not found_reason:
            print(rv.stdout)
        print()
        print(rv.stderr)
        return 1

    db = {}

    for line in rv.stdout.splitlines():
        if not line.endswith("[lobster-tracing]"):
            continue

        match = re.match(RE_NOTAGS, line)
        if match:
            filename, line_nr, kind, function_name = match.groups()
            filename = os.path.relpath(filename, prefix)
            line_nr = int(line_nr)
            function_uid = "%s:%s:%u" % (os.path.basename(filename),
                                         function_name,
                                         line_nr)
            tag = Tracing_Tag("cpp", function_uid)
            loc = File_Reference(filename, line_nr)

            assert tag.key() not in db
            db[tag.key()] = Implementation(
                tag      = tag,
                location = loc,
                language = "C/C++",
                kind     = kind,
                name     = function_name)

            continue

        match = re.match(RE_JUST, line)
        if match:
            filename, line_nr, kind, function_name, reason = match.groups()
            filename = os.path.relpath(filename, prefix)
            line_nr = int(line_nr)
            function_uid = "%s:%s:%u" % (os.path.basename(filename),
                                         function_name,
                                         line_nr)
            tag = Tracing_Tag("cpp", function_uid)
            loc = File_Reference(filename, line_nr)

            if tag.key() not in db:
                db[tag.key()] = Implementation(
                    tag      = tag,
                    location = loc,
                    language = "C/C++",
                    kind     = kind,
                    name     = function_name)

            db[tag.key].just_up.append(reason)

            continue

        match = re.match(RE_TAGS, line)
        if match:
            filename, line_nr, kind, function_name, ref = match.groups()
            filename = os.path.relpath(filename, prefix)
            line_nr = int(line_nr)
            function_uid = "%s:%s:%u" % (os.path.basename(filename),
                                         function_name,
                                         line_nr)
            tag = Tracing_Tag("cpp", function_uid)
            loc = File_Reference(filename, line_nr)

            if tag.key() not in db:
                db[tag.key()] = Implementation(
                    tag      = tag,
                    location = loc,
                    language = "C/C++",
                    kind     = kind,
                    name     = function_name)

            db[tag.key()].add_tracing_target(Tracing_Tag("req", ref))

            continue

        print("could not parse line")
        print(">", line)
        return 1

    if options.out:
        with open(options.out, "w", encoding="UTF-8") as fd:
            lobster_write(fd, Implementation, "lobster_cpp", db.values())
        print("Written output for %u items to %s" % (len(db), options.out))

    else:
        lobster_write(sys.stdout, Implementation, "lobster_cpp", db.values())
        print()


if __name__ == "__main__":
    sys.exit(main())
