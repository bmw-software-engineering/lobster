#!/usr/bin/env python3
#
# lobster_json - Extract JSON tags for LOBSTER
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
import os
import argparse
import json

from lobster.items import Tracing_Tag, Activity
from lobster.io import lobster_write
from lobster.location import File_Reference


def fetch_values(filename, data, name):
    chain = name.split(".")

    ptr = data
    current = []
    for attr in chain[:-1]:
        current.append(attr)
        if attr in ptr:
            ptr = ptr[attr]
        else:
            print("%s: error: object does not contain %s" %
                  (filename, ".".join(current)))
            return None
        if not isinstance(ptr, dict):
            print("%s: error: %s is not an object" %
                  (filename, ".".join("current")))
            return None

    if chain[-1] not in ptr:
        print("%s: error: object does not contain attribute %s" %
              (filename, chain[-1]))
        return None

    ptr = ptr[chain[-1]]
    tags = []
    if isinstance(ptr, list):
        for tag in ptr:
            if isinstance(tag, str):
                tags.append(tag)
            elif isinstance(tag, int):
                tags.append(str(tag))
            else:
                print("%s: error: tag %s is neither string nor integer" %
                      (filename, tag))
    elif isinstance(ptr, str):
        tags.append(ptr)
    elif isinstance(ptr, int):
        tags.append(str(ptr))
    else:
        print("%s: error: tag %s is neither string nor integer" %
              (filename, tag))

    return tags


def process_dict(db, filename, item_kind, data,
                 tag_attr,
                 name_attr,
                 include_path_in_name,
                 sequence):
    assert isinstance(sequence, int) or sequence is None

    # Get human name
    if name_attr is not None:
        short_name = fetch_values(filename, data, name_attr)
        if not short_name:
            return
        elif len(short_name) != 1:
            print("%s: error: only a single name can be given (%s)" %
                  (filename, " or ".join(short_name)))
        short_name = short_name[0]
    else:
        short_name = None

    # Make a name based on filename
    if not include_path_in_name:
        base = os.path.basename(filename)
    else:
        base = filename
    base = base.replace("\\", "/").strip("./").replace(".json", "")
    parts = base.replace(" ", "_").split("/")
    name = ".".join(parts)
    if sequence is not None:
        name += "_%u" % sequence

    tags = fetch_values(filename, data, tag_attr)
    if tags is None:
        return

    if name in db:
        print("%s: error: duplicate object %s" % (filename, name))
        return

    db[name] = Activity(tag       = Tracing_Tag("json", name),
                        location  = File_Reference(os.path.relpath(filename)),
                        framework = "JSON",
                        kind      = item_kind)
    for tag in tags:
        db[name].add_tracing_target(Tracing_Tag("req", tag))
    if short_name is not None:
        db[name].name = short_name


def process(db, filename, item_kind,
            tag_attr, name_attr, include_path_in_name):
    assert isinstance(db, dict)
    assert os.path.isfile(filename)
    assert isinstance(tag_attr, str)
    assert isinstance(name_attr, str) or name_attr is None
    assert isinstance(include_path_in_name, bool)

    with open(filename, "r", encoding="UTF-8") as fd:
        data = json.load(fd)

    if isinstance(data, dict):
        process_dict(db, filename, item_kind, data,
                     tag_attr,
                     name_attr,
                     include_path_in_name,
                     None)
    elif isinstance(data, list):
        for n, item in enumerate(data):
            process_dict(db, filename, item_kind, item,
                         tag_attr,
                         name_attr,
                         include_path_in_name,
                         n)
    else:
        print("%s: error: top level value is not an array or object" %
              filename)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag-attribute",
                    help=("attribute indicating the tag(s) of the "
                          "top-level json object"),
                    required=True)
    ap.add_argument("--name-attribute",
                    help="attribute indicating the name of the activity")
    ap.add_argument("--include-path-in-name",
                    help="when synthesising names, include the total path",
                    default=False,
                    action="store_true")
    ap.add_argument("--out",
                    help="write to this file instead of stdout")
    ap.add_argument("--item-kind",
                    help="item kind (by default 'test')",
                    default="test")
    ap.add_argument("paths",
                    metavar="FILE|DIR",
                    nargs="+",
                    help="process these files or directories")

    options = ap.parse_args()

    db = {}

    for path in options.paths:
        if os.path.isfile(path):
            process(db, path, options.item_kind,
                    options.tag_attribute,
                    options.name_attribute,
                    options.include_path_in_name)
        elif os.path.isdir(path):
            for prefix, _, files in os.walk(path):
                for filename in files:
                    if filename.endswith(".json"):
                        process(db,
                                os.path.join(prefix, filename),
                                options.item_kind,
                                options.tag_attribute,
                                options.name_attribute,
                                options.include_path_in_name)
        else:
            ap.error("%s is not a file or directory" % path)

    if options.out:
        with open(options.out, "w", encoding="UTF-8") as fd:
            lobster_write(fd, Activity, "lobster_json", db.values())
    else:
        lobster_write(sys.stdout, Activity, "lobster_json", db.values())
        print()


if __name__ == "__main__":
    sys.exit(main())
