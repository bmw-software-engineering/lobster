from os import path
from unittest import TestCase
from lobster.common.errors import PathError
from lobster.common.file_collector import FileCollector


class FileCollectorTest(TestCase):
    def test_extension_validation(self):
        with self.assertRaises(ValueError) as context:
            FileCollector(extensions=[".screw", "hammer", "wire cutter"], directory_exclude_patterns=[])
        self.assertEqual(
            str(context.exception), "Extension 'hammer' must start with a dot (.)"
        )

    def test_add_files(self):
        collector = FileCollector(extensions=[".drill", ".saw"], directory_exclude_patterns=[])

        # Test adding files with valid extensions
        collector.add_file("test.drill", throw_on_mismatch=False)
        collector.add_file(path.join("folder", "test.saw"), throw_on_mismatch=False)
        self.assertIn("test.drill", collector.files)
        self.assertIn(path.join("folder", "test.saw"), collector.files)

        # Test adding files with invalid extensions
        collector.add_file("test.chisel", throw_on_mismatch=False)
        self.assertNotIn("test.chisel", collector.files)

        # Test adding files with invalid extensions and throwing an error
        with self.assertRaises(PathError) as context:
            collector.add_file("test.grinder", throw_on_mismatch=True)
        self.assertEqual(
            str(context.exception),
            "File test.grinder does not have a valid extension. "
            "Expected one of .drill, .saw."
        )

    def test_add_files_with_compound_extension(self):
        collector = FileCollector(
            extensions=[".rsl", ".trlc", ".trlc.md"], directory_exclude_patterns=[]
        )

        # Test adding a file with a compound extension
        collector.add_file("requirements.trlc.md", throw_on_mismatch=True)
        self.assertEqual(collector.files, ["requirements.trlc.md"])

        # Test adding a file whose last suffix alone is not a valid extension
        with self.assertRaises(PathError) as context:
            collector.add_file("notes.md", throw_on_mismatch=True)
        self.assertEqual(
            str(context.exception),
            "File notes.md does not have a valid extension. "
            "Expected one of .rsl, .trlc, .trlc.md."
        )

    def test_add_files_extension_matching_is_case_insensitive(self):
        collector = FileCollector(
            extensions=[".RSL", ".TRLC"], directory_exclude_patterns=[]
        )

        collector.add_file("test.rsl", throw_on_mismatch=True)
        collector.add_file("test.trlc", throw_on_mismatch=True)
        self.assertEqual(collector.files, ["test.rsl", "test.trlc"])

    def test_add_files_with_no_extensions_accepts_any_file(self):
        collector = FileCollector(extensions=[], directory_exclude_patterns=[])

        collector.add_file("test.anything", throw_on_mismatch=True)
        self.assertEqual(collector.files, ["test.anything"])
