#!/usr/bin/env python3
#
# lobster_codebeamer - Extract codebeamer items for LOBSTER
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

# This tool is based on the codebeamer Rest API, as documented here:
# https://codebeamer.com/cb/wiki/117612
#
# There are some assumptions encoded here that are not clearly
# documented, in that items have a type and the type has a name.
#
# I could not find a better API for returning a specific list of
# items, but I believe it exists.
#
# Main limitations:
# * Item descriptions are ignored right now
# * Branches (if they exists or are possible) are ignored
# * We only ever fetch the HEAD item
# * We ignore any links to any other items
# * By-tracker + filter import is not implemented yet
#
# However you _can_ import all the items referenced from another
# lobster artefact.

import os
import sys
import argparse

from copy import copy

import requests

from lobster.items import Tracing_Tag, Requirement
from lobster.location import Codebeamer_Reference
from lobster.errors import Message_Handler, LOBSTER_Error
from lobster.io import lobster_read, lobster_write


def query_cb_single(cb_config, url):
    assert isinstance(cb_config, dict)
    assert isinstance(url, str)

    result = requests.get(url,
                          auth=(cb_config["user"],
                                cb_config["pass"]),
                          timeout=10.0)
    if result.status_code != 200:
        print("Could not fetch %s" % url)
        print("Status = %u" % result.status_code)
        print(result.text)
        sys.exit(1)

    return result.json()


def get_single_item(cb_config, item_id):
    assert isinstance(item_id, int) and item_id > 0

    url = "%s/item/%u" % (cb_config["base"],
                          item_id)
    data = query_cb_single(cb_config, url)
    return data


def get_many_items_maybe(cb_config, tracker_id, item_ids):
    assert isinstance(tracker_id, int)
    assert isinstance(item_ids, set)

    rv = []

    base_url = "%s/tracker/%u/items/or/%s" % (
        cb_config["base"],
        tracker_id,
        ";".join("id=%u" % item_id
                 for item_id in item_ids))
    page_id = 1
    while True:
        data = query_cb_single(cb_config, "%s/page/%u" % (base_url,
                                                          page_id))
        rv += data["items"]
        if len(rv) == data["total"]:
            break
        page_id += 1

    return rv


def to_lobster(cb_config, cb_item):
    assert isinstance(cb_config, dict)
    assert isinstance(cb_item, dict) and "id" in cb_item

    # This looks like it's business logic, maybe we should make this
    # configurable?

    if "type" in cb_item:
        kind = cb_item["type"].get("name", "codebeamer item")
    else:
        kind = "codebeamer item"

    if "status" in cb_item:
        status = cb_item["status"].get("name", None)
    else:
        status = None

    # TODO: Parse item text

    return Requirement(
        tag       = Tracing_Tag(namespace = "req",
                                tag       = str(cb_item["id"]),
                                version   = cb_item["version"]),
        location  = Codebeamer_Reference(cb_root = cb_config["root"],
                                         tracker = cb_item["tracker"]["id"],
                                         item    = cb_item["id"],
                                         version = cb_item["version"],
                                         name    = cb_item["name"]),
        framework = "codebeamer",
        kind      = kind,
        name      = cb_item["name"],
        text      = None,
        status    = status)


def import_tagged(mh, cb_config, items_to_import):
    assert isinstance(mh, Message_Handler)
    assert isinstance(cb_config, dict)
    assert isinstance(items_to_import, set)
    work_list = copy(items_to_import)
    rv        = []

    tracker_id = None
    while work_list:
        if tracker_id is None or len(work_list) < 3:
            target = work_list.pop()
            print("Fetching single item %u" % target)

            cb_item    = get_single_item(cb_config, target)
            l_item     = to_lobster(cb_config, cb_item)
            tracker_id = l_item.location.tracker
            rv.append(l_item)

        else:
            print("Attempting to fetch %u items from %s" %
                  (len(work_list), tracker_id))
            cb_items = get_many_items_maybe(cb_config, tracker_id, work_list)

            for cb_item in cb_items:
                l_item = to_lobster(cb_config, cb_item)
                assert tracker_id == l_item.location.tracker
                rv.append(l_item)
                work_list.remove(l_item.location.item)

            tracker_id = None

    return rv


def main():
    ap = argparse.ArgumentParser()

    modes = ap.add_mutually_exclusive_group()
    modes.add_argument("--import-tagged",
                       metavar="LOBSTER_FILE",
                       default=None)

    ap.add_argument("--cb-root", default=os.environ.get("CB_ROOT", None))
    ap.add_argument("--cb-user", default=os.environ.get("CB_USERNAME", None))
    ap.add_argument("--cb-pass", default=os.environ.get("CB_PASSWORD", None))
    ap.add_argument("--out", default=None)
    options = ap.parse_args()

    mh = Message_Handler()

    if options.cb_root is None:
        ap.error("please set CB_ROOT or use --cb-root")
    if options.cb_user is None:
        ap.error("please set CB_USERNAME or use --cb-user")
    if options.cb_pass is None:
        ap.error("please set CB_PASSWORD or use --cb-pass")

    items_to_import = set()

    if options.import_tagged:
        if not os.path.isfile(options.import_tagged):
            ap.error("%s is not a file" % options.import_tagged)
        items = {}
        try:
            lobster_read(mh       = mh,
                         filename = options.import_tagged,
                         level    = "N/A",
                         items    = items)
        except LOBSTER_Error:
            return 1
        for item in items.values():
            for tag in item.unresolved_references:
                if tag.namespace != "req":
                    continue
                try:
                    item_id = int(tag.tag, 10)
                    if item_id > 0:
                        items_to_import.add(item_id)
                    else:
                        mh.warning(item.location,
                                   "invalid codebeamer reference to %i" %
                                   item_id)
                except ValueError:
                    pass

    cb_config = {
        "root" : options.cb_root,
        "base" : "%s/cb/rest" % options.cb_root,
        "user" : options.cb_user,
        "pass" : options.cb_pass,
    }

    try:
        items = import_tagged(mh, cb_config, items_to_import)
    except LOBSTER_Error:
        return 1

    if options.out is None:
        lobster_write(sys.stdout, Requirement, "lobster_codebeamer", items)
        print()
    else:
        with open(options.out, "w", encoding="UTF-8") as fd:
            lobster_write(fd, Requirement, "lobster_codebeamer", items)

    return 0


if __name__ == "__main__":
    sys.exit(main())
