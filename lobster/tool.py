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

import os
import sys
import argparse
import multiprocessing

from abc import ABCMeta, abstractmethod
from functools import partial
from typing import List, Sequence, Union, Tuple, Set, Dict
import yaml
from lobster.errors import Message_Handler
from lobster.location import File_Reference
from lobster.items import Requirement, Implementation, Activity
from lobster.io import lobster_write
from lobster.meta_data_tool_base import MetaDataToolBase


class SupportedCommonConfigKeys:
    """Helper class to define supported configuration keys."""
    INPUTS_FROM_FILE     = "inputs_from_file"
    TRAVERSE_BAZEL_DIRS = "traverse_bazel_dirs"
    INPUTS              = "inputs"

    @classmethod
    def get_config_keys_manual(cls) -> Dict[str, str]:
        help_dict = {
            cls.INPUTS_FROM_FILE     : "Read input files or directories from this "
                                       "file. Each non-empty line is interpreted as "
                                       "one input. Supports comments starting with #.",
            cls.TRAVERSE_BAZEL_DIRS : "Enter bazel-* directories, which are excluded "
                                      "by default.",
            cls.INPUTS              : "List of files to process or directories to "
                                      "search for relevant input files.",
        }
        return help_dict

    @abstractmethod
    def get_mandatory_parameters(self) -> Set[str]:
        """Return a set of config file parameters that are mandatory"""

    def get_formatted_help_text(self):
        help_dict = self.get_config_keys_manual()
        help_text = ''
        max_length = max(len(config_key) for config_key in help_dict)
        for config_key, help_info in help_dict.items():
            spaces = " " * (max_length - len(config_key))
            help_text += f"\n{config_key} {spaces}- {help_info}"
        return help_text

    @classmethod
    def get_config_keys_as_set(cls) -> Set[str]:
        return set(cls.get_config_keys_manual().keys())


class LOBSTER_Tool(MetaDataToolBase, SupportedCommonConfigKeys, metaclass=ABCMeta):
    def __init__(self, name, description, extensions, official):
        super().__init__(
            name=name,
            description=description,
            official=official,
        )
        assert isinstance(extensions, (list, set, frozenset, tuple))
        assert all(isinstance(extension, str)
                   for extension in extensions)

        self.extensions  = [f".{extension}" for extension in (sorted(extensions))]
        self.exclude_pat = []
        self.schema      = None
        self.mh          = Message_Handler()
        self.config      = {}

        self._argument_parser.add_argument(
            "--out",
            default = f'{self.name}.lobster',
            help    = "Write output to the given file instead of stdout."
        )
        self._argument_parser.add_argument(
            "--config",
            default=None,
            help=(f"Path to YAML file with arguments as below,"
                  f"{self.get_formatted_help_text()}"),
            required=True
        )

    def load_yaml_config(self, config_path):
        """
        Loads configuration from a YAML file.
        Parameters
        ----------
        config_path - Yaml config file path.

        Returns
        -------
        data - Returns the Yaml file contents in dictionary format.
        """
        if not config_path:
            return {}
        if not os.path.isfile(config_path):
            sys.exit(f"Error: Config file '{config_path}' not found.")
        with open(config_path, "r", encoding="UTF-8") as f:
            data = yaml.safe_load(f) or {}
        return data

    def validate_yaml_supported_config_parameters(self, config):
        """
        Function to check if the parameters mentioned in the Yaml config are
        supported by the tool in execution
        Parameters
        ----------
        data - Yaml config file contents

        Returns
        -------
        Nothing
        """
        if config:
            supported_keys = self.get_config_keys_as_set()
            unsupported_keys = set(config.keys()) - supported_keys
            if unsupported_keys:
                raise KeyError(
                    f"Unsupported config keys: {', '.join(unsupported_keys)}. "
                    f"Supported keys are: {', '.join(supported_keys)}."
                )

    def check_mandatory_config_parameters(self, config):
        """
        Function to check if the mandatory parameters are provided in the config file
        Parameters
        ----------
        data - Yaml config file contents

        Returns
        -------
        Nothing
        """
        if self.get_mandatory_parameters():
            mandatory_parameters = self.get_mandatory_parameters() - set(config.keys())
            if mandatory_parameters:
                sys.exit(f"Required mandatory parameters missing - "
                         f"{','.join(mandatory_parameters)}")

    def process_commandline_and_yaml_options(
            self,
            options: argparse.Namespace,
    ) -> List[Tuple[File_Reference, str]]:
        """Processes all command line options"""

        self.config = self.load_yaml_config(options.config)
        self.validate_yaml_supported_config_parameters(self.config)
        self.check_mandatory_config_parameters(self.config)
        options.inputs_from_file = self.config.get(self.INPUTS_FROM_FILE, None)
        options.inputs = self.config.get(self.INPUTS, [])
        options.traverse_bazel_dirs = self.config.get(self.TRAVERSE_BAZEL_DIRS, False)
        work_list = self.process_common_options(options)
        self.process_tool_options(options, work_list)
        return work_list

    def process_common_options(
            self,
            options: argparse.Namespace,
    ) -> List[Tuple[File_Reference, str]]:
        """Generates the exact list of files to work on later. The list is sorted
        alphabetically."""
        # Sanity check output
        if options.out and \
           os.path.exists(options.out) and \
           not os.path.isfile(options.out):
            self._argument_parser.error(
                f"output {options.out} already exists and is not a file",
            )

        # Assemble input requests
        inputs = []
        if options.inputs:
            inputs += [(File_Reference("<config>"), item)
                       for item in options.inputs]
        if options.inputs_from_file:
            if not os.path.isfile(options.inputs_from_file):
                self._argument_parser.error(f"cannot open {options.inputs_from_file}")
            with open(options.inputs_from_file, "r", encoding="UTF-8") as fd:
                for line_no, raw_line in enumerate(fd, 1):
                    line = raw_line.split("#", 1)[0].strip()
                    if not line:
                        continue
                    inputs.append((File_Reference(options.inputs_from_file,
                                                  line_no),
                                   line))
        if not options.inputs and not options.inputs_from_file:
            inputs.append((File_Reference("<config>"), "."))
        # Sanity check and search directories
        work_list = []
        ok        = True
        for location, item in inputs:
            if os.path.isfile(item):
                if os.path.splitext(item)[1] not in self.extensions:
                    self.mh.warning(location,
                                    f"not a {' or '.join(self.extensions)} file")
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
                              f"{item} is not a file or directory",
                              fatal = False)
                ok = False

        if not ok:
            sys.exit(1)

        work_list.sort()

        return work_list

    def write_output(
            self,
            options: argparse.Namespace,
            items: List[Union[Activity, Implementation, Requirement]],
    ):
        assert isinstance(options, argparse.Namespace)
        assert isinstance(items, list)
        assert all(isinstance(item, (Requirement,
                                     Implementation,
                                     Activity))
                   for item in items)

        if options.out:
            with open(options.out, "w", encoding="UTF-8") as fd:
                lobster_write(fd, self.schema, self.name, items)
            print(f"{self.name}: wrote {len(items)} items to {options.out}")
        else:
            lobster_write(sys.stdout, self.schema, self.name, items)

    @abstractmethod
    def process_tool_options(
            self,
            options: argparse.Namespace,
            work_list: List[Tuple[File_Reference, str]],
    ):
        assert isinstance(options, argparse.Namespace)
        assert isinstance(work_list, list)


class LOBSTER_Per_File_Tool(LOBSTER_Tool):
    def __init__(self, name, description, extensions, official=False):
        super().__init__(name, description, extensions, official)

    @classmethod
    @abstractmethod
    def process(
            cls,
            options,
            file_name,
    ) -> Tuple[bool, Sequence[Union[Activity, Implementation, Requirement]]]:
        pass

    def _run_impl(self, options: argparse.Namespace) -> int:
        work_list = self.process_commandline_and_yaml_options(options)

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
                pool.close()
                pool.join()

        if ok:
            self.write_output(options, items)
        else:
            print(f"{self.name}: aborting due to earlier errors")

        return int(not ok)
