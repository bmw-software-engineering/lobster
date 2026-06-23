#!/usr/bin/env python3
#
# lobster_rst_report - Visualise LOBSTER report as reStructuredText for Sphinx
# Copyright (C) 2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
Primitive helpers for the RST report tool.

Organised into four static-method classes with focused concerns:

* :class:`RstUtils`            -- RST text escaping and heading generation
* :class:`ItemNaming`          -- label, page-name, and kind-string derivation
* :class:`TracingClassifier`   -- message classification and status-to-CSS mapping
* :class:`PolicyDiagramBuilder`-- Graphviz DOT generation for the tracing policy
"""

from typing import Dict, Tuple

from lobster.common.report import Report
from lobster.common.location import (
    Void_Reference,
    File_Reference,
    Github_Reference,
    Codebeamer_Reference,
)
from lobster.common.items import Item, Requirement, Implementation, Activity


class RstUtils:
    """Pure RST text-formatting utilities."""

    @staticmethod
    def escape(text: str) -> str:
        """Escape characters that carry special meaning in RST inline markup.

        The characters ``\\``, `` ` ``, ``*``, ``_``, and ``|`` are each
        prefixed with a backslash so they are treated as literals by Sphinx.

        Args:
            text: The plain-text string to escape.

        Returns:
            The escaped string, safe for use in any RST inline context.
        """
        for ch in ("\\", "`", "*", "_", "|"):
            text = text.replace(ch, "\\" + ch)
        return text

    @staticmethod
    def heading(text: str, char: str, overline: bool = False) -> list:
        """Return a list of RST lines that form a section heading.

        The caller is responsible for appending a blank string after the
        returned lines to satisfy RST's required blank line.

        Args:
            text: The heading text.
            char: The underline (and overline, if *overline* is ``True``)
                character (e.g. ``"="``, ``"-"``, ``"~"``).
            overline: When ``True`` an overline of the same character is
                added above the heading text.

        Returns:
            A list of 2 lines (underline only) or 3 lines (with overline).
            No trailing blank line is included.
        """
        line = char * len(text)
        if overline:
            return [line, text, line]
        return [text, line]


class ItemNaming:
    """Helpers for generating Sphinx labels and human-readable strings for
    LOBSTER items."""

    @staticmethod
    def item_label(item: Item) -> str:
        """Return the Sphinx cross-reference label for a tracing item.

        The label is stable as long as the item's hash does not change.

        Args:
            item: Any LOBSTER :class:`~lobster.common.items.Item`.

        Returns:
            A string of the form ``"lobster-item-<hash>"``.
        """
        return "lobster-item-" + item.tag.hash()

    @staticmethod
    def level_label(level_name: str) -> str:
        """Return the Sphinx cross-reference label for a level section.

        Args:
            level_name: The human-readable level name
                (e.g. ``"System Requirements"``).

        Returns:
            A slug of the form ``"lobster-level-system-requirements"``.
        """
        return "lobster-level-" + level_name.replace(" ", "-").lower()

    @staticmethod
    def level_page_name(level_name: str) -> str:
        """Return a filesystem-safe page stem (no file extension) for a level.

        All non-alphanumeric characters are replaced by underscores;
        consecutive underscores are collapsed; leading and trailing
        underscores are stripped.

        Args:
            level_name: The human-readable level name.

        Returns:
            A lowercase, underscore-separated identifier suitable for use as
            a filename stem (e.g. ``"system_requirements"``).
        """
        safe = level_name.lower()
        for ch in (" ", "-", "/", "\\", "(", ")", ",", "."):
            safe = safe.replace(ch, "_")
        while "__" in safe:
            safe = safe.replace("__", "_")
        return safe.strip("_") or "level"

    @staticmethod
    def item_kind_str(item: Item) -> str:
        """Return a human-readable kind label for a LOBSTER item.

        Combines the item's framework or language with its kind, e.g.
        ``"TRLC Requirement"`` or ``"Python Function"``.

        Args:
            item: Any LOBSTER :class:`~lobster.common.items.Item`.

        Returns:
            A capitalised kind string.
        """
        if isinstance(item, Requirement):
            return f"{item.framework} {item.kind.capitalize()}"
        if isinstance(item, Implementation):
            return f"{item.language} {item.kind.capitalize()}"
        assert isinstance(item, Activity)
        return f"{item.framework} {item.kind.capitalize()}"

    @staticmethod
    def location_link(location, source_root: str = "") -> str:
        """Convert a LOBSTER location to an RST anonymous hyperlink or plain text.

        Produces a clickable `` `text <url>`__ `` for file, GitHub, and
        Codebeamer references, and falls back to escaped plain text for any
        other location type.

        Args:
            location: A LOBSTER location object.
            source_root: Optional URL prefix prepended to plain
                :class:`~lobster.common.location.File_Reference` paths.

        Returns:
            An RST inline hyperlink string or plain escaped text.
        """
        e = RstUtils.escape

        if isinstance(location, Void_Reference):
            return "unknown location"

        # lobster-trace: UseCases.Item_GitHub_Source
        # lobster-trace: rst_req.RST_Source_Root_Prefix
        if isinstance(location, File_Reference):
            href = (source_root.rstrip("/") + "/" + location.filename
                    if source_root else location.filename)
            return f"`{e(location.to_string())} <{href}>`__"

        # lobster-trace: UseCases.Item_GitHub_Source
        if isinstance(location, Github_Reference):
            url = f"{location.gh_root}/blob/{location.commit}/{location.filename}"
            if location.line:
                url += f"#L{location.line}"
            return f"`{e(location.to_string())} <{url}>`__"

        # lobster-trace: UseCases.Show_codebeamer_links
        # lobster-trace: rst_req.RST_Clickable_Codebeamer_Item
        # lobster-trace: rst_req.RST_Codebeamer_Item_Name
        if isinstance(location, Codebeamer_Reference):
            url = f"{location.cb_root}/issue/{location.item}"
            if location.version:
                url += f"?version={location.version}"
            return f"`{e(location.to_string())} <{url}>`__"

        return e(str(location))


class TracingClassifier:
    """Classify tracing messages and map tracing status to sphinx-design CSS classes."""

    #: Mapping from :attr:`~lobster.common.items.Tracing_Status` name to
    #: sphinx-design card-header CSS classes.
    CARD_CLASSES: Dict[str, str] = {
        "OK": "sd-bg-success sd-text-white",
        "JUSTIFIED": "sd-bg-success sd-text-white",
        "PARTIAL": "sd-bg-warning",
        "MISSING": "sd-bg-danger sd-text-white",
        "ERROR": "sd-bg-danger sd-text-white",
    }

    @staticmethod
    def categorize(messages: list) -> tuple:
        """Split issue messages into downward, upward, and general buckets.

        Inspects each message's text to decide whether it describes a problem
        with a downward tracing link (traces *to* another item), an upward
        tracing link (derived *from* another item), or something else.

        .. note::
            Classification is based on substring matching against the following
            known LOBSTER message patterns:

            * Upward: ``"up reference"``, ``"missing upward"``,
              ``"upward tracing"``
            * Downward: ``"down reference"``, ``"missing downward"``,
              ``"missing reference to"``, ``"tracing destination"``,
              ``"unknown tracing target"``, ``"downward tracing"``
            * General: everything else

            If upstream message wording changes, update both this method and
            its tests.

        Args:
            messages: A list of raw tracing-issue message strings.

        Returns:
            A 3-tuple ``(down_msgs, up_msgs, general_msgs)`` where each
            element is a list of message strings.
        """
        down, up, general = [], [], []
        for msg in messages:
            ml = msg.lower()
            if "up reference" in ml or "missing upward" in ml or "upward tracing" in ml:
                up.append(msg)
            elif ("down reference" in ml or
                  "missing downward" in ml or
                  "missing reference to" in ml):
                down.append(msg)
            elif ("tracing destination" in ml or
                  "unknown tracing target" in ml or
                  "downward tracing" in ml):
                down.append(msg)
            else:
                general.append(msg)
        return down, up, general

    @staticmethod
    def issue_tag(msg: str) -> str:
        """Return a concise human-readable label for a tracing issue message.

        Transforms verbose internal messages into short display labels, e.g.
        ``"missing reference to Verification Test"`` becomes
        ``"no trace to: Verification Test"``.

        Args:
            msg: A raw tracing-issue message string.

        Returns:
            A short descriptive label, or the original message (RST-escaped)
            if no known pattern matches.
        """
        ml = msg.lower()
        e = RstUtils.escape
        if "version" in ml and "expected" in ml:
            return "version mismatch"
        if "unknown tracing target" in ml:
            target = msg.split("unknown tracing target ", 1)[-1]
            return f"unknown target: {e(target)}"
        if "missing up reference" in ml:
            return "no upward trace"
        if "missing reference to " in ml:
            target = msg.split("missing reference to ", 1)[-1]
            return f"no trace to: {e(target)}"
        if "missing down reference" in ml:
            return "no downward trace"
        return e(msg)

    @classmethod
    def card_header_class(cls, status_name: str) -> str:
        """Return sphinx-design CSS class string for a card header.

        Args:
            status_name: The ``name`` attribute of a
                :class:`~lobster.common.items.Tracing_Status` member
                (e.g. ``"OK"``, ``"MISSING"``).

        Returns:
            A space-separated string of sphinx-design CSS classes.
            Falls back to ``"sd-bg-secondary sd-text-white"`` for unknown values.
        """
        return cls.CARD_CLASSES.get(status_name, "sd-bg-secondary sd-text-white")


class PolicyDiagramBuilder:
    """Build a Graphviz DOT diagram representing the configured tracing policy.

    Nodes represent tracing levels, coloured by kind:

    * *requirements*   -- blue (``#2196F3``)
    * *implementation* -- green (``#4CAF50``)
    * *activity*       -- orange (``#FF9800``)

    Directed edges follow the ``traces`` relationship (level A → level B means
    A must be traceable to B).
    """

    #: Fill and font colour pairs keyed by level kind.
    KIND_COLORS: Dict[str, Tuple[str, str]] = {
        "requirements": ("#2196F3", "white"),
        "implementation": ("#4CAF50", "white"),
        "activity": ("#FF9800", "white"),
    }

    @staticmethod
    def dot_escape(text: str) -> str:
        """Escape *text* for safe embedding inside a DOT double-quoted string.

        Args:
            text: Arbitrary string to use in a DOT node label or attribute.

        Returns:
            The text with backslashes and double-quotes escaped.
        """
        return text.replace("\\", "\\\\").replace('"', '\\"')

    @classmethod
    def build(cls, report: Report, indent: int = 0,
              dot_available: bool = True) -> list:
        """Return RST lines for a ``.. graphviz::`` tracing-policy diagram.

        When *dot_available* is ``False`` (e.g. Graphviz is not installed), a
        ``.. note::`` block is emitted instead so the HTML page remains valid.

        Args:
            report: The loaded LOBSTER report whose ``config`` provides level
                names, kinds, and tracing relationships.
            indent: Number of leading spaces to prepend to each line.  Use
                a non-zero value when embedding inside nested RST directives
                such as ``.. grid-item::``.
            dot_available: Whether the Graphviz ``dot`` executable is
                available.  Pass the return value of
                :func:`~lobster.common.graphviz_utils.is_dot_available`.

        Returns:
            A list of RST lines ending with a blank string.
        """
        indent_str = " " * indent
        if not dot_available:
            # lobster-trace: rst_req.RST_Report_Tracing_Policy_Diagram_Fallback
            return [
                f"{indent_str}.. note::",
                "",
                f"{indent_str}   Tracing policy diagram omitted —"
                f" Graphviz (dot) is not installed.",
                "",
            ]
        # lobster-trace: rst_req.RST_Report_Tracing_Policy_Diagram
        nested_indent = indent_str + "   "
        out = []
        out.append(f"{indent_str}.. graphviz::")
        out.append("")
        out.append(f"{nested_indent}digraph tracing_policy {{")
        out.append(f"{nested_indent}   rankdir=TB;")
        out.append(
            f"{nested_indent}   node [shape=box, style=filled, "
            f'fontname="Helvetica", margin="0.3,0.1"];'
        )
        out.append(f"{nested_indent}   edge [arrowhead=open];")
        out.append("")
        for level_name, level in report.config.items():
            fill, font = cls.KIND_COLORS.get(level.kind, ("#9E9E9E", "white"))
            safe = cls.dot_escape(level_name)
            out.append(
                f'{nested_indent}   "{safe}" [fillcolor="{fill}", fontcolor="{font}"];'
            )
        for level_name, level in report.config.items():
            for trace_target in level.traces:
                src = cls.dot_escape(level_name)
                dst = cls.dot_escape(trace_target)
                out.append(f'{nested_indent}   "{src}" -> "{dst}";')
        out.append(f"{nested_indent}}}")
        out.append("")
        return out
