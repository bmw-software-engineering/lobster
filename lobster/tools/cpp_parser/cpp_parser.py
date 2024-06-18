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

from lobster.items import Tracing_Tag, Implementation
from lobster.location import File_Reference
from lobster.io import lobster_write
from lobster.tools.cpp_parser.parser.requirements_parser import ParserForRequirements


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files",
                    nargs="+",
                    metavar="FILE|DIR")
    ap.add_argument("--out",
                    default=None,
                    help="write output to this file; otherwise output to stdout")

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

    parser = ParserForRequirements()
    requirement_details = parser.fetch_requirement_details_for_test_files(test_files=file_list)

    db = {}

    for requirement_detail in requirement_details:
        # get requirement detail properties delivered from parser
        tracking_id: str = requirement_detail.get('tracking_id')
        function_name: str = requirement_detail.get('component')
        test_desc: str = requirement_detail.get('test_desc')
        file_name_with_line_number: str = requirement_detail.get('file_name')

        # convert into fitting parameters for Implementation
        file_name, line_nr = file_name_with_line_number.split("#L")
        filename = os.path.relpath(file_name, prefix)
        line_nr = int(line_nr)
        function_uid = "%s:%s:%u" % (os.path.basename(filename),
                                     function_name,
                                     line_nr)
        tag = Tracing_Tag("cpp", function_uid)
        loc = File_Reference(filename, line_nr)
        kind = 'Function'
        ref = tracking_id

        if tag.key() not in db:
            db[tag.key()] = Implementation(
                tag      = tag,
                location = loc,
                language = "C/C++",
                kind     = kind,
                name     = function_name)

        db[tag.key()].add_tracing_target(Tracing_Tag("req", ref))

    if options.out:
        with open(options.out, "w", encoding="UTF-8") as fd:
            lobster_write(fd, Implementation, "lobster_xxx_cpp", db.values())
        print("Written output for %u items to %s" % (len(db), options.out))

    else:
        lobster_write(sys.stdout, Implementation, "lobster_xxx_cpp", db.values())
        print()


if __name__ == "__main__":
    sys.exit(main())
