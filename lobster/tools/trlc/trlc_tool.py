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

import argparse
import os
import sys
from typing import Iterable

from yamale import YamaleError

from trlc.errors import Message_Handler, TRLC_Error
from trlc.trlc import Source_Manager

from lobster.common.errors import PathError
from lobster.common.io import lobster_write
from lobster.common.items import Requirement
from lobster.common.multi_file_input_tool import create_worklist, MultiFileInputTool

from lobster.tools.trlc.converter import Converter
from lobster.tools.trlc.errors import (
    InvalidConversionRuleError,
    RecordObjectComponentError,
    TrlcFailure,
    TupleToStringFailedError,
    TupleToStringMissingError,
)
from lobster.tools.trlc.lobster_trlc_config import LobsterTrlcConfig


class LOBSTER_Trlc(MultiFileInputTool):
    def __init__(self):
        super().__init__(
            name        = "trlc",
            description = "Extract tracing data from TRLC files.",
            extensions  = ["rsl", "trlc"],
            official    = True,
        )

    def _run_impl(self, options: argparse.Namespace):
        try:
            self._execute(options)
            return 0
        except YamaleError as e:
            print(
                f"{self.name}: The configuration file does not "
                f"conform to the YAML schema. {e}",
                file=sys.stderr,
            )
        except TRLC_Error as e:
            print(
                f"{self.name}: An error occurred during processing: {e}",
                file=sys.stderr,
            )
        except FileNotFoundError as e:
            print(
                f"{self.name}: File or directory not found: {e}",
                file=sys.stderr,
            )
        except PathError as e:
            print(
                f"{self.name}: {e}",
                file=sys.stderr,
            )
        except TrlcFailure as e:
            print(
                f"{self.name}: TRLC processing failed: {e}",
                file=sys.stderr,
            )
        except (InvalidConversionRuleError, RecordObjectComponentError) as e:
            print(
                f"{self.name}: Invalid conversion rule defined in {options.config}: "
                f"{e}",
                file=sys.stderr,
            )
        except (TupleToStringMissingError, TupleToStringFailedError) as e:
            print(
                f"{self.name}: error in 'to-string-rules' in {options.config}: "
                f"{e}",
                file=sys.stderr,
            )

        return 1

    @staticmethod
    def _register_trlc_files(sm: Source_Manager, work_list: Iterable[str]):
        for item in work_list:
            ok = True
            if os.path.isfile(item):
                ok = sm.register_file(item)
            elif os.path.isdir(item):
                ok = sm.register_directory(item)
            else:
                raise FileNotFoundError(item)
            if not ok:
                raise PathError(f"Failed to register file or directory '{item}'")

    def _execute(self, options: argparse.Namespace) -> None:
        config = LobsterTrlcConfig.from_file(options.config)
        work_list = create_worklist(config, options.dir_or_files)
        trlc_mh = Message_Handler()
        sm = Source_Manager(trlc_mh)
        self._register_trlc_files(sm, work_list)
        symbol_table = sm.process()
        if not symbol_table:
            raise TrlcFailure("aborting due to TRLC error")

        items = []
        converter = Converter(
            conversion_rules=config.conversion_rules,
            to_string_rules=config.to_string_rules,
            symbol_table=symbol_table,
        )
        for n_obj in symbol_table.iter_record_objects():
            item = converter.generate_lobster_object(n_obj)
            if item:
                items.append(item)

        with open(options.out, "w", encoding="UTF-8") as fd:
            # lobster-trace: trlc_req.Output_File
            lobster_write(
                fd=fd,
                kind=Requirement,
                generator="lobster-trlc",
                items=items,
            )
        print(f"lobster-trlc: successfully wrote {len(items)} items to {options.out}")


def main():
    return LOBSTER_Trlc().run()
