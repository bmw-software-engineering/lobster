import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from lobster.tools.trlc.errors import TrlcFailure
from lobster.tools.trlc.lobster_trlc_config import LobsterTrlcConfig
from lobster.tools.trlc.trlc_tool import LOBSTER_Trlc


_RSL_CONTENT = "package dup_test\ntype T {\n  field String\n}\n"
_TRLC_CONTENT = 'package dup_test\nT A {\n  field = "VALUE"\n}\n'


class RunLobsterTrlcTest(unittest.TestCase):
    def test_config_option_mandatory_missing(self):
        # lobster-trace: trlc_req.Config_Argparse_Requires_Config_Option
        self.assertEqual(LOBSTER_Trlc().run([]), 2)

    def test_no_inputs_produces_zero_items(self):
        # lobster-trace: trlc_req.Run_Lobster_Trlc_Empty_Symbol_Table_Writes_Zero_Items
        with TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "out.lobster"
            config = LobsterTrlcConfig.from_dict({})
            LOBSTER_Trlc().run_lobster_trlc(
                config=config,
                dir_or_files=[tmp_dir],
                out_file=str(out_file),
            )
            self.assertIn('"data": []', out_file.read_text())

    def test_duplicate_definition_raises_trlc_failure(self):
        # lobster-trace: trlc_req.Run_Lobster_Trlc_Duplicate_Definition_Raises
        with TemporaryDirectory() as tmp_dir:
            (Path(tmp_dir) / "shared.rsl").write_text(_RSL_CONTENT)
            (Path(tmp_dir) / "one.trlc").write_text(
                _TRLC_CONTENT.replace("VALUE", "one"))
            (Path(tmp_dir) / "two.trlc").write_text(
                _TRLC_CONTENT.replace("VALUE", "two"))

            config = LobsterTrlcConfig.from_dict({})
            with self.assertRaises(TrlcFailure):
                LOBSTER_Trlc().run_lobster_trlc(
                    config=config,
                    dir_or_files=[tmp_dir],
                    out_file=str(Path(tmp_dir) / "out.lobster"),
                )


if __name__ == "__main__":
    unittest.main()
