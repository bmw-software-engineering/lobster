#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
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

import os
import re
import sys
import argparse

from copy import copy
from typing import Tuple, List, Set

from trlc.trlc import Source_Manager
from trlc.lexer import TRLC_Lexer, Token
from trlc.parser import Parser_Base
from trlc.errors import Message_Handler, TRLC_Error
from trlc import ast

from lobster.tool import LOBSTER_Tool
from lobster.items import Tracing_Tag, Requirement
from lobster.location import File_Reference
from lobster.io import lobster_write


class Config_Parser(Parser_Base):
    def __init__(self, mh, file_name, stab):
        assert isinstance(mh, Message_Handler)
        assert os.path.isfile(file_name)
        assert isinstance(stab, ast.Symbol_Table)
        super().__init__(mh        = mh,
                         lexer     = TRLC_Lexer(mh, file_name),
                         eoc_name  = "end of file",
                         token_map = Token.KIND,
                         keywords  = TRLC_Lexer.KEYWORDS)
        self.stab       = stab
        self.tree       = {}
        self.entries    = {}
        self.config     = {}
        self.to_string  = {}

        # Construct type hierarchy
        for n_pkg in self.stab.values(ast.Package):
            for n_typ in n_pkg.symbols.values(ast.Record_Type):
                if n_typ not in self.tree:
                    self.tree[n_typ] = set()
                if n_typ.parent:
                    if n_typ.parent not in self.tree:
                        self.tree[n_typ.parent] = set([n_typ])
                    else:
                        self.tree[n_typ.parent].add(n_typ)

    def generate_lobster_object(self, n_obj):
        assert isinstance(n_obj, ast.Record_Object)
        assert n_obj.n_typ in self.config

        config = self.config[n_obj.n_typ]

        if not config["trace"]:
            return None

        item_tag = Tracing_Tag(namespace = "req",
                               tag       = n_obj.fully_qualified_name(),
                               version   = None)

        item_loc = File_Reference(filename = n_obj.location.file_name,
                                  line     = n_obj.location.line_no,
                                  column   = n_obj.location.col_no)

        item_data = n_obj.to_python_dict()
        item_text = None

        if len(config["description_fields"]) == 1:
            item_text = item_data[config["description_fields"][0].name]
        elif len(config["description_fields"]) > 1:
            item_text = "\n\n".join("%s: %s" % (field.name,
                                                item_data[field.name])
                                    for field in config["description_fields"]
                                    if item_data[field.name])

        rv = Requirement(tag       = item_tag,
                         location  = item_loc,
                         framework = "TRLC",
                         kind      = n_obj.n_typ.name,
                         name      = n_obj.fully_qualified_name(),
                         text      = item_text if item_text else None)

        for tag_namespace, tag_field in config["tag_fields"]:
            if item_data[tag_field.name] is None:
                continue
            elif isinstance(tag_field.n_typ, ast.Array_Type):
                for element in item_data[tag_field.name]:
                    text = self.generate_text(tag_field.n_typ.element_type,
                                              element)
                    tag = Tracing_Tag.from_text(tag_namespace, text)
                    rv.add_tracing_target(tag)
            else:
                text = self.generate_text(tag_field.n_typ,
                                          item_data[tag_field.name])
                tag = Tracing_Tag.from_text(tag_namespace, text)
                rv.add_tracing_target(tag)

        for lst, name in ((rv.just_up, "just_up"),
                          (rv.just_down, "just_down"),
                          (rv.just_global, "just_global")):
            for just_field in config[name + "_fields"]:
                if item_data[just_field.name] is None:
                    continue
                elif isinstance(just_field.n_typ, ast.Array_Type):
                    for element in item_data[just_field.name]:
                        text = self.generate_text(
                            just_field.n_typ.element_type,
                            element)
                        lst.append(text)
                else:
                    text = self.generate_text(just_field.n_typ,
                                              item_data[just_field.name])
                    lst.append(text)

        return rv

    def generate_text(self, n_typ, value):
        assert isinstance(n_typ, ast.Type)
        assert not isinstance(n_typ, ast.Array_Type)

        if isinstance(n_typ, ast.Tuple_Type):
            if n_typ not in self.to_string:
                self.lexer.mh.error(n_typ.location,
                                    "please define a to_string function for"
                                    " this type in the lobster-trlc"
                                    " configuration file")

            # We have functions, so we attempt to apply until we get
            # one that works, in order.
            for function_seq in self.to_string[n_typ]:
                rv = ""
                valid = True
                for kind, func in function_seq:
                    if kind == "text":
                        assert isinstance(func, str)
                        rv += func
                    elif kind == "field":
                        assert isinstance(func, ast.Composite_Component)
                        if value[func.name] is None:
                            valid = False
                            break
                        rv += self.generate_text(func.n_typ,
                                                 value[func.name])
                if valid:
                    return rv

            self.lexer.mh.error(n_typ.location,
                                "please define a to_string function that"
                                " can render %s" % value)

        else:
            return str(value)

    def parse_config_file(self):
        # First parse config file
        while self.nt:
            self.parse_directive()
        self.match_eof()

        # Then build the type hierarchy configuration
        for n_typ in self.tree:
            if n_typ.parent:
                continue
            context = {
                "trace"              : False,
                "description_fields" : [],
                "tag_fields"         : [],
                "just_up_fields"     : [],
                "just_down_fields"   : [],
                "just_global_fields" : [],
            }

            self.build_config(n_typ, context)

    def build_config(self, n_typ, config):
        assert isinstance(n_typ, ast.Record_Type)
        assert isinstance(config, dict)

        self.config[n_typ] = config
        if n_typ in self.entries:
            self.config[n_typ]["trace"] = True
            for field in ("description",
                          "just_up",
                          "just_down",
                          "just_global"):
                ctx_name = "%s_fields" % field
                for new_field in self.entries[n_typ][ctx_name]:
                    if new_field not in self.config[n_typ][ctx_name]:
                        self.config[n_typ][ctx_name].append(new_field)
            for tag_namespace, tag_field in self.entries[n_typ]["tag_fields"]:
                self.config[n_typ]["tag_fields"].append((tag_namespace,
                                                         tag_field))

        for n_extension in self.tree[n_typ]:
            new_context = {
                "trace" : self.config[n_typ]["trace"],

                "description_fields" :
                copy(self.config[n_typ]["description_fields"]),

                "just_up_fields" :
                copy(self.config[n_typ]["just_up_fields"]),

                "just_down_fields" :
                copy(self.config[n_typ]["just_down_fields"]),

                "just_global_fields" :
                copy(self.config[n_typ]["just_global_fields"]),

                "tag_fields" :
                copy(self.config[n_typ]["tag_fields"]),
            }
            self.build_config(n_extension, new_context)

    def parse_record_type(self, n_typ):
        assert isinstance(n_typ, ast.Record_Type)

        if n_typ in self.entries:
            self.lexer.mh.error(self.ct.location,
                                "duplicate configuration block")
        else:
            self.entries[n_typ] = {
                "description_fields" : [],
                "tag_fields"         : [],
                "just_up_fields"     : [],
                "just_down_fields"   : [],
                "just_global_fields" : [],
            }

        self.match("C_BRA")

        while self.peek("IDENTIFIER"):
            self.match("IDENTIFIER")
            if self.ct.value in ("description",
                                 "just_up",
                                 "just_down",
                                 "just_global"):
                field = self.ct.value
                self.match("ASSIGN")
                self.match("IDENTIFIER")
                n_comp = n_typ.components.lookup(
                    mh                = self.lexer.mh,
                    referencing_token = self.ct,
                    required_subclass = ast.Composite_Component)
                self.entries[n_typ]["%s_fields" % field].append(n_comp)
            elif self.ct.value == "tags":
                if self.peek("STRING"):
                    self.match("STRING")
                    tag_namespace = self.ct.value
                else:
                    tag_namespace = "req"
                self.match("ASSIGN")
                self.match("IDENTIFIER")
                n_comp = n_typ.components.lookup(
                    mh                = self.lexer.mh,
                    referencing_token = self.ct,
                    required_subclass = ast.Composite_Component)
                self.entries[n_typ]["tag_fields"].append((tag_namespace,
                                                          n_comp))
            else:
                self.lexer.mh.error(
                    self.ct.location,
                    "expected description|tags|just_up|just_down|just_global")

        self.match("C_KET")

    def parse_text_generator(self, n_typ):
        assert isinstance(n_typ, ast.Composite_Type)

        function = []

        if self.peek("STRING"):
            self.match("STRING")
            cpos = 0
            function = []
            for match in re.finditer(r"\$\([a-z][a-z0-9_]*\)",
                                     self.ct.value):
                if match.span()[0] > cpos:
                    function.append(("text",
                                     self.ct.value[cpos:match.span()[0]]))
                n_comp = n_typ.components.lookup_direct(
                    mh                = self.lexer.mh,
                    name              = match.group(0)[2:-1],
                    error_location    = self.ct.location,
                    required_subclass = ast.Composite_Component)
                function.append(("field", n_comp))
                cpos = match.span()[1]
            if cpos < len(self.ct.value):
                function.append(("text",
                                 self.ct.value[cpos:]))
            # for kind, value in function:
            #     if kind == "text" and not re.match("^[a-zA-Z_0-9@]+$",
            #                                        value):
            #         self.lexer.mh.error(
            #             self.ct.location,
            #             "text segment '%s' can only contain letters,"
            #             " numbers, underscores, or @" % value)

        else:
            self.match("IDENTIFIER")
            n_comp = n_typ.components.lookup(
                mh                = self.lexer.mh,
                referencing_token = self.ct,
                required_subclass = ast.Composite_Component)
            function.append(("field", n_comp))

        return function

    def parse_tuple_type(self, n_typ):
        assert isinstance(n_typ, ast.Tuple_Type)

        if n_typ in self.to_string:
            self.lexer.mh.error(self.ct.location,
                                "duplicate configuration block")
        else:
            self.to_string[n_typ] = []

        self.match("C_BRA")

        while self.peek("IDENTIFIER"):
            self.match("IDENTIFIER")
            if self.ct.value == "to_string":
                self.match("ASSIGN")
                self.to_string[n_typ].append(
                    self.parse_text_generator(n_typ))
            else:
                self.lexer.mh.error(self.ct.location,
                                    "expected to_string")

        self.match("C_KET")

    def parse_directive(self):
        self.match("IDENTIFIER")
        n_pkg = self.stab.lookup(mh                = self.lexer.mh,
                                 referencing_token = self.ct,
                                 required_subclass = ast.Package)
        self.match("DOT")
        self.match("IDENTIFIER")
        n_typ = n_pkg.symbols.lookup(mh                = self.lexer.mh,
                                     referencing_token = self.ct,
                                     required_subclass = ast.Composite_Type)
        if isinstance(n_typ, ast.Record_Type):
            self.parse_record_type(n_typ)
        else:
            self.parse_tuple_type(n_typ)


class LOBSTER_Trlc(LOBSTER_Tool):
    def __init__(self):
        super().__init__(
            name        = "trlc",
            description = "Extract tracing data from rsl and trlc files.",
            extensions  = ["rsl", "trlc"],
            official    = True,
        )

        for action in self._argument_parser._actions:
            if action.dest == 'config':
                action.required = False

    # Supported config parameters for lobster-trlc
    TRLC_CONFIG_FILE = "trlc_config_file"

    @classmethod
    def get_config_keys_manual(cls):
        help_dict = super().get_config_keys_manual()
        help_dict.update(
            {
                cls.TRLC_CONFIG_FILE: "Name of lobster-trlc config file, "
                                      "by default lobster-trlc.conf"
            }
        )
        return help_dict

    def get_mandatory_parameters(self) -> Set[str]:
        """As of now lobster-trlc don't have any mandatory parameters"""
        return set()

    def process_commandline_and_yaml_options(
            self,
            options: argparse.Namespace,
    ) -> List[Tuple[File_Reference, str]]:
        """
        Overrides the parent class method and add fetch tool specific options from the
        yaml config

        Returns
        -------
        options - command-line and yaml options
        worklist - list of trlc and rsl files
        """

        work_list = super().process_commandline_and_yaml_options(options)
        options.trlc_config_file = self.config.get(self.TRLC_CONFIG_FILE,
                                                   "lobster-trlc.conf")
        return work_list

    def process_tool_options(
            self,
            options: argparse.Namespace,
            work_list: List[Tuple[File_Reference, str]],
    ):
        super().process_tool_options(options, work_list)
        self.schema = Requirement

    def _run_impl(self, options: argparse.Namespace):
        trlc_mh = Message_Handler()
        sm = Source_Manager(trlc_mh)
        work_list = self.process_commandline_and_yaml_options(options)
        if not os.path.isfile(options.trlc_config_file):
            sys.exit("lobster-trlc: cannot open config file '%s'" %
                     options.trlc_config_file)

        if os.path.exists(options.out) and not os.path.isfile(options.out):
            sys.exit("lobster-trlc: output file '%s' exists and is not a file"
                     % options.out)

        ok = True
        for item in work_list:
            if os.path.isfile(item):
                try:
                    sm.register_file(item)
                except TRLC_Error:
                    ok = False
            elif os.path.isdir(item):
                try:
                    sm.register_directory(item)
                except TRLC_Error:
                    ok = False
            else:
                print("lobster-trlc: neither a file or directory: '%s'" %
                      item)
                ok = False

        if ok:
            stab = sm.process()
        # pylint: disable=possibly-used-before-assignment
        if not ok or stab is None:
            print("lobster-trlc: aborting due to earlier error")
            return 1

        config_parser = Config_Parser(trlc_mh, options.trlc_config_file, stab)
        try:
            config_parser.parse_config_file()
        except TRLC_Error:
            print("lobster-trlc: aborting due to error in"
                  " configuration file '%s'" % options.trlc_config_file)
            return 1

        items = []
        for n_obj in stab.iter_record_objects():
            try:
                item = config_parser.generate_lobster_object(n_obj)
                if item:
                    items.append(item)
            except TRLC_Error:
                ok = False

        if not ok:
            print("lobster-trlc: aborting due to error during extraction")
            return 1

        with open(options.out, "w", encoding="UTF-8") as fd:
            # lobster-trace: trlc_req.Output_File
            lobster_write(fd=fd,
                          kind=Requirement,
                          generator="lobster-trlc",
                          items=items)
        print("lobster-trlc: successfully wrote %u items to %s" %
              (len(items), options.out))
        return 0


def main():
    return LOBSTER_Trlc().run()
