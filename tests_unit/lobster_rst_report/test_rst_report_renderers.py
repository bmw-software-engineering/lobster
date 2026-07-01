#!/usr/bin/env python3
# Copyright (C) 2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
# SPDX-License-Identifier: AGPL-3.0-or-later
import unittest
from unittest.mock import MagicMock
from lobster.common.items import Tracing_Status, Activity
from lobster.common.location import Void_Reference
from lobster.common.report import Report
from lobster.tools.core.rst_report._helpers import ItemNaming
from lobster.tools.core.rst_report._renderers import (
    ItemCardBuilder,
    LevelSectionBuilder,
    CoverageGridBuilder,
    IssuesListBuilder,
)


def _make_item(status):
    item = MagicMock()
    item.__class__ = Activity
    item.tag = MagicMock()
    item.tag.hash.return_value = "abc123"
    item.tracing_status = status
    item.name = "test.item"
    item.messages = []
    item.ref_down = []
    item.ref_up = []
    item.just_global = []
    item.just_up = []
    item.just_down = []
    item.framework = "TestFramework"
    item.kind = "test"
    item.location = MagicMock()
    item.location.__class__ = Void_Reference
    item.location.sorting_key.return_value = (0, 0)
    return item


def _make_report(items=None):
    report = MagicMock(spec=Report)
    report.items = items if items is not None else {}
    return report


class TestItemCardBuilderDropdownState(unittest.TestCase):
    def _build(self, status):
        return "\n".join(ItemCardBuilder(_make_item(status), _make_report()).build())

    def test_partial_item_renders_open(self):
        text = self._build(Tracing_Status.PARTIAL)
        self.assertIn("[PARTIAL]", text)
        self.assertIn(":open:", text)

    def test_error_item_renders_open(self):
        text = self._build(Tracing_Status.ERROR)
        self.assertIn("[ERROR]", text)
        self.assertIn(":open:", text)

    def test_missing_item_renders_open(self):
        text = self._build(Tracing_Status.MISSING)
        self.assertIn("[MISSING]", text)
        self.assertIn(":open:", text)

    def test_ok_item_renders_closed(self):
        text = self._build(Tracing_Status.OK)
        self.assertIn("[OK]", text)
        self.assertNotIn(":open:", text)

    def test_justified_item_renders_closed(self):
        text = self._build(Tracing_Status.JUSTIFIED)
        self.assertIn("[JUSTIFIED]", text)
        self.assertNotIn(":open:", text)


class TestItemCardBuilderAnchor(unittest.TestCase):
    def test_anchor_label_contains_hash(self):
        item = _make_item(Tracing_Status.OK)
        item.tag.hash.return_value = "deadbeef"
        text = "\n".join(ItemCardBuilder(item, _make_report()).build())
        self.assertIn("lobster-item-deadbeef", text)


class TestItemCardBuilderVoidLocation(unittest.TestCase):
    def test_void_location_renders_unknown_location(self):
        item = _make_item(Tracing_Status.OK)
        text = "\n".join(ItemCardBuilder(item, _make_report()).build())
        self.assertIn("unknown location", text)


class TestItemCardBuilderRefResolution(unittest.TestCase):
    def test_unresolved_down_ref_is_annotated(self):
        item = _make_item(Tracing_Status.MISSING)
        unresolved = MagicMock()
        unresolved.key.return_value = "req example.unknown"
        item.ref_down = [unresolved]
        text = "\n".join(ItemCardBuilder(item, _make_report()).build())
        self.assertIn("(unresolved)", text)
        self.assertIn("req example.unknown", text)

    def test_resolved_down_ref_produces_ref_link(self):
        target = _make_item(Tracing_Status.OK)
        target.name = "example.req_foo"
        target.tag.hash.return_value = "feed1234"
        item = _make_item(Tracing_Status.MISSING)
        ref = MagicMock()
        ref.key.return_value = "req example.req_foo"
        item.ref_down = [ref]
        report = _make_report(items={"req example.req_foo": target})
        text = "\n".join(ItemCardBuilder(item, report).build())
        self.assertIn(":ref:", text)
        self.assertIn("lobster-item-feed1234", text)
        self.assertNotIn("(unresolved)", text)


class TestLocationLinkVoidReference(unittest.TestCase):
    def test_void_reference_returns_unknown_location(self):
        void_loc = MagicMock(spec=Void_Reference)
        result = ItemNaming.location_link(void_loc)
        self.assertEqual(result, "unknown location")


class TestLevelSectionBuilderEdgeCases(unittest.TestCase):
    def test_empty_items_list_returns_no_items_message(self):
        lines = LevelSectionBuilder([], _make_report()).build()
        self.assertIn("No items recorded at this level.", lines)

    def test_issues_before_ok_items(self):
        ok_item = _make_item(Tracing_Status.OK)
        ok_item.name = "ok.item"
        ok_item.tag.hash.return_value = "ok000000"
        issue_item = _make_item(Tracing_Status.MISSING)
        issue_item.name = "missing.item"
        issue_item.tag.hash.return_value = "miss0000"
        lines = LevelSectionBuilder([ok_item, issue_item], _make_report()).build()
        text = "\n".join(lines)
        ok_pos = text.find("lobster-item-ok000000")
        miss_pos = text.find("lobster-item-miss0000")
        self.assertGreater(ok_pos, miss_pos, "Issue items must precede OK items")

    def test_all_ok_items_renders_without_error(self):
        items = [_make_item(Tracing_Status.OK) for _ in range(3)]
        for i, it in enumerate(items):
            it.tag.hash.return_value = f"ok{i:06d}"
            it.name = f"item_{i}"
        lines = LevelSectionBuilder(items, _make_report()).build()
        self.assertTrue(len(lines) > 0)


# ---------------------------------------------------------------------------
# CoverageGridBuilder
# ---------------------------------------------------------------------------

def _make_coverage(level, items_count, ok_count, coverage_pct):
    cov = MagicMock()
    cov.level = level
    cov.items = items_count
    cov.ok = ok_count
    cov.coverage = coverage_pct
    return cov


def _make_level_config(name, kind, traces=None):
    lv = MagicMock()
    lv.name = name
    lv.kind = kind
    lv.traces = traces or []
    return lv


def _make_report_with_coverage(levels):
    """Create a report mock with config and coverage data.

    Args:
        levels: list of (name, kind, items, ok, coverage, traces) tuples.
    """
    report = MagicMock(spec=Report)
    config = {}
    coverage = {}
    for name, kind, items_count, ok_count, cov_pct, traces in levels:
        config[name] = _make_level_config(name, kind, traces)
        coverage[name] = _make_coverage(name, items_count, ok_count, cov_pct)
    report.config = config
    report.coverage = coverage
    report.items = {}
    return report


class TestCoverageGridBuilder(unittest.TestCase):
    # lobster-trace: UseCases.RST_Coverage_in_output

    def test_coverage_table_contains_headers(self):
        report = _make_report_with_coverage([
            ("Requirements", "requirements", 10, 8, 80.0, []),
        ])
        lines = CoverageGridBuilder(report).build(lambda n: f"REF({n})")
        text = "\n".join(lines)
        self.assertIn("Category", text)
        self.assertIn("Coverage", text)
        self.assertIn("OK Items", text)
        self.assertIn("Total Items", text)

    def test_coverage_table_contains_level_data(self):
        report = _make_report_with_coverage([
            ("Software Reqs", "requirements", 20, 15, 75.0, []),
        ])
        lines = CoverageGridBuilder(report).build(lambda n: f"REF({n})")
        text = "\n".join(lines)
        self.assertIn("REF(Software Reqs)", text)
        self.assertIn("75.0%", text)
        self.assertIn("15", text)
        self.assertIn("20", text)

    def test_coverage_calls_ref_fn_for_each_level(self):
        report = _make_report_with_coverage([
            ("Reqs", "requirements", 5, 5, 100.0, []),
            ("Code", "implementation", 3, 2, 66.7, []),
        ])
        called_with = []
        def ref_fn(n):
            called_with.append(n)
            return f"REF({n})"
        CoverageGridBuilder(report).build(ref_fn)
        self.assertIn("Reqs", called_with)
        self.assertIn("Code", called_with)

    def test_coverage_grid_contains_graphviz_directive(self):
        report = _make_report_with_coverage([
            ("Reqs", "requirements", 5, 5, 100.0, []),
        ])
        lines = CoverageGridBuilder(report).build(lambda n: n)
        text = "\n".join(lines)
        self.assertIn(".. graphviz::", text)
        self.assertIn("digraph tracing_policy", text)


# ---------------------------------------------------------------------------
# IssuesListBuilder
# ---------------------------------------------------------------------------

class TestIssuesListBuilder(unittest.TestCase):
    # lobster-trace: UseCases.RST_Missing_tracing_policy_violation_in_output

    def test_all_ok_items_shows_no_issues(self):
        report = _make_report()
        ok_item = _make_item(Tracing_Status.OK)
        ok_item.name = "good.item"
        report.items = {"req good.item": ok_item}
        lines = IssuesListBuilder(report).build()
        text = "\n".join(lines)
        self.assertIn("No traceability issues found.", text)

    def test_missing_item_appears_in_issues(self):
        report = _make_report()
        bad_item = _make_item(Tracing_Status.MISSING)
        bad_item.name = "bad.item"
        bad_item.messages = ["missing up reference"]
        report.items = {"req bad.item": bad_item}
        lines = IssuesListBuilder(report).build()
        text = "\n".join(lines)
        self.assertIn("MISSING", text)
        self.assertIn("bad.item", text)
        self.assertNotIn("No traceability issues found.", text)

    def test_issue_tag_formatting(self):
        report = _make_report()
        item = _make_item(Tracing_Status.MISSING)
        item.name = "req.test"
        item.messages = ["missing reference to Verification Test"]
        report.items = {"req req.test": item}
        lines = IssuesListBuilder(report).build()
        text = "\n".join(lines)
        self.assertIn("no trace to:", text)

    def test_justified_item_not_in_issues(self):
        report = _make_report()
        just_item = _make_item(Tracing_Status.JUSTIFIED)
        just_item.name = "just.item"
        just_item.messages = []
        report.items = {"req just.item": just_item}
        lines = IssuesListBuilder(report).build()
        text = "\n".join(lines)
        self.assertIn("No traceability issues found.", text)


if __name__ == "__main__":
    unittest.main()
