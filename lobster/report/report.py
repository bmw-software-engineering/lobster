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

import os.path
import json

import lobster.report.errors as errors


def load(mh, file_name):
    assert isinstance(mh, errors.Message_Handler)
    assert isinstance(file_name, str)

    loc = errors.Source_Reference(file_name = file_name)

    if not os.path.isfile(file_name):
        mh.error(loc, "is not a file")

    with open(file_name, "r") as fd:
        try:
            data = json.load(fd)
        except Exception as err:
            mh.error(loc, "does not contain JSON: %s" % str(err))

    if not isinstance(data, dict):
        mh.error(loc, "invalid data: top-level JSON item must be an object")

    if data.get("schema", None) not in ("lobster-report",):
        mh.error(loc,
                 "invalid data: schema %s is not supported" %
                 data.get("schema", "None"))
    else:
        schema = data["schema"].split("-", 1)[1]

    versions_supported = {
        "report" : set([1]),
    }

    version = data.get("version", None)
    if not isinstance(version, int):
        mh.error(loc,
                 "invalid data: version is not an integer")
    if version < 1:
        mh.error(loc,
                 "invalid data: version is less than 1")
    if version not in versions_supported[schema]:
        mh.error(loc,
                 "invalid data: version %u is not supported for %s,"
                 " only %s is supported"
                 % (version,
                    schema,
                    " or ".join(sorted(versions_supported[schema]))))

    if "generator" not in data or \
       not isinstance(data["generator"], str):
        mh.error(loc,
                 "invalid data: no generator string")

    if "levels" not in data or \
       not isinstance(data["levels"], list):
        mh.error(loc,
                 "invalid data: no levels list")

    if "policy" not in data or \
       not isinstance(data["policy"], dict):
        mh.error(loc,
                 "invalid data: no policy object")

    data["xref"] = {}

    for level in data["levels"]:
        for item in level["items"]:
            data["xref"][item["name"]] = item

    return data
