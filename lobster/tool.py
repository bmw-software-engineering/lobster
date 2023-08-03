#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
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

import os
import sys
import argparse
import multiprocessing

from abc import ABCMeta, abstractmethod
from functools import partial

from lobster.version import FULL_NAME
from lobster.errors import Message_Handler
from lobster.location import File_Reference
from lobster.items import Requirement, Implementation, Activity
from lobster.io import lobster_write

BUG_URL = "https://github.com/bmw-software-engineering/lobster/issues"


class LOBSTER_Tool(metaclass=ABCMeta):
    def __init__(self, name, description, extensions, official):
        assert isinstance(name, str)
        assert isinstance(description, str)
        assert isinstance(extensions, (list, set, frozenset, tuple))
        assert all(isinstance(extension, str)
                   for extension in extensions)
        assert isinstance(official, bool)

        self.name        = "lobster-%s" % name
        self.description = description
        self.extensions  = [".%s" % extension
                            for extension in sorted(extensions)]
        self.exclude_pat = []
        self.schema      = None
        self.mh          = Message_Handler()

        self.ap = argparse.ArgumentParser(
            prog         = self.name,
            description  = description,
            epilog       = ("Part of %s, licensed under the AGPLv3."
                            " Please report bugs to %s." %
                            (FULL_NAME, BUG_URL)
                            if official else None),
            allow_abbrev = False)

        self.g_common = self.ap.add_argument_group("common options")
        self.g_debug  = self.ap.add_argument_group("debug options")
        self.g_tool   = self.ap.add_argument_group("tool specific options")

        self.g_common.add_argument(
            "--out",
            default = None,
            help    = "Write output to given file instead of stdout.")

        self.g_common.add_argument(
            "--inputs-from-file",
            metavar = "FILE",
            default = None,
            help    = ("Read input files or directories from this file."
                       " Each non-empty line is interpreted as one input."
                       " Supports comments starting with #."))

        self.g_common.add_argument(
            "inputs",
            default = None,
            nargs   = "*",
            metavar = "FILE_OR_DIR",
            help    = ("List of files to process or directories to search"
                       " for relevant input files."))

        self.g_common.add_argument(
            "--traverse-bazel-dirs",
            default = False,
            action  = "store_true",
            help    = ("Enter bazel-* directories, which are"
                       " excluded by default."))

        self.add_argument = self.g_tool.add_argument

    def process_commandline_options(self):
        options = self.ap.parse_args()

        # Sanity check output
        if options.out and \
           os.path.exists(options.out) and \
           not os.path.isfile(options.out):
            self.ap.error("output %s already exists and is not a file" %
                          options.out)

        # Assemble input requests
        inputs = []
        if options.inputs:
            inputs += [(File_Reference("<cmdline>"), item)
                       for item in options.inputs]
        if options.inputs_from_file:
            if not os.path.isfile(options.inputs_from_file):
                self.ap.error("cannot open %s" % options.inputs_from_file)
            with open(options.inputs_from_file, "r", encoding="UTF-8") as fd:
                for line_no, raw_line in enumerate(fd, 1):
                    line = raw_line.split("#", 1)[0].strip()
                    if not line:
                        continue
                    inputs.append((File_Reference(options.inputs_from_file,
                                                  line_no),
                                   line))
        if not options.inputs and not options.inputs_from_file:
            inputs.append((File_Reference("<cmdline>"), "."))

        # Sanity check and search directories
        work_list = []
        ok        = True
        for location, item in inputs:
            if os.path.isfile(item):
                if os.path.splitext(item)[1] not in self.extensions:
                    self.mh.warning(location,
                                    "not a %s file" %
                                    " or ".join(self.extensions))
                work_list.append(item)

            elif os.path.isdir(item):
                for path, dirs, files in os.walk(item):
                    for n, dir_name in reversed(list(enumerate(dirs))):
                        keep = True
                        for pattern in self.exclude_pat:
                            if pattern.match(dir_name):
                                keep = False
                                break
                        if not keep:
                            del dirs[n]

                    for file_name in files:
                        if os.path.splitext(file_name)[1] in self.extensions:
                            work_list.append(os.path.join(path, file_name))

            else:
                self.mh.error(location,
                              "%s is not a file or directory" % item,
                              fatal = False)
                ok = False

        if not ok:
            sys.exit(1)

        work_list.sort()

        self.process_tool_options(options, work_list)

        return options, work_list

    def write_output(self, ok, options, items):
        assert isinstance(ok, bool)
        assert isinstance(options, argparse.Namespace)
        assert isinstance(items, list)
        assert all(isinstance(item, (Requirement,
                                     Implementation,
                                     Activity))
                   for item in items)

        if ok:
            if options.out:
                with open(options.out, "w", encoding="UTF-8") as fd:
                    lobster_write(fd, self.schema, self.name, items)
                print("%s: wrote %u items to %s" % (self.name,
                                                    len(items),
                                                    options.out))
            else:
                lobster_write(sys.stdout, self.schema, self.name, items)
            return 0

        else:
            print("%s: aborting due to earlier errors" % self.name)
            return 1

    @abstractmethod
    def process_tool_options(self, options, work_list):
        assert isinstance(options, argparse.Namespace)
        assert isinstance(work_list, list)

    @abstractmethod
    def execute(self):
        pass


class LOBSTER_Per_File_Tool(LOBSTER_Tool):
    def __init__(self, name, description, extensions, official=False):
        super().__init__(name, description, extensions, official)

        self.g_debug.add_argument(
            "--single",
            default = False,
            action  = "store_true",
            help    = "Avoid use of multiprocessing.")

    @classmethod
    @abstractmethod
    def process(cls, options, file_name):
        return True, []

    def execute(self):
        options, work_list = self.process_commandline_options()

        ok    = True
        items = []
        pfun  = partial(self.process, options)
        if options.single:
            for file_name in work_list:
                new_ok, new_items = pfun(file_name)
                ok    &= new_ok
                items += new_items
        else:
            with multiprocessing.Pool() as pool:
                for new_ok, new_items in pool.imap(pfun, work_list, 4):
                    ok    &= new_ok
                    items += new_items

        return self.write_output(ok, options, items)
