import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from docutils import nodes
from sphinx_lobster_builder import LobsterBuilder, LobsterTranslator

def _make_translator(source="", docname="", section_path=None) -> LobsterTranslator:
    """Create a LobsterTranslator with SphinxTranslator.__init__ mocked out."""
    with patch.object(
            LobsterTranslator, "__init__", lambda self, doc, builder: None
    ):
        translator = LobsterTranslator.__new__(LobsterTranslator)

    translator.document = MagicMock(spec=nodes.document)
    translator.builder = MagicMock(spec=LobsterBuilder)
    translator.source = source
    translator.docname = docname
    translator.line = ""
    translator.section_path = section_path if section_path is not None else []
    translator.tags = {}
    translator.lobster_json = {
        "data": [],
        "generator": "sphinx_lobster",
        "schema": "lobster-imp-trace",
        "version": 3,
    }
    return translator

class TestAddRef(unittest.TestCase):

    def test_reference_will_be_added(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["test_section"]
        translator.add_ref("test_ref")

        tag = translator.tags["test_doc.test_section"]
        self.assertIn("test_ref", tag["refs"])

    def test_no_duplicate_ref_added(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["test_section"]
        translator.add_ref("test_ref")
        translator.add_ref("test_ref")

        tag = translator.tags["test_doc.test_section"]
        self.assertEqual(tag["refs"].count("test_ref"), 1)

    def test_different_refs_can_be_added(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["test_section"]
        translator.add_ref("test_ref_1")
        translator.add_ref("test_ref_2")

        tag = translator.tags["test_doc.test_section"]
        self.assertIn("test_ref_1", tag["refs"])
        self.assertIn("test_ref_2", tag["refs"])

class TestAddDownstreamRef(unittest.TestCase):

    def test_downstream_ref_will_be_added(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["test_section"]
        translator.add_downstream_ref("test_downstream_ref")

        tag = translator.tags["test_doc.test_section"]
        self.assertIn("test_downstream_ref", tag["just_down"])

    def test_no_duplicate_downstream_ref_added(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["test_section"]
        translator.add_downstream_ref("test_downstream_ref")
        translator.add_downstream_ref("test_downstream_ref")

        tag = translator.tags["test_doc.test_section"]
        self.assertEqual(tag["just_down"].count("test_downstream_ref"), 1)

    def test_different_downstream_refs_can_be_added(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["test_section"]
        translator.add_downstream_ref("test_downstream_ref_1")
        translator.add_downstream_ref("test_downstream_ref_2")

        tag = translator.tags["test_doc.test_section"]
        self.assertIn("test_downstream_ref_1", tag["just_down"])
        self.assertIn("test_downstream_ref_2", tag["just_down"])


class TestVisitDocument(unittest.TestCase):

    def test_visit_document_creates_correct_doc_name(self):
        translator = _make_translator(docname="test_doc")
        document_node = MagicMock(spec=nodes.document)
        source_node_value = ".../.../_sources/sub/doc.rst"
        document_node.attributes = {"source": source_node_value}
        translator.visit_document(document_node)

        self.assertEqual(source_node_value, translator.source)
        self.assertEqual("sub.doc", translator.docname)

    def test_visit_document_removes_spaces_from_doc_name(self):
        translator = _make_translator(docname="test_doc")
        document_node = MagicMock(spec=nodes.document)
        source_node_value = ".../.../_sources/sub folder/doc"
        document_node.attributes = {"source": source_node_value}
        translator.visit_document(document_node)

        self.assertEqual(source_node_value, translator.source)
        self.assertEqual("subfolder.doc", translator.docname)

    def test_visit_document_handles_short_doc_name(self):
        translator = _make_translator(docname="test_doc")
        document_node = MagicMock(spec=nodes.document)
        source_node_value = "sub/doc.rst"
        document_node.attributes = {"source": source_node_value}
        translator.visit_document(document_node)

        self.assertEqual(source_node_value, translator.source)
        self.assertEqual("doc", translator.docname)

class TestVisitComment(unittest.TestCase):
    def test_visit_comment_skips_node(self):
        translator = _make_translator(docname="test_doc")
        comment_node = MagicMock(spec=nodes.comment)

        with self.assertRaises(nodes.SkipNode):
            translator.visit_comment(comment_node)

class TestVisitToctree(unittest.TestCase):
    def test_visit_toctree_skips_node(self):
        translator = _make_translator(docname="test_doc")
        toctree_node = MagicMock(spec=nodes.Element)

        with self.assertRaises(nodes.SkipNode):
            translator.visit_toctree(toctree_node)

class TestVisitIndex(unittest.TestCase):
    def test_visit_index_skips_node(self):
        translator = _make_translator(docname="test_doc")
        index_node = MagicMock(spec=nodes.Element)

        with self.assertRaises(nodes.SkipNode):
            translator.visit_index(index_node)

class TestVisitTabularColSpec(unittest.TestCase):
    def test_visit_tabular_col_spec_skips_node(self):
        translator = _make_translator(docname="test_doc")
        tabular_col_spec_node = MagicMock(spec=nodes.Element)

        with self.assertRaises(nodes.SkipNode):
            translator.visit_tabular_col_spec(tabular_col_spec_node)

class TestDepartDocument(unittest.TestCase):
    def test_depart_document_produces_valid_json(self):
        translator = _make_translator(docname="test_doc")
        translator.lobster_json["data"] = [{"name": "test_tag"}]
        document_node = MagicMock(spec=nodes.document)
        translator.depart_document(document_node)

        expected_json = json.dumps(translator.lobster_json, indent=4)
        self.assertEqual(expected_json, translator.body)

class TestVisitPendingXref(unittest.TestCase):
    def test_visit_pending_xref_skips_node(self):
        translator = _make_translator(docname="test_doc")
        pending_xref_node = MagicMock(spec=nodes.document)

        with self.assertRaises(nodes.SkipNode):
            translator.visit_pending_xref(pending_xref_node)

    def test_visit_pending_xref_adds_upstream_ref(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["test_section"]
        pending_xref_node = nodes.Element()

        pending_xref_node["reftype"] = "upstream-ref"
        pending_xref_node["refdomain"] = "requirement"
        pending_xref_node["reftarget"] = "my_ref_target"

        with self.assertRaises(nodes.SkipNode):
            translator.visit_pending_xref(pending_xref_node)
        tag = translator.tags["test_doc.test_section"]
        self.assertIn("req my_ref_target", tag["refs"])

    def test_visit_pending_xref_adds_downstream_ref(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["test_section"]
        pending_xref_node = nodes.Element()

        pending_xref_node["reftype"] = "downstream-ref"
        pending_xref_node["refdomain"] = "requirement"
        pending_xref_node["reftarget"] = "my_ref_target"

        with self.assertRaises(nodes.SkipNode):
            translator.visit_pending_xref(pending_xref_node)
        tag = translator.tags["test_doc.test_section"]
        self.assertIn("req my_ref_target", tag["just_down"])

class TestVisitLiteral(unittest.TestCase):
    def test_visit_literal_add_upstream_ref(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["test_section"]
        literal_node = nodes.Element()

        literal_node["classes"] = ["requirement-upstream-ref"]

        translator.visit_literal(literal_node)

        tag = translator.tags["test_doc.test_section"]
        self.assertIn("req ", tag["refs"])

    def test_visit_literal_add_downstream_ref(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["test_section"]
        literal_node = nodes.Element()
        literal_node["classes"] = ["requirement-downstream-ref"]

        translator.visit_literal(literal_node)

        tag = translator.tags["test_doc.test_section"]
        self.assertIn("req ", tag["just_down"])

    def test_visit_literal_no_update_if_no_classes(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["test_section"]
        literal_node = nodes.Element()
        literal_node["classes"] = []

        translator.visit_literal(literal_node)

        self.assertEqual(len(translator.tags), 0)

class TestVisitParagraph(unittest.TestCase):
    def test_visit_paragraph_updates_line(self):
        translator = _make_translator(docname="test_doc")
        paragraph_node = MagicMock(spec=nodes.paragraph)
        paragraph_node.line = 42

        translator.visit_paragraph(paragraph_node)
        self.assertEqual(translator.line, 42)

class TestVisitSection(unittest.TestCase):
    def test_visit_section_updates_section_path(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["Section0"]
        section_node = MagicMock(spec=nodes.section)
        section_node.attributes = {"names": ["Section 1", "Another name"]}

        translator.visit_section(section_node)
        self.assertEqual(translator.section_path, ["Section0", "Section1"])

    def test_visit_section_adds_empty_section_path(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["Section0"]
        section_node = nodes.Element()

        translator.visit_section(section_node)
        self.assertEqual(translator.section_path, ["Section0", ""])

class TestDepartSection(unittest.TestCase):
    def test_depart_section_pops_section_path(self):
        translator = _make_translator(docname="test_doc")
        translator.section_path = ["Section0", "Section1"]
        section_node = MagicMock(spec=nodes.section)

        translator.depart_section(section_node)
        self.assertEqual(translator.section_path, ["Section0"])

class TestLobsterBuilderFinish(unittest.TestCase):
    """Testing the LobsterBuilder.finish method"""

    def _write_json(self, directory, filename, data):
        filepath = os.path.join(directory, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(data, fh)

    @patch("sphinx_lobster_builder.TextBuilder.finish")
    def test_finish_merges_json_files(self, mock_super_finish):
        with tempfile.TemporaryDirectory() as tmpdir:
            doc1 = {
                "data": [{"tag": "sphinx doc1.sec", "name": "doc1.sec"}],
                "generator": "sphinx_lobster",
                "schema": "lobster-imp-trace",
                "version": 3,
            }
            doc2 = {
                "data": [{"tag": "sphinx doc2.sec", "name": "doc2.sec"}],
                "generator": "sphinx_lobster",
                "schema": "lobster-imp-trace",
                "version": 3,
            }
            self._write_json(tmpdir, "doc1.json", doc1)
            self._write_json(tmpdir, "doc2.json", doc2)

            builder = LobsterBuilder.__new__(LobsterBuilder)
            builder.outdir = tmpdir

            builder.finish()

            mock_super_finish.assert_called_once()

            merged_path = os.path.join(tmpdir, "_merged.lobster")
            self.assertTrue(os.path.exists(merged_path))

            with open(merged_path, encoding="utf-8") as fh:
                merged = json.load(fh)

            self.assertEqual(merged["generator"], "sphinx_lobster")
            self.assertEqual(merged["schema"], "lobster-imp-trace")
            self.assertEqual(merged["version"], 3)
            self.assertEqual(len(merged["data"]), 2)

            names = [item["name"] for item in merged["data"]]
            self.assertIn("doc1.sec", names)
            self.assertIn("doc2.sec", names)

    @patch("sphinx_lobster_builder.TextBuilder.finish")
    def test_finish_empty_output_directory(self, mock_super_finish):
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = LobsterBuilder.__new__(LobsterBuilder)
            builder.outdir = tmpdir

            builder.finish()

            merged_path = os.path.join(tmpdir, "_merged.lobster")
            with open(merged_path, encoding="utf-8") as fh:
                merged = json.load(fh)

            self.assertEqual(merged["data"], [])

    @patch("sphinx_lobster_builder.TextBuilder.finish")
    def test_finish_merges_subdirectory_json(self, mock_super_finish):
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = os.path.join(tmpdir, "subdir")
            os.makedirs(sub)
            doc = {
                "data": [{"tag": "sphinx sub.doc"}],
                "generator": "sphinx_lobster",
                "schema": "lobster-imp-trace",
                "version": 3,
            }
            self._write_json(sub, "nested.json", doc)

            builder = LobsterBuilder.__new__(LobsterBuilder)
            builder.outdir = tmpdir

            builder.finish()

            merged_path = os.path.join(tmpdir, "_merged.lobster")
            with open(merged_path, encoding="utf-8") as fh:
                merged = json.load(fh)

            self.assertEqual(len(merged["data"]), 1)
            self.assertEqual(merged["data"][0]["tag"], "sphinx sub.doc")


if __name__ == "__main__":
    unittest.main()

