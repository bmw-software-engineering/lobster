#!/usr/bin/env python3
#
# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2022-2024 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

import os.path
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outfile")
    ap.add_argument("infiles", nargs="*")
    options = ap.parse_args()

    with open(options.outfile, "w", encoding="UTF-8") as fd_out:
        fd_out.write("#!/usr/bin/env python3\n\n")
        for file_name in options.infiles:
            with open(file_name, "r", encoding="UTF-8") as fd_in:
                svg = fd_in.read()
            assert len(svg.splitlines()) == 1
            name, _ = os.path.splitext(os.path.basename(file_name))
            name = name.replace("-", "_")
            fd_out.write("SVG_" + name.upper())
            fd_out.write(" = r'''")
            svg_text = svg.strip()
            svg_text = svg_text.replace('svg" width="24" height="24"',
                                        'svg" width="1em" height="1em"')
            fd_out.write(svg_text)
            fd_out.write("'''\n\n")

if __name__ == "__main__":
    main()
