from unittest import TestCase
from lobster.file_tag_generator import FileTagGenerator


class FileTagGeneratorTest(TestCase):
    def setUp(self):
        self.generator = FileTagGenerator()

    def test_unique_tags(self):
        basename = "file.txt"
        tag1 = self.generator.get_tag(f"/path/to/{basename}")
        tag2 = self.generator.get_tag(f"/another/path/to/{basename}")
        self.assertEqual(tag1, f"{basename}:1")
        self.assertEqual(tag2, f"{basename}:2")

    def test_same_file_same_tag(self):
        path = "/path/to/file.abc"
        tag1 = self.generator.get_tag(path)
        tag2 = self.generator.get_tag(path)
        self.assertEqual(tag1, tag2)

    def test_basename_only(self):
        file = "document.abc"
        tag1 = self.generator.get_tag(file)
        self.assertEqual(tag1, f"{file}:1")
