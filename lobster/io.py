#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2023, 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

from collections.abc import Iterable
import json
from typing import Dict, Optional, Sequence, TextIO, Type, Union

from lobster.errors import Message_Handler
from lobster.location import File_Reference
from lobster.items import Requirement, Implementation, Activity


def lobster_write(
        fd: TextIO,
        kind: Union[Type[Requirement], Type[Implementation], Type[Activity]],
        generator: str,
        items: Iterable,
):
    if not all(isinstance(item, kind) for item in items):
        raise ValueError(
            f"All elements in 'items' must be of the type {kind.__name__}!",
        )

    if kind is Requirement:
        schema  = "lobster-req-trace"
        version = 4
    elif kind is Implementation:
        schema  = "lobster-imp-trace"
        version = 3
    else:
        schema  = "lobster-act-trace"
        version = 3

    data = {"data"      : list(x.to_json() for x in items),
            "generator" : generator,
            "schema"    : schema,
            "version"   : version}
    json.dump(data, fd, indent=2)
    fd.write("\n")


def lobster_read(
        mh,
        filename: str,
        level: str,
        items: Dict[str, Union[Activity, Implementation, Requirement]],
        source_info: Optional[Dict] = None,
):
    loc = File_Reference(filename)

    # Read and validate JSON
    with open(filename, "r", encoding="UTF-8") as fd:
        try:
            data = json.load(fd)
        except json.decoder.JSONDecodeError as err:
            mh.error(File_Reference(filename,
                                    err.lineno,
                                    err.colno),
                     err.msg)

    # Validate basic structure
    if not isinstance(data, dict):
        mh.error(loc, "parsed json is not an object")

    for rkey in ("schema", "version", "generator", "data"):
        if rkey not in data:
            mh.error(loc, "required top-levelkey %s not present" % rkey)
        if rkey == "data":
            if not isinstance(data[rkey], list):
                mh.error(loc, "data is not an array")
        elif rkey == "version":
            if not isinstance(data[rkey], int):
                mh.error(loc, "version is not an integer")
        else:
            if not isinstance(data[rkey], str):
                mh.error(loc, "%s is not a string" % rkey)

    # Validate indicated schema
    supported_schema = {
        "lobster-req-trace" : set([3, 4]),
        "lobster-imp-trace" : set([3]),
        "lobster-act-trace" : set([3]),
    }
    if data["schema"] not in supported_schema:
        mh.error(loc, "unknown schema kind %s" % data["schema"])
    if data["version"] not in supported_schema[data["schema"]]:
        mh.error(loc,
                 "version %u for schema %s is not supported" %
                 (data["version"], data["schema"]))

    duplicate_items = []
    # Convert to items, and integrate into symbol table
    for raw in data["data"]:
        if data["schema"] == "lobster-req-trace":
            item = Requirement.from_json(level, raw, data["version"])
        elif data["schema"] == "lobster-imp-trace":
            item = Implementation.from_json(level, raw, data["version"])
        else:
            item = Activity.from_json(level, raw, data["version"])

        if source_info is not None:
            item.perform_source_checks(source_info)

        if item.tag.key() in items:
            # 'duplicate definition' errors are fatal, but the user wants to see all
            # of them. So store the affected items in a list first, and create
            # errors later.
            duplicate_items.append(item)
        else:
            items[item.tag.key()] = item

    signal_duplicate_items(mh, items, duplicate_items)


def signal_duplicate_items(
        mh: Message_Handler,
        items,
        duplicate_items: Sequence[Union[Activity, Implementation, Requirement]],
):
    """
    Report errors for duplicate items to the message handler.
    If there are any duplicate items, the last one is considered fatal.
    """
    if duplicate_items:
        for counter, item in enumerate(duplicate_items, start=1):
            mh.error(
                location=item.location,
                message=f"duplicate definition of {item.tag.key()}, "
                        f"previously defined at "
                        f"{items[item.tag.key()].location.to_string()}",
                fatal=(counter == len(duplicate_items)),
            )
