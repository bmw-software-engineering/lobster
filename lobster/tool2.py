# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

from dataclasses import dataclass
import os
import sys
import re
import argparse
import multiprocessing

from abc import ABCMeta, abstractmethod
from functools import partial
from typing import Iterable, List, Optional, Sequence, Type, Union, Tuple, Set, Dict
import yaml
from lobster.errors import Message_Handler
from lobster.location import File_Reference
from lobster.items import Requirement, Implementation, Activity
from lobster.io import lobster_write
from lobster.meta_data_tool_base import MetaDataToolBase


@dataclass
class Config:
    inputs: str
    inputs_from_file: str
    traverse_bazel_dirs: str
    extensions: List[str]
    exclude_pattern: List[re.Pattern]


class LOBSTER_Tool(MetaDataToolBase, metaclass=ABCMeta):
    def __init__(self, name: str, description: str, extensions: Iterable[str], official: bool):
        super().__init__(
            name=name,
            description=description,
            official=official,
        )
        self._extensions = [f".{extension}" for extension in (sorted(extensions))]
        self._exclude_pattern = []
        self._mh = Message_Handler()
        self._config = None

        self._argument_parser.add_argument(
            "--out",
            default=f'{self.name}.lobster',
            help="Write output to the given file instead of stdout."
        )
        self._argument_parser.add_argument(
            "--config",
            default=None,
            help="Path to configuration file",
            required=True
        )
    
    @staticmethod
    def _get_all_inputs(options: Config) -> List[str]:
        inputs = []
        if options.inputs:
            inputs.extend(options.inputs)
        if options.inputs_from_file:
            with open(options.inputs_from_file, "r", encoding="UTF-8") as fd:
                for raw_line in fd:
                    line = raw_line.split("#", 1)[0].strip()
                    if line:
                        inputs.append(line)
        return inputs

    def _create_worklist(
            self,
            options: Config,
    ) -> List[Tuple[File_Reference, str]]:
        """Generates the exact list of files to work on later."""
        inputs = self._get_all_inputs(options)
        work_list = []
        for item in inputs:
            if os.path.isfile(item):
                # FIXME: if file has no extension, then this raises an error!
                if os.path.splitext(item)[1] not in options.extensions:
                    raise ValueError(
                        f"File {item} does not have a valid extension. "
                        f"Expected one of {options.extensions}."
                    )
                work_list.append(item)

            elif os.path.isdir(item):
                for path, dirs, files in os.walk(item):
                    for n, dir_name in enumerate(dirs):
                        keep = True
                        for pattern in options.exclude_pattern:
                            if pattern.match(dir_name):
                                keep = False
                                break
                        if not keep:
                            del dirs[n]

                    for file_name in files:
                        # FIXME: if file has no extension, then this raises an error!
                        if os.path.splitext(file_name)[1] in options.extensions:
                            work_list.append(os.path.join(path, file_name))

            else:
                raise ValueError(f"{item} is not a file or directory")

        return work_list

    def write_output(
            self,
            schema: Union[Type[Requirement], Type[Implementation], Type[Activity]],
            options: argparse.Namespace,
            items: List[Union[Activity, Implementation, Requirement]],
    ):
        if not all(isinstance(item, (Requirement, Implementation, Activity))
                   for item in items):
            raise ValueError(
                f"Expected all items to be of type Requirement, Implementation, or Activity, "
                f"but got {set(type(item) for item in items)}"
            )

        if options.out:
            with open(options.out, "w", encoding="UTF-8") as fd:
                lobster_write(fd, schema, self.name, items)
            print(f"{self.name}: wrote {len(items)} items to {options.out}")
        else:
            lobster_write(sys.stdout, schema, self.name, items)


class LOBSTER_Per_File_Tool(LOBSTER_Tool):
    def __init__(self, name, description, extensions, official=False):
        super().__init__(name, description, extensions, official)

    @classmethod
    @abstractmethod
    def process(
            cls,
            options: Config,
            file_name: str,
    ) -> Tuple[bool, Sequence[Union[Activity, Implementation, Requirement]]]:
        pass

    def _run_impl(self, options: argparse.Namespace) -> int:
        config = self._load_config(options.config)
        work_list = self._create_worklist(config)

        items = []
        pfun  = partial(self.process, config)

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
