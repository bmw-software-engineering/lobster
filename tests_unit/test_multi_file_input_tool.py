import os
from tempfile import TemporaryDirectory
from unittest import TestCase
from lobster.multi_file_input_tool import (
    create_worklist,
    combine_all_inputs,
    select_non_comment_parts,
)
from lobster.multi_file_input_config import Config
from tests_unit.temp_content_file import TempContentFile


class MultiFileInputToolTest(TestCase):
    def test_select_non_comment_parts(self):
        input_text = [
            "This is a line.           ",
            "This is another line. # with a comment",
            "  # This is a full comment line",
            "Yet another line.",
            "",
            "  ",
            "#",
            "##",
            "Line with # two # comment separators"
        ]
        expected_output = [
            "This is a line.",
            "This is another line.",
            "Yet another line.",
            "Line with"
        ]
        result = select_non_comment_parts(input_text)
        self.assertEqual(result, expected_output)

    def test_combine_all_inputs_single_source1(self):
        config = Config(
            inputs=None,
            inputs_from_file=None,
            extensions=None,
            exclude_patterns=None,
            schema=None,
        )
        dir_or_files = ["mouse", "elephant"]
        result = combine_all_inputs(config, dir_or_files)
        self.assertListEqual(result, dir_or_files)

    def test_combine_all_inputs_single_source2(self):
        file_content = ["penguin", "seagull", "kangaroo"]
        with TempContentFile("\n".join(file_content)) as tmp_file:
            config = Config(
                inputs=None,
                inputs_from_file=tmp_file,
                extensions=None,
                exclude_patterns=None,
                schema=None,
            )
            result = combine_all_inputs(config, None)
            self.assertEqual(result, file_content)

    def test_combine_all_inputs_single_source3(self):
        config = Config(
            inputs=["giraffe", "lion", "spider"],
            inputs_from_file=None,
            extensions=None,
            exclude_patterns=None,
            schema=None,
        )
        result = combine_all_inputs(config, None)
        self.assertEqual(result, config.inputs)

    def test_combine_all_inputs_three_sources(self):
        file_content = ["otter", "lemur", "alpaca"]
        dir_or_files = ["guinea pig", "sparrow"]
        with TempContentFile("\n".join(file_content)) as tmp_file:
            config = Config(
                inputs=["cat", "dog", "rabbit", "bare-nosed wombat"],
                inputs_from_file=tmp_file,
                extensions=None,
                exclude_patterns=None,
                schema=None,
            )
            result = combine_all_inputs(config, dir_or_files)
            self.assertEqual(result, config.inputs + file_content + dir_or_files)

    def test_create_worklist(self):
        with TemporaryDirectory() as tmp_dir:
            extension = ".animal"
            def as_path(file_base_name: str) -> str:
                return os.path.join(tmp_dir, f"{file_base_name}{extension}")

            config_inputs = [
                as_path("wolf"),
                as_path("bear"),
                as_path("salmon"),
                as_path("rhinoceros"),
            ]
            expected_file_content = [
                as_path("bison"),
                as_path("toucan"),
                as_path("meerkat"),
            ]
            file_content = expected_file_content.copy()
            file_content.insert(1, "# comment line")
            file_content[-1] += " # comment appended after path"
            dir_or_files = [
                as_path("unicorn"),
                as_path("dragon"),
            ]

            expected = config_inputs + expected_file_content + dir_or_files

            for dummy_file in expected:
                # the files must really exist, because the function under test
                # differentiates between files and directories; so create empty files
                with open(dummy_file, "w", encoding="UTF-8"):
                    pass

            with TempContentFile("\n".join(file_content)) as tmp_file:
                config = Config(
                    inputs=config_inputs,
                    inputs_from_file=tmp_file,
                    extensions=[extension],
                    exclude_patterns=None,
                    schema=None,
                )
                result = create_worklist(config, dir_or_files)
                # The implementation actually keeps the order, so we could compare lists
                # instead of sets. But that works only if no directories are traversed.
                # Furthermore, the function 'create_worklist' is not designed to return
                # the items in any specific order, so we should not test for it either.
                # Hence compare only sets:
                self.assertSetEqual(set(result), set(expected))
