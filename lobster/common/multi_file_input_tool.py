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

import os

from abc import ABCMeta
from typing import Iterable, List, Optional, Type, Union
from lobster.common.errors import Message_Handler
from lobster.common.items import Requirement, Implementation, Activity
from lobster.common.io import lobster_write
from lobster.common.meta_data_tool_base import MetaDataToolBase
from lobster.common.tool2_config import Config
from lobster.common.file_collector import FileCollector


def read_commented_file(file: str) -> List[str]:
    """Reads lines from a file, ignoring comments and empty lines.
       Returns all lines (without comments) as a list of strings.
    """
    # lobster-trace: req.Lines_In_Inputs_File
    with open(file, "r", encoding="UTF-8") as fd:
        return select_non_comment_parts(fd.readlines())


def select_non_comment_parts(text_list: Iterable[str]) -> List[str]:
    """Selects non-comment parts from a list of strings.

       Returns the input list where each entry is stripped of comments, as well as
       leading and trailing whitespace, and empty lines are removed.
    """
    return list(
        filter(
            None,
            [line.split("#", 1)[0].strip() for line in text_list],
        ),
    )


def combine_all_inputs(
    config: Config,
    dir_or_files: Optional[List[str]],
) -> List[str]:
    """Combines all input sources into a single list."""
    inputs = []
    if config.inputs:
        inputs.extend(config.inputs)
    if config.inputs_from_file:
        inputs.extend(read_commented_file(config.inputs_from_file))
    if dir_or_files:
        inputs.extend(dir_or_files)
    return inputs


def create_worklist(
        config: Config,
        dir_or_files: Optional[List[str]],
) -> List[str]:
    """Generates the exact list of files to work on. Directories are iterated
       recursively and their files are collected, if they match the extensions.
       Subdirectories are iterated if they do not match the exclude patterns.
    """
    inputs = combine_all_inputs(config, dir_or_files)
    file_collector = FileCollector(config.extensions, config.exclude_patterns)
    for item in inputs:
        if os.path.isfile(item):
            file_collector.add_file(item, throw_on_mismatch=True)
        elif os.path.isdir(item):
            file_collector.add_dir_recursively(item)
        else:
            raise ValueError(f"{item} is not a file or directory")
    return file_collector.files


class MultiFileInputTool(MetaDataToolBase, metaclass=ABCMeta):
    """This class serves as base class for tools that process multiple input files."""

    def __init__(
            self,
            name: str,
            description: str,
            extensions: Iterable[str],
            official: bool,
    ):
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
            help=f"Write output to the given file (default: {self.name}.lobster)",
        )
        self._argument_parser.add_argument(
            "--config",
            default=None,
            help="Path to configuration file",
            required=True
        )
        self._argument_parser.add_argument(
            "dir_or_files",
            nargs="*",
            metavar="DIR|FILE",
            help="Input directories or files"
        )

    def _write_output(
            self,
            schema: Union[Type[Requirement], Type[Implementation], Type[Activity]],
            out_file: str,
            items: List[Union[Activity, Implementation, Requirement]],
    ):
        with open(out_file, "w", encoding="UTF-8") as fd:
            lobster_write(fd, schema, self.name, items)
        print(f"{self.name}: wrote {len(items)} items to {out_file}")
