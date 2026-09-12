import unittest
from unittest.mock import patch

from lobster.common.errors import LOBSTER_Error, Message_Handler
from lobster.common.location import Void_Reference
from lobster.common.policy_builder import build_tracing_policy
from lobster.common.raw_policy import (
    RawLevel,
    RawPolicy,
    RawRequiresCandidate,
    RawSource,
    RawTraceTo,
)

LOC = Void_Reference()


def make_level(name, kind="requirements", source=None, trace_to=None, requires=None):
    return RawLevel(
        name=name,
        name_loc=LOC,
        kind=kind,
        source=source or [],
        trace_to=trace_to or [],
        requires=requires or [],
    )


class PolicyBuilderTests(unittest.TestCase):
    def setUp(self):
        self.mh = Message_Handler()

    def test_duplicate_level_name_raises_error(self):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Duplicate_Level_Names
        raw_policy = RawPolicy(levels=[
            make_level("Requirements"),
            make_level("Requirements"),
        ])

        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(self.mh, raw_policy)
        self.assertEqual(exc_info.exception.message, "duplicate declaration")

    @patch("os.path.isfile", return_value=False)
    def test_missing_source_file_raises_error(self, _mock_isfile):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Missing_Source_File
        raw_policy = RawPolicy(levels=[
            make_level("Requirements",
                       source=[RawSource(file="missing.lobster", loc=LOC)]),
        ])

        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(self.mh, raw_policy)
        self.assertEqual(exc_info.exception.message,
                          "cannot find file missing.lobster")

    def test_self_trace_raises_error(self):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Self_Trace
        raw_policy = RawPolicy(levels=[
            make_level("Requirements",
                       trace_to=[RawTraceTo(target="Requirements", loc=LOC)]),
        ])

        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(self.mh, raw_policy)
        self.assertEqual(exc_info.exception.message, "cannot trace to yourself")

    def test_unknown_trace_to_target_raises_error(self):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Unknown_Trace_To_Target
        raw_policy = RawPolicy(levels=[
            make_level("Code",
                       trace_to=[RawTraceTo(target="Ghost", loc=LOC)]),
        ])

        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(self.mh, raw_policy)
        self.assertEqual(exc_info.exception.message, "unknown item Ghost")

    def test_unknown_requires_level_raises_error(self):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Unknown_Requires_Level
        raw_policy = RawPolicy(levels=[
            make_level("Requirements",
                       requires=[[RawRequiresCandidate(name="Ghost", loc=LOC)]]),
        ])

        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(self.mh, raw_policy)
        self.assertEqual(exc_info.exception.message, "unknown level Ghost")

    def test_requires_level_without_trace_to_raises_error(self):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Untraced_Requires
        raw_policy = RawPolicy(levels=[
            make_level("Code"),
            make_level("Requirements",
                       requires=[[RawRequiresCandidate(name="Code", loc=LOC)]]),
        ])

        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(self.mh, raw_policy)
        self.assertEqual(exc_info.exception.message,
                          "Code cannot trace to Requirements items")

    def test_breakdown_requirements_auto_derived_when_absent(self):
        # lobster-trace: core_report_req.Policy_Builder_Derives_Breakdown_Requirements
        raw_policy = RawPolicy(levels=[
            make_level("Requirements"),
            make_level("Code",
                       trace_to=[RawTraceTo(target="Requirements", loc=LOC)]),
        ])

        levels = build_tracing_policy(self.mh, raw_policy)

        self.assertEqual(levels["Requirements"].breakdown_requirements, [["Code"]])

    def test_breakdown_requirements_from_explicit_requires_directive(self):
        # lobster-trace: core_report_req.Policy_Builder_Derives_Breakdown_Requirements
        raw_policy = RawPolicy(levels=[
            make_level("Component Tests"),
            make_level("Unit Tests"),
            make_level(
                "Requirements",
                requires=[[
                    RawRequiresCandidate(name="Component Tests", loc=LOC),
                    RawRequiresCandidate(name="Unit Tests", loc=LOC),
                ]],
            ),
        ])
        for name in ("Component Tests", "Unit Tests"):
            for raw_level in raw_policy.levels:
                if raw_level.name == name:
                    raw_level.trace_to.append(
                        RawTraceTo(target="Requirements", loc=LOC))

        levels = build_tracing_policy(self.mh, raw_policy)

        self.assertEqual(levels["Requirements"].breakdown_requirements,
                          [["Component Tests", "Unit Tests"]])

    def test_derives_tracing_direction_flags(self):
        # lobster-trace: core_report_req.Policy_Builder_Derives_Tracing_Direction_Flags
        raw_policy = RawPolicy(levels=[
            make_level("Requirements"),
            make_level("Code",
                       trace_to=[RawTraceTo(target="Requirements", loc=LOC)]),
        ])

        levels = build_tracing_policy(self.mh, raw_policy)

        self.assertTrue(levels["Code"].needs_tracing_up)
        self.assertFalse(levels["Code"].needs_tracing_down)
        self.assertTrue(levels["Requirements"].needs_tracing_down)
        self.assertFalse(levels["Requirements"].needs_tracing_up)

    def test_level_order_independent(self):
        # lobster-trace: core_report_req.Policy_Builder_Level_Order_Independent
        raw_policy = RawPolicy(levels=[
            make_level("Code",
                       trace_to=[RawTraceTo(target="Requirements", loc=LOC)]),
            make_level("Requirements",
                       requires=[[RawRequiresCandidate(name="Code", loc=LOC)]]),
        ])

        levels = build_tracing_policy(self.mh, raw_policy)

        self.assertTrue(levels["Code"].needs_tracing_up)
        self.assertTrue(levels["Requirements"].needs_tracing_down)
        self.assertEqual(levels["Requirements"].breakdown_requirements, [["Code"]])


if __name__ == "__main__":
    unittest.main()
