import subprocess
import unittest
from unittest.mock import MagicMock, patch

from lobster.tools.core.rst_report._helpers import (
    RstUtils,
    ItemNaming,
    TracingClassifier,
    PolicyDiagramBuilder,
)
from lobster.tools.core.rst_report._renderers import _build_page_map
from lobster.common.graphviz_utils import is_dot_available
from lobster.common.location import (
    Void_Reference,
    File_Reference,
    Github_Reference,
    Codebeamer_Reference,
)


# ---------------------------------------------------------------------------
# RstUtils
# ---------------------------------------------------------------------------

class TestRstUtilsEscape(unittest.TestCase):
    def test_backslash_is_escaped(self):
        self.assertEqual(RstUtils.escape("a\\b"), "a\\\\b")

    def test_backtick_is_escaped(self):
        self.assertEqual(RstUtils.escape("a`b"), "a\\`b")

    def test_asterisk_is_escaped(self):
        self.assertEqual(RstUtils.escape("a*b"), "a\\*b")

    def test_underscore_is_escaped(self):
        self.assertEqual(RstUtils.escape("a_b"), "a\\_b")

    def test_pipe_is_escaped(self):
        self.assertEqual(RstUtils.escape("a|b"), "a\\|b")

    def test_plain_text_unchanged(self):
        self.assertEqual(RstUtils.escape("hello world"), "hello world")

    def test_multiple_special_chars(self):
        result = RstUtils.escape("a_b*c`d")
        self.assertIn("\\_", result)
        self.assertIn("\\*", result)
        self.assertIn("\\`", result)


class TestRstUtilsHeading(unittest.TestCase):
    def test_underline_only(self):
        lines = RstUtils.heading("Hello", "=")
        self.assertEqual(lines, ["Hello", "====="])

    def test_overline_and_underline(self):
        lines = RstUtils.heading("Hi", "#", overline=True)
        self.assertEqual(lines, ["##", "Hi", "##"])

    def test_heading_length_matches_text(self):
        text = "Some Long Title"
        lines = RstUtils.heading(text, "-")
        self.assertEqual(len(lines[1]), len(text))


# ---------------------------------------------------------------------------
# ItemNaming
# ---------------------------------------------------------------------------

class TestItemNamingLevelPageName(unittest.TestCase):
    def test_spaces_become_underscores(self):
        self.assertEqual(ItemNaming.level_page_name("System Requirements"), "system_requirements")

    def test_hyphens_become_underscores(self):
        self.assertEqual(ItemNaming.level_page_name("My-Level"), "my_level")

    def test_consecutive_underscores_collapsed(self):
        result = ItemNaming.level_page_name("A  B")
        self.assertNotIn("__", result)

    def test_leading_trailing_underscores_stripped(self):
        result = ItemNaming.level_page_name(" level ")
        self.assertFalse(result.startswith("_"))
        self.assertFalse(result.endswith("_"))

    def test_empty_like_input_returns_level(self):
        self.assertEqual(ItemNaming.level_page_name("___"), "level")

    def test_mixed_special_chars(self):
        result = ItemNaming.level_page_name("A/B (C)")
        self.assertNotIn("/", result)
        self.assertNotIn("(", result)
        self.assertNotIn(")", result)


class TestBuildPageMap(unittest.TestCase):
    """Tests for _build_page_map collision resolution."""

    def _make_report(self, level_names):
        """Return a minimal mock with just the config attribute."""
        report = MagicMock()
        report.config = {name: MagicMock() for name in level_names}
        return report

    def test_unique_names_produce_unique_stems(self):
        report = self._make_report(["System Requirements", "Code"])
        page_map = _build_page_map(report)
        stems = list(page_map.values())
        self.assertEqual(len(stems), len(set(stems)))

    def test_duplicate_slugs_are_disambiguated(self):
        # "A B" and "A-B" both collapse to "a_b"
        report = self._make_report(["A B", "A-B"])
        page_map = _build_page_map(report)
        stems = list(page_map.values())
        self.assertEqual(len(stems), len(set(stems)), "Duplicate stems not disambiguated")


# ---------------------------------------------------------------------------
# TracingClassifier
# ---------------------------------------------------------------------------

class TestTracingClassifierCategorize(unittest.TestCase):
    def test_up_reference_message(self):
        down, up, gen = TracingClassifier.categorize(["missing up reference"])
        self.assertIn("missing up reference", up)
        self.assertEqual(down, [])
        self.assertEqual(gen, [])

    def test_down_reference_message(self):
        down, up, gen = TracingClassifier.categorize(["missing down reference"])
        self.assertIn("missing down reference", down)
        self.assertEqual(up, [])
        self.assertEqual(gen, [])

    def test_missing_reference_to_message(self):
        msg = "missing reference to Verification Test"
        down, _, _ = TracingClassifier.categorize([msg])
        self.assertIn(msg, down)

    def test_tracing_destination_message(self):
        msg = "tracing destination req X has version 2 (expected 1)"
        down, _, _ = TracingClassifier.categorize([msg])
        self.assertIn(msg, down)

    def test_unknown_tracing_target(self):
        msg = "unknown tracing target req example.foo"
        down, _, _ = TracingClassifier.categorize([msg])
        self.assertIn(msg, down)

    def test_general_message(self):
        msg = "some unrecognised error"
        _, _, gen = TracingClassifier.categorize([msg])
        self.assertIn(msg, gen)


class TestTracingClassifierIssueTag(unittest.TestCase):
    def test_version_mismatch(self):
        self.assertEqual(
            TracingClassifier.issue_tag("tracing destination X has version 2 (expected 1)"),
            "version mismatch",
        )

    def test_unknown_target(self):
        tag = TracingClassifier.issue_tag("unknown tracing target req foo")
        self.assertIn("unknown target", tag)

    def test_missing_up_reference(self):
        self.assertEqual(
            TracingClassifier.issue_tag("missing up reference"),
            "no upward trace",
        )

    def test_missing_reference_to(self):
        tag = TracingClassifier.issue_tag("missing reference to Verification Test")
        self.assertIn("no trace to", tag)

    def test_missing_down_reference(self):
        self.assertEqual(
            TracingClassifier.issue_tag("missing down reference"),
            "no downward trace",
        )

    def test_fallback_escapes_original(self):
        tag = TracingClassifier.issue_tag("some_underscored_message")
        self.assertIn("\\_", tag)


# ---------------------------------------------------------------------------
# PolicyDiagramBuilder
# ---------------------------------------------------------------------------

class TestPolicyDiagramBuilderDotEscape(unittest.TestCase):
    def test_double_quote_escaped(self):
        self.assertEqual(PolicyDiagramBuilder.dot_escape('a"b'), 'a\\"b')

    def test_backslash_escaped(self):
        self.assertEqual(PolicyDiagramBuilder.dot_escape("a\\b"), "a\\\\b")

    def test_plain_text_unchanged(self):
        self.assertEqual(PolicyDiagramBuilder.dot_escape("hello"), "hello")


# ---------------------------------------------------------------------------
# is_dot_available
# ---------------------------------------------------------------------------

class TestIsDotAvailable(unittest.TestCase):
    def test_returns_true_when_dot_succeeds(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = None
            self.assertTrue(is_dot_available())

    def test_returns_false_when_dot_not_found(self):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            self.assertFalse(is_dot_available())

    def test_returns_false_when_dot_times_out(self):
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("dot", 5)):
            self.assertFalse(is_dot_available())

    def test_explicit_dot_path_is_used(self):
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = None
            is_dot_available(dot="/usr/bin/dot")
            called_cmd = mock_run.call_args[0][0]
            self.assertEqual(called_cmd[0], "/usr/bin/dot")

    def test_returns_false_when_dot_returns_nonzero(self):
        with patch(
            "subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "dot"),
        ):
            self.assertFalse(is_dot_available())


# ---------------------------------------------------------------------------
# ItemNaming.location_link
# ---------------------------------------------------------------------------

class TestLocationLink(unittest.TestCase):
    # lobster-trace: UseCases.RST_Codebeamer_Links_In_Output
    # lobster-trace: UseCases.RST_Source_location_in_output

    def test_void_reference_returns_unknown(self):
        loc = Void_Reference()
        self.assertEqual(ItemNaming.location_link(loc), "unknown location")

    def test_file_reference_no_source_root(self):
        loc = File_Reference("src/main.cpp", line=42)
        result = ItemNaming.location_link(loc)
        self.assertIn("src/main.cpp", result)
        self.assertIn("`__", result)  # anonymous hyperlink
        self.assertIn("<src/main.cpp>", result)

    def test_file_reference_with_source_root(self):
        loc = File_Reference("src/main.cpp", line=10)
        result = ItemNaming.location_link(loc, source_root="https://example.com/")
        self.assertIn("https://example.com/src/main.cpp", result)
        self.assertIn("`__", result)

    def test_file_reference_with_line_number(self):
        loc = File_Reference("foo.py", line=7)
        result = ItemNaming.location_link(loc)
        self.assertIn("foo.py:7", result)

    def test_file_reference_without_line_number(self):
        loc = File_Reference("foo.py")
        result = ItemNaming.location_link(loc)
        self.assertIn("foo.py", result)
        self.assertNotIn("foo.py:", result)

    def test_github_reference_with_line(self):
        loc = Github_Reference(
            "https://github.com/org/repo", "src/main.cpp", 42, "abc123"
        )
        result = ItemNaming.location_link(loc)
        self.assertIn("github.com/org/repo/blob/abc123/src/main.cpp", result)
        self.assertIn("#L42", result)
        self.assertIn("`__", result)

    def test_github_reference_without_line(self):
        loc = Github_Reference(
            "https://github.com/org/repo", "README.md", None, "abc123"
        )
        result = ItemNaming.location_link(loc)
        self.assertIn("github.com/org/repo/blob/abc123/README.md", result)
        self.assertNotIn("#L", result)

    def test_codebeamer_reference_without_version(self):
        loc = Codebeamer_Reference("https://cb.example.com", 1, 999)
        result = ItemNaming.location_link(loc)
        self.assertIn("cb.example.com/issue/999", result)
        self.assertNotIn("?version=", result)
        self.assertIn("`__", result)

    def test_codebeamer_reference_with_version(self):
        loc = Codebeamer_Reference("https://cb.example.com", 1, 999, version=5)
        result = ItemNaming.location_link(loc)
        self.assertIn("cb.example.com/issue/999?version=5", result)

    def test_codebeamer_reference_with_name(self):
        loc = Codebeamer_Reference(
            "https://cb.example.com", 1, 999, name="My Requirement"
        )
        result = ItemNaming.location_link(loc)
        self.assertIn("My Requirement", result)
        self.assertIn("cb item 999", result)

    def test_unknown_location_type_returns_escaped_text(self):
        """A location type not handled by any branch should be escaped."""
        class CustomLocation:  # pylint: disable=too-few-public-methods
            def __str__(self):
                return "custom_loc_42"
        loc = CustomLocation()
        result = ItemNaming.location_link(loc)
        self.assertIn("custom\\_loc\\_42", result)


if __name__ == "__main__":
    unittest.main()
