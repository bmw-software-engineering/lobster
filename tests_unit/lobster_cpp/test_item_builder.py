from os import getcwd
from os.path import abspath, join
import re
from unittest import TestCase
from lobster.common.items import Implementation, Item, KindTypes
from lobster.common.location import File_Reference
from lobster.tools.cpp.item_builder import ItemBuilder


class ItemBuilderTest(TestCase):
    @staticmethod
    def _get_os_independent_abspath_start():
        """Returns an arbitrary path which is guaranteed to be absolute.
           This way we can construct absolute paths in a platform-independent way.
           Note that otherwise an absolute path on Linux would start with a slash ("/"),
           while on Windows it would start with a drive letter (e.g., "C:\").

           The simplest solution is to use the current working directory,
           which always exists on all platforms and is always absolute.
        """
        return getcwd()

    def test_get_location_from_abs_path(self):
        item_builder = ItemBuilder()
        path = join(self._get_os_independent_abspath_start(),
                    "path", "to", "the", "baking soda.NaHCO3")
        result = item_builder._get_location(path, 420)
        self.assertEqual(result.filename, path)
        self.assertEqual(result.line, 420)
        self.assertIsNone(result.column)

    def test_get_location_from_rel_path(self):
        item_builder = ItemBuilder()
        result = item_builder._get_location(join(".", "water.H2O"), 1)
        self.assertEqual(result.filename, abspath("water.H2O"))
        self.assertEqual(result.line, 1)
        self.assertIsNone(result.column)

    def test_get_tag(self):
        item_builder = ItemBuilder()
        for duplicate_file_counter, parent_folder in enumerate(
            ("cake", "pie"),
            start=1,
        ):
            FILE = "ingredients.txt"
            path = join(parent_folder, FILE)
            function_names = ["Sodium Chloride (NaCl)", "Glucose (C6H12O6)"]
            for line_nr, function_name in enumerate(function_names, start=1):
                with self.subTest(path=path, function_name=function_name):
                    tracing_tag = item_builder._get_tag(path, function_name, line_nr)
                    self.assertEqual(tracing_tag.namespace, "cpp")
                    self.assertEqual(
                        tracing_tag.tag,
                        f"{FILE}:{duplicate_file_counter}:{function_name}:{line_nr}",
                    )
                    self.assertIsNone(tracing_tag.version)

    def test_from_match_no_kind(self):
        item_builder = ItemBuilder()

        for num_extra_groups in (0, 1, 10):
            num_groups = item_builder.MIN_NUM_GROUPS + num_extra_groups
            with self.subTest(num_groups=num_groups):
                values = "example.cpp:42:call:myFunction"
                values += "".join(
                    f":additional_{i}" for i in range(num_extra_groups)
                )
                match = re.match(
                    r":".join(r"(.*)" for _ in range(num_groups)),
                    values
                )
                if not match:
                    self.fail("Invalid test setup: regex match failed!")
                if len(match.groups()) != num_groups:
                    self.fail(f"Invalid test setup: expected {num_groups} groups, "
                              f"got {len(match.groups())}!")
                item = item_builder.from_match(match)

                self.assertEqual(item.tag.namespace, "cpp")
                self.assertEqual(item.tag.tag, "example.cpp:1:myFunction:42")
                self.assertIsInstance(item.location, File_Reference)
                self.assertEqual(item.location.filename, abspath("example.cpp"))
                self.assertEqual(item.location.line, 42)
                self.assertIsNone(item.location.column)
                self.assertTrue(isinstance(item, Item))

    def test_from_match_kind_itm(self):
        item_builder = ItemBuilder(kind=KindTypes.ITM.value)

        for num_extra_groups in (0, 1, 10):
            num_groups = item_builder.MIN_NUM_GROUPS + num_extra_groups
            with self.subTest(num_groups=num_groups):
                values = "example.cpp:42:call:myFunction"
                values += "".join(
                    f":additional_{i}" for i in range(num_extra_groups)
                )
                match = re.match(
                    r":".join(r"(.*)" for _ in range(num_groups)),
                    values
                )
                if not match:
                    self.fail("Invalid test setup: regex match failed!")
                if len(match.groups()) != num_groups:
                    self.fail(f"Invalid test setup: expected {num_groups} groups, "
                              f"got {len(match.groups())}!")
                item = item_builder.from_match(match)

                self.assertEqual(item.tag.namespace, "cpp")
                self.assertEqual(item.tag.tag, "example.cpp:1:myFunction:42")
                self.assertIsInstance(item.location, File_Reference)
                self.assertEqual(item.location.filename, abspath("example.cpp"))
                self.assertEqual(item.location.line, 42)
                self.assertIsNone(item.location.column)
                self.assertTrue(isinstance(item, Item))

    def test_from_match_kind_imp(self):
        item_builder = ItemBuilder(kind=KindTypes.IMP.value)

        for num_extra_groups in (0, 1, 10):
            num_groups = item_builder.MIN_NUM_GROUPS + num_extra_groups
            with self.subTest(num_groups=num_groups):
                values = "example.cpp:42:call:myFunction"
                values += "".join(
                    f":additional_{i}" for i in range(num_extra_groups)
                )
                match = re.match(
                    r":".join(r"(.*)" for _ in range(num_groups)),
                    values
                )
                if not match:
                    self.fail("Invalid test setup: regex match failed!")
                if len(match.groups()) != num_groups:
                    self.fail(f"Invalid test setup: expected {num_groups} groups, "
                              f"got {len(match.groups())}!")
                item = item_builder.from_match(match)

                self.assertEqual(item.tag.namespace, "cpp")
                self.assertEqual(item.tag.tag, "example.cpp:1:myFunction:42")
                self.assertIsInstance(item.location, File_Reference)
                self.assertEqual(item.location.filename, abspath("example.cpp"))
                self.assertEqual(item.location.line, 42)
                self.assertIsNone(item.location.column)
                self.assertTrue(isinstance(item, Implementation))
                self.assertEqual(item.language, "C/C++")
                self.assertEqual(item.kind, "call")
                self.assertEqual(item.name, "myFunction")

    def test_from_match_invalid_line_number(self):
        item_builder = ItemBuilder()

        match = re.match(
            r"(.*)-(.*)-(.*)-(.*)",
            "stuff.cpp-NOT_INTEGER-abc-def"
        )
        if not match:
            self.fail("Invalid test setup: regex match failed!")
        if len(match.groups()) != item_builder.MIN_NUM_GROUPS:
            self.fail(f"Invalid test setup: expected {item_builder.MIN_NUM_GROUPS} "
                      f"groups, got {len(match.groups())}!")
        with self.assertRaises(ValueError):
            item_builder.from_match(match)

    def test_from_match_if_new(self):
        item_builder = ItemBuilder()
        db = {}
        match = re.match(
            r"(.*):(.*):(.*):(.*)",
            "example.cpp:43:callback:yourFunction"
        )
        if not match:
            self.fail("Invalid test setup: regex match failed!")
        item = item_builder.from_match_if_new(db, match)
        self.assertEqual(len(db), 1)
        self.assertIn(item.tag.key(), db)
        self.assertIs(db[item.tag.key()], item)

        # Test that it returns the existing implementation if it already exists
        existing_item = item_builder.from_match_if_new(db, match)
        self.assertIs(existing_item, item)
