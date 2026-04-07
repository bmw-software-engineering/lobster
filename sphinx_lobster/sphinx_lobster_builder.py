from __future__ import annotations

from os import path
from pathlib import Path
from typing import TYPE_CHECKING

from sphinx.builders.text import TextBuilder
from sphinx.locale import __
from sphinx.util.docutils import SphinxTranslator
from docutils import nodes

import json


class LobsterTranslator(SphinxTranslator):
    builder: LobsterBuilder

    def __init__(self, document: nodes.document, builder: LobsterBuilder) -> None:
        super().__init__(document, builder)

        self.source = ""
        self.docname = ""
        self.line = ""
        self.section_path = []
        self.tags = {}

        self.lobster_json = {}

        self.lobster_json["data"] = []

        self.lobster_json["generator"] = "sphinx_lobster"
        self.lobster_json["schema"] = "lobster-imp-trace"
        self.lobster_json["version"] = 3

    def _current_tag_name(self) -> str:
        section_str = ".".join(map(str, self.section_path))
        return self.docname + "." + section_str if self.docname else section_str

    def _ensure_tag(self, tag_name: str) -> None:
        """Create a lobster item for tag_name if it does not exist yet."""
        if tag_name not in self.tags:
            self.tags[tag_name] = {}
            self.tags[tag_name]["tag"] = "sphinx " + tag_name

            loc = {}
            loc["kind"] = "file"
            loc["file"] = self.source
            loc["line"] = (
                self.line if (isinstance(self.line, int) and self.line >= 1) else None
            )
            loc["column"] = None

            self.tags[tag_name]["location"] = loc

            self.tags[tag_name]["name"] = tag_name
            self.tags[tag_name]["messages"] = []
            self.tags[tag_name]["just_up"] = []
            self.tags[tag_name]["just_down"] = []
            self.tags[tag_name]["just_global"] = []
            self.tags[tag_name]["language"] = "rst"
            self.tags[tag_name]["kind"] = "section"
            self.tags[tag_name]["refs"] = []

            self.lobster_json["data"].append(self.tags[tag_name])

    def add_ref(self, name: str) -> None:
        """Record an upstream tracing reference (upstream-ref role)."""
        tag_name = self._current_tag_name()
        self._ensure_tag(tag_name)
        if name not in self.tags[tag_name]["refs"]:
            self.tags[tag_name]["refs"].append(name)

    def add_downstream_ref(self, name: str) -> None:
        """Record a downstream reference (downstream-ref role).

        Downstream refs are stored in just_down so lobster does not try to
        resolve them as upstream tracing targets.
        """
        tag_name = self._current_tag_name()
        self._ensure_tag(tag_name)
        if name not in self.tags[tag_name]["just_down"]:
            self.tags[tag_name]["just_down"].append(name)

    def visit_document(self, node: Element) -> None:
        self.source = node.attributes["source"]
        # Derive a short doc identifier from the source path.
        # Bazel sandboxes produce paths like .../.../_sources/sub/doc.rst
        source = self.source
        if "_sources/" in source:
            doc_rel = source.split("_sources/", 1)[1]
        else:
            doc_rel = Path(source).name
        if doc_rel.endswith(".rst"):
            doc_rel = doc_rel[:-4]
        # Convert slashes to dots and remove spaces for a clean identifier.
        self.docname = doc_rel.replace("/", ".").replace(" ", "")

    def depart_document(self, node: Element) -> None:
        self.body = json.dumps(self.lobster_json, indent=4)

    def visit_comment(self, node: Element) -> None:  # type: ignore[override]
        raise nodes.SkipNode

    def visit_toctree(self, node: Element) -> None:
        raise nodes.SkipNode

    def visit_index(self, node: Element) -> None:
        raise nodes.SkipNode

    def visit_tabular_col_spec(self, node: Element) -> None:
        raise nodes.SkipNode

    def visit_pending_xref(self, node: Element) -> None:
        # pending_xref nodes are normally resolved before write_doc runs,
        # but handle them here as a fallback.
        if node.get("refdomain") == "requirement":
            if node.get("reftype") == "upstream-ref":
                self.add_ref("req " + node.get("reftarget", ""))
            elif node.get("reftype") == "downstream-ref":
                self.add_downstream_ref("req " + node.get("reftarget", ""))
        raise nodes.SkipNode

    def visit_literal(self, node: Element) -> None:
        # Resolved xref roles become literal nodes whose classes carry the
        # role name: 'requirement-upstream-ref' or 'requirement-downstream-ref'.
        # Prefix with "req " to match the lobster-trlc requirement tag format.
        classes = node.get("classes", [])
        ref = "req " + node.astext()
        if "requirement-upstream-ref" in classes:
            self.add_ref(ref)
        elif "requirement-downstream-ref" in classes:
            self.add_downstream_ref(ref)

    def visit_paragraph(self, node: Element) -> None:
        self.line = node.line

    def visit_section(self, node: Element) -> None:
        names = node.attributes.get("names", [])
        self.section_path.append(names[0].replace(" ", "") if names else "")

    def depart_section(self, node: Element) -> None:
        self.section_path.pop()

    def unknown_visit(self, node: nodes.Node) -> None:
        pass

    def unknown_departure(self, node: nodes.Node) -> None:
        pass


class LobsterBuilder(TextBuilder):
    name = "lobster"
    format = "json"
    epilog = __("The text files are in %(outdir)s.")

    out_suffix = ".json"
    allow_parallel = True
    default_translator_class = LobsterTranslator

    def finish(self) -> None:
        super().finish()
        # Merge all per-document .json files written by write_doc() into a
        # single lobster implementation-trace file so consumers don't need a
        # separate merge step.
        merged: dict = {
            "data": [],
            "generator": "sphinx_lobster",
            "schema": "lobster-imp-trace",
            "version": 3,
        }
        for json_file in sorted(Path(self.outdir).rglob("*.json")):
            with open(json_file, encoding="utf-8") as fh:
                doc = json.load(fh)
            merged["data"].extend(doc.get("data", []))
        # NOTE: The output filename "_merged.lobster" is referenced by the
        # Bazel rule that is consuming this output and therefore needs to be
        # in sync.
        merged_path = path.join(self.outdir, "_merged.lobster")
        with open(merged_path, "w", encoding="utf-8") as fh:
            json.dump(merged, fh, indent=4)


def setup(app: Sphinx):
    app.add_builder(LobsterBuilder)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
