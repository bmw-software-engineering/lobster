from argparse import Namespace
from unittest import TestCase
from lobster.tool_base import ToolBase


class CherryPineappleTool(ToolBase):
    def _run_impl(self, options: Namespace) -> int:
        return 0


class ToolBaseTest(TestCase):
    def setUp(self):
        self.tool = CherryPineappleTool(name="Knorrstraße", description="A test tool", official=True)

    def test_name(self):
        self.assertEqual(self.tool.name, "lobster-Knorrstraße")
