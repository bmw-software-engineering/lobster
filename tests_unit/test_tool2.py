from unittest import TestCase
from lobster.tool2 import select_non_comment_parts


class LobsterToolTest(TestCase):
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
