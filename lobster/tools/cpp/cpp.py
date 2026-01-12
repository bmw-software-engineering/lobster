#!/usr/bin/env python3
#
# lobster_cpp - Extract C/C++ tracing tags for LOBSTER
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

from argparse import Namespace
import os.path
import subprocess
import re
from typing import Optional, Sequence

from lobster.common.items import Tracing_Tag, Implementation, Item, KindTypes
from lobster.common.multi_file_input_config import Config
from lobster.tools.cpp.item_builder import ItemBuilder
from lobster.common.multi_file_input_tool import create_worklist, MultiFileInputTool


FILE_LINE_PATTERN = r"(.*):(\d+):\d+:"
KIND_PATTERN = r"(function|main function|method)"
NAME_PATTERN = r"([a-zA-Z0-9_:~^()&\s<>,=*!+-.|[\]/\"]+)"
PREFIX = "^%s warning:" % FILE_LINE_PATTERN
SUFFIX = r"\[lobster-tracing\]$"

RE_NOTAGS = (PREFIX + " " +
             r"%s %s has no tracing tags" % (KIND_PATTERN,
                                             NAME_PATTERN) +
             " " + SUFFIX)
RE_TAGS = (PREFIX + " " +
           r"%s %s traces to +([^,\n]+(?:\s*,\s*[^,\n]+)*) +" % (KIND_PATTERN,
                                                                 NAME_PATTERN) +
           SUFFIX)
RE_JUST = (PREFIX + " " +
           r"%s %s exempt from tracing: +(.+) +" % (KIND_PATTERN,
                                                    NAME_PATTERN) +
           SUFFIX)


def extract_clang_finding_name(line: str) -> Optional[str]:
    """extracts the name of the clang finding from the end of the line"""
    if line.endswith("]") and ("[" in line):
        return line.split("[")[-1].rstrip("]")
    return None


class CppTool(MultiFileInputTool):
    def __init__(self):
        super().__init__(
            name = "cpp",
            description = "Extract tracing tags from C++ using clang-tidy",
            extensions=("cpp", "cc", "c", "h"),
            official = True,
        )
        self._argument_parser.add_argument(
            "--clang-tidy",
            default="clang-tidy",
            metavar="FILE",
            help=("use the specified clang-tidy; by default we"
                  " pick the one on PATH"),
        )
        self._argument_parser.add_argument(
            "--compile-commands",
            metavar="FILE",
            default=None,
            help=("Path to the compile command database for all targets for "
                  "'clang tidy', or none to use the default behavior of "
                  "'clang tidy'. This is equal to calling 'clang tidy' "
                  "directly with its '-p' option. Refer to its official "
                  "documentation for more details."),
        )
        self._argument_parser.add_argument(
            "--skip-clang-errors",
            default=[],
            nargs="*",
            metavar="FINDINGS",
            help="List of all clang-tidy errors to ignore.",
        )
        self._argument_parser.add_argument(
            "--kind",
            required=False,
            choices=[KindTypes.ITM.value, KindTypes.IMP.value],
            default=KindTypes.ITM.value,
            help=f"Kind of LOBSTER entries to create: '{KindTypes.ITM.value}' for Item, "
                 f"'{KindTypes.IMP.value}' for Implementation",
        )

    def _add_config_argument(self):
        # This tool does not use a config file
        pass

    def _run_impl(self, options: Namespace) -> int:
        config = Config(
            inputs=None,
            inputs_from_file=None,
            extensions=self._extensions,
            exclude_patterns=None,
            schema=Item,
        )

        if options.kind == KindTypes.IMP.value:
            config.schema = Implementation
        
        file_list = create_worklist(config, options.dir_or_files)
        clang_tidy_path = os.path.expanduser(options.clang_tidy)

        # Test if the clang-tidy can be used
        rv = subprocess.run(
            [
                clang_tidy_path,
                "-checks=-*,lobster-tracing",
                "--list-checks",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="UTF-8",
            check=False,
        )

        if "No checks enabled." in rv.stderr:
            print("The provided clang-tidy does include the lobster-tracing check")
            print("> Please build from "
                  "https://github.com/bmw-software-engineering/llvm-project")
            print("> Or make sure to provide the "
                  "correct binary using the --clang-tidy flag")
            return 1

        subprocess_args = [
            clang_tidy_path,
            "-checks=-*,lobster-tracing",
        ]
        if options.compile_commands:
            subprocess_args.append("-p")
            subprocess_args.append(options.compile_commands)

        subprocess_args += file_list

        rv = subprocess.run(
            subprocess_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="UTF-8",
            check=False,
        )

        if rv.returncode != 0:
            print(rv.stdout)
            print()
            print(rv.stderr)

            for line in rv.stdout.splitlines():
                if "error: " in line:
                    clang_error = extract_clang_finding_name(line)
                    if clang_error and (clang_error in options.skip_clang_errors):
                        print(f"Ignoring clang-tidy error {clang_error}")
                    else:
                        print("Found clang-tidy error: ", clang_error)
                        return 1

        db = {}
        item_builder = ItemBuilder()

        for line in rv.stdout.splitlines():
            if not line.endswith("[lobster-tracing]"):
                continue

            match = re.match(RE_NOTAGS, line)
            if match:
                impl = item_builder.from_match(match)
                assert impl.tag.key() not in db
                db[impl.tag.key()] = impl
                continue

            match = re.match(RE_JUST, line)
            if match:
                impl = item_builder.from_match_if_new(db, match)
                impl.just_up.append(
                    match.group(item_builder.REASON_GROUP_NUM),
                )
                continue

            match = re.match(RE_TAGS, line)
            if match:
                impl = item_builder.from_match_if_new(db, match)
                all_tags = match.group(item_builder.REFERENCE_GROUP_NUM)
                for tag in re.split(r"[, ]+", all_tags.strip()):
                    if tag:
                        impl.add_tracing_target(
                            Tracing_Tag(
                                "req",
                                tag,
                            ),
                        )
                continue

            print("could not parse line")
            print(">", line)
            return 1

        self._write_output(
            schema=config.schema,
            out_file=options.out,
            items=db.values(),
        )

        return 0


def main(args: Optional[Sequence[str]] = None) -> int:
    return CppTool().run(args)
