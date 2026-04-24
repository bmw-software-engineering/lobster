import unittest
import subprocess
from datetime import datetime, timezone
from lobster.tools.core.html_report.html_report import (
    get_commit_timestamp_utc,
    write_html,
)
from lobster.common.report import Report, Coverage
from lobster.common.level_definition import LevelDefinition
from lobster.common.items import Requirement, Tracing_Status, Tracing_Tag
from lobster.common.location import File_Reference


class LobsterHtmlReportTests(unittest.TestCase):
    def test_timestamp_found_in_main_repo(self):
        """Test when commit is found in main repo"""
        head_commit = "HEAD"
        result = subprocess.run(
            ['git', 'show', '-s', '--format=%ct', head_commit],
            capture_output=True, text=True, check=True
        )
        epoch_time = int(result.stdout.strip())
        expected_time = datetime.fromtimestamp(epoch_time, tz=timezone.utc)

        returned = get_commit_timestamp_utc(head_commit)
        self.assertIn(str(expected_time), returned)
        self.assertNotIn("from submodule", returned)

    def test_timestamp_unknown_commit(self):
        """Test when commit is not found in repo or submodules"""
        invalid_commit = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
        returned = get_commit_timestamp_utc(invalid_commit)
        self.assertEqual(returned, "Unknown")

    def test_html_contains_ver_val_fields(self):
        report = Report()
        level_name = "System Requirements"
        report.config = {
            level_name: LevelDefinition(name=level_name, kind="requirements"),
        }
        report.coverage = {
            level_name: Coverage(level=level_name, items=1, ok=1, coverage=100.0),
        }

        item = Requirement(
            tag=Tracing_Tag("req", "123", "1"),
            location=File_Reference("req.trlc", 1, 1),
            framework="codebeamer",
            kind="Requirement",
            name="Requirement with ver/val fields",
            status="Formal Review",
            asil="ASIL B",
            ver_ValSetup="SW unit/comp test",
            ver_ValRationalargumentation="Validation rationale text",
        )
        item.set_level(level_name)
        item.tracing_status = Tracing_Status.OK
        report.items = {item.tag.key(): item}

        html_content = write_html(
            report=report,
            dot=None,
            high_contrast=False,
            render_md=False,
        )

        self.assertIn("Ver_Val setup: SW unit/comp test", html_content)
        self.assertIn(
            "Ver_Val rational/argumentation: Validation rationale text",
            html_content,
        )


if __name__ == "__main__":
    unittest.main()
