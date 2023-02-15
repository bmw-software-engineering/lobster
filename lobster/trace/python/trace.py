#!/usr/bin/env python3
#
# lobster_python - Extract Python tracing tags for LOBSTER
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
import json
import multiprocessing
import functools

from libcst.metadata import PositionProvider
import libcst as cst

LOBSTER_TRACE_PREFIX = "# lobster-trace: "
LOBSTER_JUST_PREFIX = "# lobster-exclude: "


def parse_value(val):
    if isinstance(val, cst.SimpleString):
        return val.value[1:-1]
    else:
        return str(val.value)

class Lobster_Visitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, file_name, db, options):
        super().__init__()
        assert os.path.isfile(file_name)
        assert isinstance(db, dict)
        self.scope_stack = []
        self.file_name = file_name
        self.db = db
        self.options = options
        self.current_class    = None
        self.current_function = None
        self.current_uid      = None

    def visit_ClassDef(self, node):
        self.scope_stack.append((node.name.value, node))

    def visit_FunctionDef(self, node):
        self.scope_stack.append((node.name.value, node))

        if self.current_function is not None:
            return

        starting_tags = []

        for dec in node.decorators:
            if isinstance(dec.decorator, (cst.Name, cst.Attribute)):
                continue
            else:
                assert isinstance(dec.decorator, cst.Call)
                dec_name = dec.decorator.func.value
                if dec_name != self.options["decorator"]:
                    continue
                dec_args = {arg.keyword.value: parse_value(arg.value)
                            for arg in dec.decorator.args}

            assert self.options["dec_arg_name"] in dec_args

            starting_tags.append(self.options["prefix"] +
                                 str(dec_args[self.options["dec_arg_name"]]))

        uids = []
        for s_name, s_node in self.scope_stack:
            uids.append(s_name)
            if isinstance(s_node, cst.FunctionDef):
                self.current_function = s_node
                break
            else:
                self.current_class = s_node
        assert len(uids) >= 1
        self.current_uid = "::".join(uids)

        line = self.get_metadata(PositionProvider,
                                 self.current_function).start.line

        self.db[self.current_uid] = {
            "kind"               : ("method"
                                    if self.current_class
                                    else "function"),
            "language"           : "Python",
            "source"             : {"file" : self.file_name,
                                    "line" : line},
            "tags"               : starting_tags,
            "justification"      : [],
            "justification_up"   : [],
            "justification_down" : [],
        }

    def leave_FunctionDef(self, node):
        self.scope_stack.pop()
        if node == self.current_function:
            self.current_function = None
            self.current_uid      = None

    def leave_ClassDef(self, node):
        self.scope_stack.pop()
        if node == self.current_class:
            self.current_class = None

    def visit_Comment(self, node):
        if self.current_function is None:
            return

        item = self.db[self.current_uid]

        if node.value.startswith(LOBSTER_TRACE_PREFIX):
            tag = node.value[len(LOBSTER_TRACE_PREFIX):].strip()
            item["tags"].append(tag)

        elif node.value.startswith(LOBSTER_JUST_PREFIX):
            reason = node.value[len(LOBSTER_JUST_PREFIX):].strip()
            item["justification_up"].append(reason)


def process_file(file_name, options={}):
    db = {}
    with open(file_name, "r") as fd:
        ast = cst.parse_module(fd.read())
    ast = cst.MetadataWrapper(ast)
    ast.visit(Lobster_Visitor(file_name, db, options))

    if options["exclude_untagged"]:
        return {name: db[name]
                for name in db
                if db[name]["tags"]}
    else:
        return db


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files",
                    nargs="+",
                    metavar="FILE|DIR")
    ap.add_argument("--out",
                    default=None)
    ap.add_argument("--single",
                    action="store_true",
                    default=False,
                    help="don't multi-thread")
    ap.add_argument("--decorator-tag-prefix",
                    default=None,
                    help="prefix tags from decorators with this string and a colon")
    ap.add_argument("--parse-decorator",
                    nargs=2,
                    metavar="DECORATOR_NAME ARGUMENT_NAME",
                    default=(None, None))
    ap.add_argument("--only-tagged-functions",
                    default=False,
                    action="store_true",
                    help="only trace functions with tags")

    options = ap.parse_args()

    file_list = []
    for item in options.files:
        if os.path.isfile(item):
            file_list.append(item)
        elif os.path.isdir(item):
            for path, dirs, files in os.walk(item):
                for filename in files:
                    _, ext = os.path.splitext(filename)
                    if ext == ".py":
                        file_list.append(os.path.join(path, filename))
        else:
            ap.error("%s is not a file or directory" % item)

    prefix = os.getcwd()

    db = {"schema"    : "lobster-imp-trace",
          "generator" : "lobster_python",
          "version"   : 1,
          "data"      : {}}

    context = {
        "decorator"        : options.parse_decorator[0],
        "dec_arg_name"     : options.parse_decorator[1],
        "exclude_untagged" : options.only_tagged_functions,
        "prefix"           : (options.decorator_tag_prefix + ":"
                              if options.decorator_tag_prefix
                              else ""),
    }

    fn = functools.partial(process_file, options=context)

    if options.single:
        for file_name in file_list:
            db["data"].update(fn(file_name))
    else:
        with multiprocessing.Pool() as pool:
            for fragment in pool.imap_unordered(fn, file_list):
                db["data"].update(fragment)

    if options.out:
        with open(options.out, "w") as fd:
            json.dump(db, fd, indent=4, sort_keys=True)
        print("Written output for %u items to %s" % (len(db["data"]),
                                                     options.out))
    else:
        print(json.dumps(db, indent=4, sort_keys=True))
