#!/usr/bin/env python3
#
# lobster_matlab - Extract Octave or MATLAB tracing tags for LOBSTER
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
import argparse
import os.path
import subprocess
import re
import json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files",
                    nargs="+",
                    metavar="FILE|DIR")
    ap.add_argument("--code-out",
                    default=None)
    ap.add_argument("--test-out",
                    default=None)

    options = ap.parse_args()

    prefix = os.getcwd()

    rv = subprocess.run([sys.executable,
                         "-m", "miss_hit.mh_trace"] +
                        options.files,
                        encoding="UTF-8")

    if (rv.returncode != 0):
        return 1

    with open("mh_trace.json", "r") as fd:
        data = json.load(fd)

    db_code = {}
    db_test = {}
    for function_name, function in data.items():
        if function["test"]:
            db_test[function_name] = {
                "source"    : {"file" : function["source"]["filename"],
                               "line" : function["source"]["line"]},
                "language"  : "MATLAB",
                "kind"      : "test",
                "framework" : "MATLAB",
                "tags"      : function["tags"],
                "status"    : "unknown",
            }
        else:
            db_code[function_name] = {
                "source"   : {"file" : function["source"]["filename"],
                              "line" : function["source"]["line"]},
                "language" : "MATLAB",
                "kind"     : "function",
                "tags"     : function["tags"],
            }

    db_code = {"schema"    : "lobster-imp-trace",
               "generator" : "lobster_matlab",
               "version"   : 1,
               "data"      : db_code}
    db_test = {"schema"    : "lobster-act-trace",
               "generator" : "lobster_matlab",
               "version"   : 1,
               "data"      : db_test}

    if options.code_out:
        with open(options.code_out, "w") as fd:
            json.dump(db_code, fd, indent=4, sort_keys=True)
        print("Written output for %u items to %s" % (len(db_code["data"]),
                                                     options.code_out))

    if options.test_out:
        with open(options.test_out, "w") as fd:
            json.dump(db_test, fd, indent=4, sort_keys=True)
        print("Written output for %u items to %s" % (len(db_test["data"]),
                                                     options.test_out))
