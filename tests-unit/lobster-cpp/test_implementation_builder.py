from os import getcwd
from os.path import abspath, join
import re
from unittest import TestCase
from lobster.location import File_Reference
from lobster.tools.cpp.implementation_builder import ImplementationBuilder


class ImplementationBuilderTest(TestCase):
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
        impl_builder = ImplementationBuilder()
        path = join(self._get_os_independent_abspath_start(),
                    "path", "to", "the", "baking soda.NaHCO3")
        result = impl_builder._get_location(path, 420)
        self.assertEqual(result.filename, path)
        self.assertEqual(result.line, 420)
        self.assertIsNone(result.column)

    def test_get_location_from_rel_path(self):
        impl_builder = ImplementationBuilder()
        result = impl_builder._get_location(join(".", "water.H2O"), 1)
        self.assertEqual(result.filename, abspath("water.H2O"))
        self.assertEqual(result.line, 1)
        self.assertIsNone(result.column)

    def test_get_tag(self):
        impl_builder = ImplementationBuilder()
        for duplicate_file_counter, parent_folder in enumerate(
            ("cake", "pie"),
            start=1,
        ):
            FILE = "ingredients.txt"
            path = join(parent_folder, FILE)
            function_names = ["Sodium Chloride (NaCl)", "Glucose (C6H12O6)"]
            for line_nr, function_name in enumerate(function_names, start=1):
                with self.subTest(path=path, function_name=function_name):
                    tracing_tag = impl_builder._get_tag(path, function_name, line_nr)
                    self.assertEqual(tracing_tag.namespace, "cpp")
                    self.assertEqual(
                        tracing_tag.tag,
                        f"{FILE}:{duplicate_file_counter}:{function_name}:{line_nr}",
                    )
                    self.assertIsNone(tracing_tag.version)

    def test_from_match(self):
        impl_builder = ImplementationBuilder()

        for num_extra_groups in (0, 1, 10):
            num_groups = impl_builder.MIN_NUM_GROUPS + num_extra_groups
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
                impl = impl_builder.from_match(match)

                self.assertEqual(impl.tag.namespace, "cpp")
                self.assertEqual(impl.tag.tag, "example.cpp:1:myFunction:42")
                self.assertIsInstance(impl.location, File_Reference)
                self.assertEqual(impl.location.filename, abspath("example.cpp"))
                self.assertEqual(impl.location.line, 42)
                self.assertIsNone(impl.location.column)
                self.assertEqual(impl.language, "C/C++")
                self.assertEqual(impl.kind, "call")
                self.assertEqual(impl.name, "myFunction")

    def test_from_match_invalid_line_number(self):
        impl_builder = ImplementationBuilder()

        match = re.match(
            r"(.*)-(.*)-(.*)-(.*)",
            "stuff.cpp-NOT_INTEGER-abc-def"
        )
        if not match:
            self.fail("Invalid test setup: regex match failed!")
        if len(match.groups()) != impl_builder.MIN_NUM_GROUPS:
            self.fail(f"Invalid test setup: expected {impl_builder.MIN_NUM_GROUPS} "
                      f"groups, got {len(match.groups())}!")
        with self.assertRaises(ValueError):
            impl_builder.from_match(match)

    def test_from_match_if_new(self):
        impl_builder = ImplementationBuilder()
        db = {}
        match = re.match(
            r"(.*):(.*):(.*):(.*)",
            "example.cpp:43:callback:yourFunction"
        )
        if not match:
            self.fail("Invalid test setup: regex match failed!")
        impl = impl_builder.from_match_if_new(db, match)
        self.assertEqual(len(db), 1)
        self.assertIn(impl.tag.key(), db)
        self.assertIs(db[impl.tag.key()], impl)

        # Test that it returns the existing implementation if it already exists
        existing_impl = impl_builder.from_match_if_new(db, match)
        self.assertIs(existing_impl, impl)
