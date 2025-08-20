from os import path
from unittest import TestCase
from lobster.common.file_collector import FileCollector
from lobster.common.errors import PathError


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
