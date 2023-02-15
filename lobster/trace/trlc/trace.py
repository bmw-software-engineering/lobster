#!/usr/bin/env python3
#
# lobster_trlc - Extract TRLC requirements for LOBSTER
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

import argparse
import os.path
import subprocess
import re
import json

from trlc.errors import Message_Handler, TRLC_Error
from trlc.trlc import Source_Manager
from trlc.ast import Package


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files",
                    nargs="+",
                    metavar="FILE|DIR")
    ap.add_argument("--out",
                    default=None)
    ap.add_argument("--descriptions",
                    nargs="+",
                    default=["text"],
                    metavar="TRLC attribute name")
    ap.add_argument("--tags",
                    nargs="+",
                    default=[],
                    metavar="TRLC attribute name")

    options = ap.parse_args()

    mh = Message_Handler()
    sm = Source_Manager(mh)

    try:
        for name in options.files:
            if os.path.isfile(name):
                sm.register_file(name)
            elif os.path.isdir(name):
                sm.register_directory(name)
            else:
                ap.error("%s is not a file or directory" % name)
        stab = sm.process()
    except TRLC_Error:
        return 1

    if stab is None:
        return 1

    db = {}

    for pkg in stab.table.values():
        if not isinstance(pkg, Package):
            continue
        for obj in pkg.symbols.iter_record_objects():
            py_obj = obj.to_python_dict()
            text = []
            for attr_name in options.descriptions:
                if attr_name not in py_obj:
                    continue
                if isinstance(py_obj[attr_name], str):
                    text.append(py_obj[attr_name])
                elif isinstance(py_obj[attr_name], list):
                    for text_item in py_obj[attr_name]:
                        text.append(text_item)
            if text:
                text = "\n".join(text)
            else:
                text = None

            item = {
                "kind"      : obj.e_typ.name,
                "name"      : "%s (%s)" % (obj.name.replace("_", " "),
                                           pkg.name),
                "text"      : text,
                "framework" : "TRLC",
                "source"    : {"file" : obj.location.file_name,
                               "line" : obj.location.line_no},
                "tags"      : [],
            }
            for tagname in options.tags:
                if tagname in py_obj and py_obj[tagname]:
                    item["tags"].append(str(py_obj[tagname]))
            db[pkg.name + "." + obj.name] = item

    db = {"schema"    : "lobster-req-trace",
          "generator" : "lobster_trlc",
          "version"   : 2,
          "data"      : db}

    if options.out:
        with open(options.out, "w") as fd:
            json.dump(db, fd, indent=4, sort_keys=True)
        print("Written output for %u items to %s" % (len(db["data"]),
                                                     options.out))
    else:
        print(json.dumps(db, indent=4, sort_keys=True))
