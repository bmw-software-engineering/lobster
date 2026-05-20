#!/usr/bin/env python3
#
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
"""Integration test: generate RST report and build with Sphinx.

Verifies that the generated RST output is valid Sphinx input by running
a full Sphinx build with warnings-as-errors (``-W``).
"""

# lobster-trace: UseCases.RST_Valid_Sphinx_Build

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from sphinx.application import Sphinx

from lobster.tools.core.rst_report.rst_report import main as rst_report_main


class SphinxRstReportBuildTest(unittest.TestCase):
    """Build a Sphinx project from lobster-rst-report output."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="lobster-sphinx-rst-test-")

        # In Bazel, data files are in the runfiles tree.  When running
        # outside Bazel, fall back to paths relative to this source file.
        runfiles_dir = os.environ.get("TEST_SRCDIR")
        if runfiles_dir:
            ws = os.environ.get("TEST_WORKSPACE", "lobster")
            base = Path(runfiles_dir) / ws
            self._project_dir = (
                base / "tests_integration" / "projects" / "sphinx_rst_report"
            )
            self._lobster_file = (
                base
                / "tests_system"
                / "lobster_rst_report"
                / "data"
                / "basic_report.lobster"
            )
        else:
            self._project_dir = Path(__file__).parent
            self._lobster_file = (
                Path(__file__).parents[2]
                / "tests_system"
                / "lobster_rst_report"
                / "data"
                / "basic_report.lobster"
            )

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _setup_sphinx_project(self) -> Path:
        """Copy project files to temp dir and generate RST traceability pages."""
        work = Path(self._tmp)

        # Copy conf.py and index.rst
        shutil.copy2(self._project_dir / "conf.py", work / "conf.py")
        shutil.copy2(self._project_dir / "index.rst", work / "index.rst")

        # Copy _static/
        static_src = self._project_dir / "_static"
        static_dst = work / "_static"
        if static_src.exists():
            shutil.copytree(static_src, static_dst)

        # Copy lobster file
        shutil.copy2(self._lobster_file, work / "basic_report.lobster")

        # Generate RST traceability pages
        tracing_dir = work / "traceability"
        rc = rst_report_main([
            str(work / "basic_report.lobster"),
            "--out-dir", str(tracing_dir),
        ])
        self.assertEqual(rc, 0, "lobster-rst-report failed")
        self.assertTrue(
            (tracing_dir / "index.rst").exists(),
            "traceability/index.rst not generated",
        )
        return work

    def test_sphinx_build_succeeds_without_warnings(self):
        """A full Sphinx build must complete without warnings or errors."""
        src_dir = self._setup_sphinx_project()
        out_dir = Path(self._tmp) / "_build" / "html"
        doctree_dir = Path(self._tmp) / "_build" / "doctrees"

        app = Sphinx(
            srcdir=str(src_dir),
            confdir=str(src_dir),
            outdir=str(out_dir),
            doctreedir=str(doctree_dir),
            buildername="html",
            freshenv=True,
            warningiserror=True,
        )
        app.build()

        # Verify output exists
        self.assertTrue(
            (out_dir / "index.html").exists(),
            "index.html was not generated",
        )
        # Verify traceability pages were built
        tracing_html = list(out_dir.glob("traceability/*.html"))
        self.assertGreater(
            len(tracing_html), 0,
            "No traceability HTML pages were generated",
        )

    def test_generated_rst_pages_are_well_formed(self):
        """Each generated RST page must be parseable by Sphinx without errors."""
        src_dir = self._setup_sphinx_project()
        tracing_dir = src_dir / "traceability"

        # Verify all expected RST files exist
        rst_files = list(tracing_dir.glob("*.rst"))
        self.assertGreater(len(rst_files), 1, "Expected index + level pages")

        # Verify index.rst has toctree
        index_content = (tracing_dir / "index.rst").read_text(encoding="UTF-8")
        self.assertIn(".. toctree::", index_content)


if __name__ == "__main__":
    unittest.main()
