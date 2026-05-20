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
RST block builder classes for the RST report tool.

Each class accepts LOBSTER report data and returns RST lines via a ``build()``
method.  Lines can be joined with ``"\\n".join(lines)`` to form valid RST.

Classes
-------
* :class:`ItemCardBuilder`      -- one item as a sphinx-design card
* :class:`LevelSectionBuilder`  -- all items for one level (Issues + OK Items)
* :class:`CoverageGridBuilder`  -- coverage table + graphviz policy diagram
* :class:`IssuesListBuilder`    -- index-page issue summary list

Module-level helpers
--------------------
* :data:`_KIND_ORDER`     -- canonical display order for level kinds
* :func:`_build_page_map` -- ``{level_name: page_stem}`` mapping
"""

from typing import Dict

from lobster.common.report import Report
from lobster.common.items import Tracing_Status, Item, Requirement

from ._helpers import RstUtils, ItemNaming, TracingClassifier, PolicyDiagramBuilder


#: Canonical display order: list of ``(kind_value, section_title)`` pairs.
_KIND_ORDER = [
    ("requirements", "Requirements and Specification"),
    ("implementation", "Implementation"),
    ("activity", "Verification and Validation"),
]


def _build_page_map(report: Report) -> Dict[str, str]:
    """Build a mapping from level name to filesystem-safe page stem.

    Duplicate stems (produced when two level names collapse to the same slug)
    are disambiguated by appending a numeric suffix.

    Args:
        report: The loaded LOBSTER report.

    Returns:
        A ``dict`` of ``{level_name: page_stem}`` where every value is a
        unique, filesystem-safe string without a file extension.
    """
    seen: Dict[str, int] = {}
    page_map: Dict[str, str] = {}
    for level_name in report.config:
        stem = ItemNaming.level_page_name(level_name)
        if stem in seen:
            seen[stem] += 1
            stem = f"{stem}_{seen[stem]}"
        else:
            seen[stem] = 0
        page_map[level_name] = stem
    return page_map


class ItemCardBuilder:
    """Build a sphinx-design card for a single LOBSTER tracing item.

    The card is structured in three sections:

    * **Header** (coloured stripe) -- status badge and item name, styled via
      the ``^^^`` separator so that ``:class-header:`` CSS is applied.
    * **Body** -- workflow status, description, tracing links, and any inline
      issue messages (no ``.. warning::`` admonition box).
    * **Footer** -- source location link.

    Usage::

        lines = ItemCardBuilder(item, report, source_root).build()
    """

    def __init__(self, item: Item, report: Report, source_root: str = ""):
        """Initialise the builder.

        Args:
            item: The LOBSTER item to render.
            report: The full report, needed to resolve cross-references.
            source_root: Optional URL prefix prepended to plain file-reference
                paths (see :meth:`ItemNaming.location_link`).
        """
        self._item = item
        self._report = report
        self._source_root = source_root

    def build(self) -> list:
        """Return RST lines for the item dropdown.

        All items use ``.. dropdown::``.  OK and JUSTIFIED items start closed
        (low visual weight); all other statuses start open.  Issue messages
        are rendered as nested open red dropdowns -- no custom CSS required.

        Returns:
            A list of RST lines ending with a blank string.
        """
        item = self._item
        e = RstUtils.escape
        status = item.tracing_status.name if item.tracing_status else "UNKNOWN"
        kind_str = ItemNaming.item_kind_str(item)
        down_msgs, up_msgs, gen_msgs = TracingClassifier.categorize(item.messages)
        is_ok = status in ("OK", "JUSTIFIED")
        hdr_class = TracingClassifier.card_header_class(status)
        title = f"[{status}] {e(kind_str)} {e(item.name)}"

        out = []

        # Anchor label
        out.append(f".. _{ItemNaming.item_label(item)}:")
        out.append("")

        # lobster-trace: rst_req.RST_Report_Item_Details
        # lobster-trace: UseCases.Colored_Findings
        # All items are dropdowns; non-OK items start open.
        out.append(f".. dropdown:: {title}")
        if not is_ok:
            out.append("   :open:")
        out.append(f"   :class-title: {hdr_class}")
        out.append("")

        def body(text=""):
            """Append a line at 3-space indent (card body level)."""
            out.append(f"   {text}".rstrip())

        def nested(text=""):
            """Append a line at 6-space indent (nested directive body)."""
            out.append(f"      {text}".rstrip())

        def sep():
            """Emit an HTML horizontal rule separator."""
            body(".. raw:: html")
            out.append("")
            nested("<hr>")
            out.append("")

        def issue_box(msgs):
            """Render issue messages as a light-red card body (no heading)."""
            body(".. card::")
            nested(":class-card: lobster-issue-card")
            out.append("")
            for msg in msgs:
                nested(f"* {e(msg)}")
            out.append("")

        # Track whether any body content has been emitted (drives separator logic).
        has_content = False

        # lobster-trace: rst_req.RST_Report_Item_Details
        # Workflow status (requirements only)
        if isinstance(item, Requirement) and item.status:
            body(f"**Status:** {e(item.status)}")
            out.append("")
            has_content = True

        # Description text (requirements only)
        if isinstance(item, Requirement) and item.text:
            body(".. pull-quote::")
            out.append("")
            for text_line in item.text.splitlines():
                nested(e(text_line))
            out.append("")
            has_content = True

        # lobster-trace: UseCases.List_Requirements_to_Tests
        # lobster-trace: UseCases.List_Tests_to_Requirements
        # Downward traces section
        has_down = bool(item.ref_down or down_msgs)
        if has_down:
            if has_content:
                sep()
            body("**Traces to:**")
            out.append("")
            for ref_str in self._resolve_refs(item.ref_down):
                body(f"* {ref_str}")
            if item.ref_down:
                out.append("")
            if down_msgs:
                issue_box(down_msgs)
            has_content = True

        # lobster-trace: UseCases.List_Requirements_without_Tests
        # lobster-trace: UseCases.List_Tests_without_Requirements
        # Upward traces section
        has_up = bool(item.ref_up or up_msgs)
        if has_up:
            if has_content:
                sep()
            body("**Derived from:**")
            out.append("")
            for ref_str in self._resolve_refs(item.ref_up):
                body(f"* {ref_str}")
            if item.ref_up:
                out.append("")
            if up_msgs:
                issue_box(up_msgs)
            has_content = True

        # Justification text
        if item.tracing_status == Tracing_Status.JUSTIFIED:
            justifications = item.just_global + item.just_up + item.just_down
            if justifications:
                if has_content:
                    sep()
                body(f"**Justifications:** {'; '.join(e(j) for j in justifications)}")
                out.append("")
                has_content = True

        # General messages (not clearly upward or downward)
        if gen_msgs:
            if has_content:
                sep()
            issue_box(gen_msgs)

        # lobster-trace: UseCases.Item_GitHub_Source
        # lobster-trace: UseCases.Show_codebeamer_links
        # Source location: always inline at end (.. dropdown:: has no +++ footer).
        source_link = ItemNaming.location_link(item.location, self._source_root)
        if has_content or gen_msgs:
            sep()
        body(f"**Source:** {source_link}")
        out.append("")

        return out

    def _resolve_refs(self, refs) -> list:
        """Resolve tracing references to RST cross-reference strings.

        Known items are rendered as ``:ref:`` links; unresolvable references
        fall back to a code literal of the reference key.

        Args:
            refs: An iterable of reference objects with a ``key()`` method.

        Returns:
            A list of RST inline strings (one per reference).
        """
        parts = []
        for ref in refs:
            key = ref.key()
            if key in self._report.items:
                ref_item = self._report.items[key]
                parts.append(
                    f":ref:`{RstUtils.escape(ref_item.name)}"
                    f" <{ItemNaming.item_label(ref_item)}>`"
                )
            else:
                parts.append(f"``{RstUtils.escape(key)}`` (unresolved)")
        return parts


class LevelSectionBuilder:
    """Build the RST body for a single tracing level.

    Issue items (open red dropdowns) are emitted before OK items (closed green
    dropdowns).  The dropdown open/closed state communicates status visually,
    so no filter TOC or sub-section headings are added.

    Usage::

        lines = LevelSectionBuilder(items, report, source_root).build()
    """

    def __init__(self, items: list, report: Report, source_root: str = ""):
        """Initialise the builder.

        Args:
            items: The list of LOBSTER items belonging to this level.
            report: The full report, needed for cross-reference resolution.
            source_root: Optional URL prefix prepended to file-reference paths.
        """
        self._items = items
        self._report = report
        self._source_root = source_root

    def build(self) -> list:
        """Return RST lines for the level body.

        Issue items (non-OK/non-JUSTIFIED) come first, sorted by location,
        followed by OK/JUSTIFIED items.  No filter TOC or sub-headings are
        emitted; the dropdown open/closed state communicates status visually.

        Returns:
            A list of RST lines.
        """
        issue_items = sorted(
            (
                it
                for it in self._items
                if it.tracing_status
                not in (Tracing_Status.OK, Tracing_Status.JUSTIFIED)
            ),
            key=lambda x: x.location.sorting_key(),
        )
        ok_items = sorted(
            (
                it
                for it in self._items
                if it.tracing_status in (Tracing_Status.OK, Tracing_Status.JUSTIFIED)
            ),
            key=lambda x: x.location.sorting_key(),
        )

        out = []
        for it in issue_items + ok_items:
            out += ItemCardBuilder(it, self._report, self._source_root).build()

        if not out:
            out += ["No items recorded at this level.", ""]

        return out


class CoverageGridBuilder:
    """Build the coverage summary section (table + policy diagram side by side).

    Uses a sphinx-design ``.. grid:: 1 1 2 2`` layout:

    * Left column (7/12 width on desktop) -- a ``.. list-table::`` with
      per-level coverage statistics and links to each level.
    * Right column (5/12 width on desktop) -- the :class:`PolicyDiagramBuilder`
      graphviz diagram showing level kinds and tracing relationships.

    Usage::

        ref_fn = lambda n: f":doc:`{n} <page_stem>`"
        lines = CoverageGridBuilder(report).build(ref_fn)
    """

    def __init__(self, report: Report):
        """Initialise the builder.

        Args:
            report: The loaded LOBSTER report, providing coverage data and config.
        """
        self._report = report

    def build(self, ref_fn) -> list:
        """Return RST lines for the coverage grid.

        Args:
            ref_fn: A callable ``(level_name: str) -> str`` returning an RST
                cross-reference for the given level.  Use ``:ref:`` links for
                single-page output and ``:doc:`` links for multi-page output.

        Returns:
            A list of RST lines ending with a blank string.
        """
        # lobster-trace: UseCases.Item_Coverage
        # lobster-trace: rst_req.RST_Report_Coverage_Table
        lines = []
        lines += [".. grid:: 1 1 2 2", "   :gutter: 3", ""]
        lines += ["   .. grid-item::", "      :columns: 12 12 7 7", ""]
        lines += [
            "      .. list-table::",
            "         :header-rows: 1",
            "         :widths: 35 15 15 15",
            "",
        ]
        lines += [
            "         * - Category",
            "           - Coverage",
            "           - OK Items",
            "           - Total Items",
        ]
        for level_name in self._report.config:
            data = self._report.coverage[level_name]
            lines.append(f"         * - {ref_fn(level_name)}")
            lines.append(f"           - {data.coverage:.1f}%")
            lines.append(f"           - {data.ok}")
            lines.append(f"           - {data.items}")
        lines.append("")
        lines += ["   .. grid-item::", "      :columns: 12 12 5 5", ""]
        lines += PolicyDiagramBuilder.build(self._report, indent=6)
        return lines


class IssuesListBuilder:
    """Build the index-page issues summary list.

    Each issue is rendered as a bullet with a granular tag derived from the
    message text (e.g. ``[MISSING — version mismatch]``) and a cross-page
    ``:ref:`` link to the corresponding item card.

    Usage::

        lines = IssuesListBuilder(report).build()
    """

    def __init__(self, report: Report):
        """Initialise the builder.

        Args:
            report: The loaded LOBSTER report.
        """
        self._report = report

    def build(self) -> list:
        """Return RST lines for the issues list.

        Returns:
            A list of RST bullet items, one per issue message.  If no issues
            exist, a single ``"No traceability issues found."`` line is returned.
        """
        # lobster-trace: rst_req.RST_Report_Issues_List
        # lobster-trace: UseCases.List_Findings
        lines = []
        found_any = False
        for item in sorted(
            self._report.items.values(), key=lambda x: x.location.sorting_key()
        ):
            if item.tracing_status in (Tracing_Status.OK, Tracing_Status.JUSTIFIED):
                continue
            for message in item.messages:
                tag = TracingClassifier.issue_tag(message)
                item_ref = (
                    f":ref:`{RstUtils.escape(item.name)}"
                    f" <{ItemNaming.item_label(item)}>`"
                )
                lines.append(f"* [{item.tracing_status.name} — {tag}] {item_ref}")
                found_any = True
        if not found_any:
            lines.append("No traceability issues found.")
        return lines
