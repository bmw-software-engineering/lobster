#!/usr/bin/env python3
#
# lobster_rst_report - Visualise LOBSTER report as reStructuredText for Sphinx
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
"""
LOBSTER RST report tool -- top-level orchestration and CLI.

This module is intentionally thin: it wires together the helpers from
:mod:`_helpers` and the builder classes from :mod:`_renderers` to produce
complete RST documents, and exposes the CLI entry-point :func:`main`.

Public API
----------
* :func:`write_rst`              -- single-page RST string
* :func:`write_rst_to_file`      -- single-page RST to file
* :func:`write_rst_pages`        -- multi-page RST dict (filename to content)
* :func:`write_rst_pages_to_dir` -- write multi-page dict to a directory
* :func:`lobster_rst_report`     -- convenience wrapper (single-page)
* :func:`lobster_rst_report_pages` -- convenience wrapper (multi-page)
* :func:`main`                   -- argparse CLI entry-point
"""

import os
import argparse
from datetime import datetime, timezone
from typing import Dict, Optional, Sequence

from lobster.common.version import LOBSTER_VERSION
from lobster.common.report import Report
from lobster.common.io import ensure_output_directory
from lobster.common.meta_data_tool_base import MetaDataToolBase
from lobster.common.exceptions import LOBSTER_Exception
from lobster.common.errors import LOBSTER_Error
from lobster.common.graphviz_utils import is_dot_available

from ._helpers import RstUtils, ItemNaming
from ._renderers import (
    _KIND_ORDER,
    _build_page_map,
    LevelSectionBuilder,
    CoverageGridBuilder,
    IssuesListBuilder,
)


# ---------------------------------------------------------------------------
# Single-page output
# ---------------------------------------------------------------------------
#
# Heading hierarchy (first appearance determines RST level):
#   overline/#  -> document title
#   =           -> kind groups  (Requirements and Specification, ...)
#   -           -> level names  (System Requirements, ...)
#   ~           -> status groups inside each level (Issues N items, OK Items M items)


def write_rst(report: Report, source_root: str = "") -> str:
    """Render a LOBSTER report as a single reStructuredText string.

    The document contains a coverage summary grid (table + tracing-policy
    diagram), an issues list, and then the full item detail for every level
    grouped by kind.  Coverage Summary and Issues use ``.. rubric::`` so they
    do not appear as TOC entries in the Sphinx sidebar.

    Args:
        report: A loaded :class:`~lobster.common.report.Report` instance.
        source_root: Optional URL prefix prepended to plain file-reference
            paths.

    Returns:
        The complete RST document as a string (ending with a newline).
    """
    lines = []

    title = "L.O.B.S.T.E.R. Traceability Report"
    lines += RstUtils.heading(title, "#", overline=True)
    lines.append("")
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"| Generated: {now}")
    lines.append(f"| LOBSTER Version: {LOBSTER_VERSION}")
    lines.append("")

    # Coverage table + tracing-policy diagram (rubric = not a TOC entry)
    lines.append(".. rubric:: Coverage Summary")
    lines.append("")

    def ref_fn(n):
        return f":ref:`{RstUtils.escape(n)} <{ItemNaming.level_label(n)}>`"

    lines += CoverageGridBuilder(report).build(ref_fn)

    # Issues summary (rubric = not a TOC entry)
    lines.append(".. rubric:: Issues")
    lines.append("")
    lines += IssuesListBuilder(report).build()
    lines.append("")

    # Detailed content: kind groups and level sections
    items_by_level = {
        lv: [it for it in report.items.values() if it.level == lv]
        for lv in report.config
    }

    for kind, kind_title in _KIND_ORDER:
        levels_of_kind = [lv for lv in report.config.values() if lv.kind == kind]
        if not levels_of_kind:
            continue

        lines += RstUtils.heading(kind_title, "=")
        lines.append("")

        for level in levels_of_kind:
            lines.append(f".. _{ItemNaming.level_label(level.name)}:")
            lines.append("")
            lines += RstUtils.heading(level.name, "-")
            lines.append("")

            items = items_by_level[level.name]
            if not items:
                lines.append("No items recorded at this level.")
                lines.append("")
                continue

            data = report.coverage[level.name]
            lines.append(
                f"**Coverage:** {data.coverage:.1f}%"
                f" ({data.ok} of {data.items} items OK)"
            )
            lines.append("")
            lines += LevelSectionBuilder(items, report, source_root).build()

    return "\n".join(lines) + "\n"


def write_rst_to_file(rst_content: str, output_path: str) -> None:
    """Write RST content to *output_path*, creating parent directories as needed.

    Args:
        rst_content: The RST string to write.
        output_path: The destination file path.
    """
    ensure_output_directory(output_path)
    with open(output_path, "w", encoding="UTF-8") as fd:
        fd.write(rst_content)


# ---------------------------------------------------------------------------
# Multi-page output
# ---------------------------------------------------------------------------
#
# Heading hierarchy:
#   index.rst   -- overline/# title only; Coverage/Issues are rubrics (not in
#                  TOC); kind groups are toctree :caption: entries (not headings)
#   level pages -- = for page title, - for Issues/OK Items sub-sections


def write_rst_pages(report: Report, source_root: str = "") -> Dict[str, str]:
    """Render a LOBSTER report as a set of linked RST pages.

    Produces one RST file per tracing level plus an ``index.rst`` that links
    them together.  The index page contains the coverage grid, issues list,
    and per-kind ``.. toctree::`` directives whose ``:caption:`` entries
    appear in the Sphinx sidebar without adding clickable heading nodes.

    Args:
        report: A loaded :class:`~lobster.common.report.Report` instance.
        source_root: Optional URL prefix prepended to plain file-reference
            paths.

    Returns:
        A ``dict`` mapping filename (e.g. ``"index.rst"``,
        ``"system_requirements.rst"``) to RST content strings.
    """
    page_map = _build_page_map(report)
    coverage = report.coverage
    items_by_level = {
        lv: [it for it in report.items.values() if it.level == lv]
        for lv in report.config
    }

    pages = {}

    # -- Level pages --
    for level_name in report.config:
        stem = page_map[level_name]
        data = coverage[level_name]
        items = items_by_level[level_name]

        lines = []
        lines += RstUtils.heading(level_name, "=")
        lines.append("")

        if not items:
            lines.append("No items recorded at this level.")
            lines.append("")
        else:
            lines.append(
                f"**Coverage:** {data.coverage:.1f}%"
                f" ({data.ok} of {data.items} items OK)"
            )
            lines.append("")
            lines += LevelSectionBuilder(items, report, source_root).build()

        pages[f"{stem}.rst"] = "\n".join(lines) + "\n"

    # -- Index page --
    lines = []
    title = "L.O.B.S.T.E.R. Traceability Report"
    lines += RstUtils.heading(title, "#", overline=True)
    lines.append("")
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"| Generated: {now}")
    lines.append(f"| LOBSTER Version: {LOBSTER_VERSION}")
    lines.append("")

    # Coverage table + policy diagram (rubric = not a TOC entry)
    lines.append(".. rubric:: Coverage Summary")
    lines.append("")

    def ref_fn(n):
        return f":doc:`{RstUtils.escape(n)} <{page_map[n]}>`"

    lines += CoverageGridBuilder(report).build(ref_fn)

    # Issues list (rubric = not a TOC entry)
    lines.append(".. rubric:: Issues")
    lines.append("")
    lines += IssuesListBuilder(report).build()
    lines.append("")

    # Per-kind toctrees -- :caption: shows in sidebar but doesn't create a
    # heading node, so clicking a level goes straight to that level's page
    for kind, kind_title in _KIND_ORDER:
        levels_of_kind = [lv for lv in report.config.values() if lv.kind == kind]
        if not levels_of_kind:
            continue
        lines.append(".. toctree::")
        lines.append(f"   :caption: {kind_title}")
        lines.append("   :maxdepth: 1")
        lines.append("")
        for lv in levels_of_kind:
            lines.append(f"   {page_map[lv.name]}")
        lines.append("")

    pages["index.rst"] = "\n".join(lines) + "\n"

    return pages


def write_rst_pages_to_dir(pages: Dict[str, str], out_dir: str) -> None:
    """Write multi-page RST output to *out_dir*, creating it if necessary.

    Args:
        pages: A ``dict`` mapping filename to RST content, as returned by
            :func:`write_rst_pages`.
        out_dir: The directory to write files into.  Created if it does not
            already exist.
    """
    os.makedirs(out_dir, exist_ok=True)
    for filename, content in pages.items():
        filepath = os.path.join(out_dir, filename)
        with open(filepath, "w", encoding="UTF-8") as fd:
            fd.write(content)


# ---------------------------------------------------------------------------
# CLI tool
# ---------------------------------------------------------------------------


class RstReportTool(MetaDataToolBase):
    """Argparse-based CLI tool for generating RST reports from LOBSTER data.

    Registered as the ``rst-report`` tool in the LOBSTER tool registry.
    Supports both single-page (``--out``) and multi-page (``--out-dir``) output.
    """

    def __init__(self):
        """Register the tool with its name, description, and argument parser."""
        super().__init__(
            name="rst-report",
            description="Visualise LOBSTER report as reStructuredText for Sphinx",
            official=True,
        )

        ap = self._argument_parser
        ap.add_argument(
            "lobster_report",
            nargs="?",
            default="report.lobster",
            help="path to the LOBSTER report file (default: report.lobster)",
        )

        output_group = ap.add_mutually_exclusive_group()
        output_group.add_argument(
            "--out",
            default=None,
            metavar="FILE",
            help="write single-page RST to FILE (default: lobster_report.rst)",
        )
        output_group.add_argument(
            "--out-dir",
            default=None,
            metavar="DIR",
            help="write multi-page RST to DIR (index.rst + one page per level)",
        )

        ap.add_argument(
            "--source-root",
            default="",
            help="prefix prepended to file reference URLs, e.g. a relative "
            "path from the RST output location back to the workspace root",
        )

    def _run_impl(self, options: argparse.Namespace) -> int:
        """Execute the tool with the parsed command-line options.

        Args:
            options: Parsed argument namespace from argparse.

        Returns:
            Integer exit code (0 on success).
        """
        # lobster-trace: rst_req.Missing_Lobster_File
        if not os.path.isfile(options.lobster_report):
            self._argument_parser.error(f"{options.lobster_report} is not a file")

        try:
            report = Report()
            report.load_report(options.lobster_report)
        except LOBSTER_Error as err:
            print(err)
            print(f"{self.name}: aborting due to earlier errors.")
            return 1
        except LOBSTER_Exception as err:
            err.dump()
            return 1

        if not is_dot_available():
            print(
                "warning: dot utility not found, report will not include "
                "the tracing policy visualisation"
            )
            print("> please install Graphviz (https://graphviz.org)")

        # lobster-trace: UseCases.RST_Output
        # lobster-trace: rst_req.RST_Report_Multi_Page
        # lobster-trace: rst_req.Valid_Lobster_File_Multi_Page
        if options.out_dir is not None:
            pages = write_rst_pages(report=report, source_root=options.source_root)
            write_rst_pages_to_dir(pages, options.out_dir)
            print(
                f"LOBSTER RST report written to {options.out_dir}/ ({len(pages)} files)"
            )
        # lobster-trace: UseCases.RST_Output
        # lobster-trace: rst_req.RST_Report_Single_Page
        # lobster-trace: rst_req.Valid_Lobster_File
        else:
            out_path = options.out if options.out is not None else "lobster_report.rst"
            rst_content = write_rst(report=report, source_root=options.source_root)
            write_rst_to_file(rst_content, out_path)
            print(f"LOBSTER RST report written to {out_path}")

        return 0


# ---------------------------------------------------------------------------
# Public convenience API
# ---------------------------------------------------------------------------


def lobster_rst_report(
    lobster_report_path: str,
    output_rst_path: str,
    source_root: str = "",
) -> None:
    """Generate a single-page RST report from a LOBSTER report file.

    Args:
        lobster_report_path: Path to the input ``.lobster`` report file.
        output_rst_path: Path to the output RST file to create.
        source_root: Optional URL prefix prepended to file-reference paths.
    """
    report = Report()
    report.load_report(lobster_report_path)
    write_rst_to_file(
        write_rst(report=report, source_root=source_root), output_rst_path
    )


def lobster_rst_report_pages(
    lobster_report_path: str,
    output_dir: str,
    source_root: str = "",
) -> None:
    """Generate a multi-page RST report from a LOBSTER report file.

    Args:
        lobster_report_path: Path to the input ``.lobster`` report file.
        output_dir: Directory to write RST pages into.
        source_root: Optional URL prefix prepended to file-reference paths.
    """
    report = Report()
    report.load_report(lobster_report_path)
    write_rst_pages_to_dir(
        write_rst_pages(report=report, source_root=source_root),
        output_dir,
    )


def main(args: Optional[Sequence[str]] = None) -> int:
    """Entry point for the ``lobster-rst-report`` command-line tool.

    Args:
        args: Optional list of CLI argument strings.  When ``None`` (default),
            ``sys.argv[1:]`` is used.

    Returns:
        Integer exit code (0 on success).
    """
    return RstReportTool().run(args)
