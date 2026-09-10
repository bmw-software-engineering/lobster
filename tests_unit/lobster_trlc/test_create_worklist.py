import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from lobster.common.multi_file_input_config import Config
from lobster.common.multi_file_input_tool import combine_all_inputs, create_worklist


def _make_config(inputs=None, inputs_from_file=None):
    return Config(
        inputs=inputs or [],
        inputs_from_file=inputs_from_file,
        extensions=(".rsl", ".trlc", ".trlc.md"),
        exclude_patterns=[],
        schema=None,
    )


class CombineAllInputsTest(unittest.TestCase):
    def test_combines_inputs_and_dir_or_files(self):
        # lobster-trace: trlc_req.Combine_All_Inputs_Includes_Positional_Arguments
        config = _make_config(inputs=["a.trlc"])
        result = combine_all_inputs(config, ["b.trlc"])
        self.assertEqual(result, ["a.trlc", "b.trlc"])

    def test_reads_inputs_from_file(self):
        # lobster-trace: trlc_req.Combine_All_Inputs_Reads_Inputs_From_File
        with TemporaryDirectory() as tmp_dir:
            list_file = Path(tmp_dir) / "list.txt"
            list_file.write_text("\n# a comment\na.trlc\nb.rsl  # trailing comment\n")
            config = _make_config(inputs_from_file=str(list_file))
            result = combine_all_inputs(config, None)
            self.assertEqual(result, ["a.trlc", "b.rsl"])

    def test_combines_inputs_and_inputs_from_file(self):
        # lobster-trace: trlc_req.Combine_All_Inputs_Merges_Inputs_And_Inputs_From_File
        with TemporaryDirectory() as tmp_dir:
            list_file = Path(tmp_dir) / "list.txt"
            list_file.write_text("from_file.trlc\n")
            config = _make_config(
                inputs=["from_inputs.trlc"],
                inputs_from_file=str(list_file),
            )
            result = combine_all_inputs(config, None)
            self.assertEqual(result, ["from_inputs.trlc", "from_file.trlc"])


class CreateWorklistTest(unittest.TestCase):
    def test_directory_is_searched_recursively(self):
        # lobster-trace: trlc_req.Create_Worklist_Searches_Directories_Recursively
        with TemporaryDirectory() as tmp_dir:
            nested = Path(tmp_dir) / "nested"
            nested.mkdir()
            (Path(tmp_dir) / "a.rsl").write_text("package a\n")
            (nested / "b.trlc").write_text("")
            (nested / "c.txt").write_text("not trlc")

            config = _make_config(inputs=[tmp_dir])
            work_list = create_worklist(config, None)

            self.assertEqual(len(work_list), 2)
            self.assertTrue(all(f.endswith((".rsl", ".trlc")) for f in work_list))

    def test_invalid_path_raises(self):
        # lobster-trace: trlc_req.Create_Worklist_Rejects_Invalid_Path
        config = _make_config(inputs=["/no/such/path"])
        with self.assertRaises(ValueError):
            create_worklist(config, None)


if __name__ == "__main__":
    unittest.main()
