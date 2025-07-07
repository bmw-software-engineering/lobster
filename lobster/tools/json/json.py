#!/usr/bin/env python3
#
# lobster_json - Extract JSON tags for LOBSTER
# Copyright (C) 2023-2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
import json
from pathlib import PurePath
from pprint import pprint
from typing import Tuple, List, Set

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
        return None

    elif required:
        raise Malformed_Input("not an object", root)
    return None


def syn_test_name(file_name):
    assert isinstance(file_name, PurePath)
    if file_name.is_absolute():
        components = list(file_name.parts)[1:-1]
    else:
        components = list(file_name.parts)[:-1]
    components.append(file_name.name.replace(".json", ""))
    components = [item
                  for item in components
                  if item and item not in (".", "..")]
    return ".".join(components)


class LOBSTER_Json(LOBSTER_Per_File_Tool):
    def __init__(self):
        super().__init__(
            name        = "json",
            description = "Extract tracing data from JSON files.",
            extensions  = ["json"],
            official    = True)

    # Supported config parameters for lobster-json
    TEST_LIST = "test_list"
    NAME_ATTRIBUTE = "name_attribute"
    TAG_ATTRIBUTE = "tag_attribute"
    JUSTIFICATION_ATTRIBUTE = "justification_attribute"
    SINGLE = "single"

    @classmethod
    def get_config_keys_manual(cls):
        help_dict = super().get_config_keys_manual()
        help_dict.update(
            {
                cls.TEST_LIST: "Member name indicator resulting in a "
                               "list containing objects carrying test "
                               "data.",
                cls.NAME_ATTRIBUTE: "Member name indicator for test name.",
                cls.TAG_ATTRIBUTE: "Member name indicator for test tracing tags.",
                cls.JUSTIFICATION_ATTRIBUTE: "Member name indicator for "
                                             "justifications.",
                cls.SINGLE: "Avoid use of multiprocessing."
            }
        )
        return help_dict

    def get_mandatory_parameters(self) -> Set[str]:
        return {self.TAG_ATTRIBUTE}

    def process_commandline_and_yaml_options(
            self,
            options: argparse.Namespace,
    ) -> List[Tuple[File_Reference, str]]:
        """
        Overrides the parent class method and add fetch tool specific options from the
        yaml
        config

        Returns
        -------
        options - command-line and yaml options
        worklist - list of json files
        """
        work_list = super().process_commandline_and_yaml_options(options)
        options.test_list = self.config.get(self.TEST_LIST, '')
        options.name_attribute = self.config.get(self.NAME_ATTRIBUTE)
        options.tag_attribute = self.config.get(self.TAG_ATTRIBUTE)
        options.justification_attribute = self.config.get(self.JUSTIFICATION_ATTRIBUTE)
        options.single = self.config.get(self.SINGLE, False)
        return work_list

    def process_tool_options(
            self,
            options: argparse.Namespace,
            work_list: List[Tuple[File_Reference, str]],
    ):
        super().process_tool_options(options, work_list)
        self.schema = Activity

    @classmethod
    def process(cls, options, file_name) -> Tuple[bool, List[Activity]]:
        try:
            with open(file_name, "r", encoding="UTF-8") as fd:
                data = json.load(fd)
            data = get_item(root     = data,
                            path     = options.test_list,
                            required = True)
        except UnicodeDecodeError as decode_error:
            print("%s: File is not encoded in utf-8: %s" % (file_name, decode_error))
            return False, []
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
                    item_name = "%s.%u" % (syn_test_name(PurePath(file_name)),
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
                                            tag       = "%s:%s" %
                                            (file_name, item_name)),
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
    return LOBSTER_Json().run()
