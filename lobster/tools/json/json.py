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
import os.path
import json
from pprint import pprint

from lobster.tool import LOBSTER_Per_File_Tool
from lobster.items import Tracing_Tag, Activity
from lobster.location import File_Reference


class Malformed_Input(Exception):
    def __init__(self, msg, data):
        super().__init__(msg)
        self.msg  = msg
        self.data = data


def get_item(root, path, required):
    assert isinstance(path, str)
    assert isinstance(required, bool)

    if path == "":
        return root

    if "." in path:
        field, tail = path.split(".", 1)
    else:
        field = path
        tail  = ""

    if isinstance(root, dict):
        if field in root:
            return get_item(root[field], tail, required)
        elif required:
            raise Malformed_Input("object does not contain %s" % field,
                                  root)
        else:
            return None

    elif required:
        raise Malformed_Input("not an object", root)

    else:
        return None


def syn_test_name(file_name):
    components = []
    head = os.path.dirname(file_name)
    while True:
        head, tail = os.path.split(head)
        components = [tail] + components
        if not head:
            break
    components.append(os.path.basename(file_name).replace(".json", ""))
    components = [item
                  for item in components
                  if item and item != "."]
    return ".".join(components)


class LOBSTER_Json(LOBSTER_Per_File_Tool):
    def __init__(self):
        super().__init__(
            name        = "json",
            description = "Extract tracing data from JSON files.",
            extensions  = ["json"],
            official    = True)
        self.add_argument("--test-list",
                          default = "",
                          help    = ("Member name indicator resulting in a"
                                     " list containing objects carrying test"
                                     " data."))
        self.add_argument("--name-attribute",
                          default = None,
                          help    = "Member name indicator for test name.")
        self.add_argument("--tag-attribute",
                          default  = None,
                          required = True,
                          help     = ("Member name indicator for test "
                                      " tracing tags."))
        self.add_argument("--justification-attribute",
                          default  = None,
                          help     = ("Member name indicator for "
                                      " justifications."))

    def process_tool_options(self, options, work_list):
        self.schema = Activity
        return True

    @classmethod
    def process(cls, options, file_name):
        with open(file_name, "r", encoding="UTF-8") as fd:
            data = json.load(fd)

        # First we follow the test-list items to get the actual data
        # we're interested in.
        try:
            data = get_item(root     = data,
                            path     = options.test_list,
                            required = True)
        except Malformed_Input as err:
            pprint(err.data)
            print("%s: malformed input: %s" % (file_name, err.msg))
            return False, []

        # Ensure we actually have a list now
        if not isinstance(data, list):
            data = [data]

        # Convert individual items
        items = []
        ok    = True
        for item_id, item in enumerate(data, 1):
            try:
                if options.name_attribute:
                    item_name = get_item(root     = item,
                                         path     = options.name_attribute,
                                         required = True)
                else:
                    item_name = "%s.%u" % (syn_test_name(file_name),
                                           item_id)
                if not isinstance(item_name, str):
                    raise Malformed_Input("name is not a string",
                                          item_name)

                item_tags = get_item(root     = item,
                                     path     = options.tag_attribute,
                                     required = False)
                if isinstance(item_tags, list):
                    pass
                elif isinstance(item_tags, str):
                    item_tags = [item_tags]
                elif item_tags is None:
                    item_tags = []
                else:
                    raise Malformed_Input("tags are not a string or list",
                                          item_name)

                if options.justification_attribute:
                    item_just = get_item(
                        root     = item,
                        path     = options.justification_attribute,
                        required = False)
                else:
                    item_just = []
                if isinstance(item_just, list):
                    pass
                elif isinstance(item_just, str):
                    item_just = [item_just]
                elif item_just is None:
                    item_just = []
                else:
                    raise Malformed_Input("justification is not a string"
                                          " or list",
                                          item_just)

                l_item = Activity(
                    tag       = Tracing_Tag(namespace = "json",
                                            tag       = item_name),
                    location  = File_Reference(file_name),
                    framework = "JSON",
                    kind      = "Test Vector")
                for tag in item_tags:
                    l_item.add_tracing_target(
                        Tracing_Tag(namespace = "req",
                                    tag       = tag))
                for just_up in item_just:
                    l_item.just_up.append(just_up)

                items.append(l_item)
            except Malformed_Input as err:
                pprint(err.data)
                print("%s: malformed input: %s" % (file_name, err.msg))
                ok = False

        return ok, items


def main():
    tool = LOBSTER_Json()
    return tool.execute()


if __name__ == "__main__":
    sys.exit(main())
