from argparse import Namespace
from unittest import TestCase
from lobster.meta_data_tool_base import MetaDataToolBase


class CherryPineappleTool(MetaDataToolBase):
    def _run_impl(self, options: Namespace) -> int:
        return 0


class MetaDataToolBaseTest(TestCase):
    def setUp(self):
        self.tool = CherryPineappleTool(
            name="Knorrstraße",
            description="A test tool",
            official=True,
        )

    def test_name(self):
        self.assertEqual(self.tool.name, "lobster-Knorrstraße")
