# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

import unittest
from unittest.mock import patch

from lobster.common.errors import LOBSTER_Error
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
    def test_duplicate_level_name_raises_error(self):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Duplicate_Level_Names

        # GIVEN a policy with duplicate level names
        raw_policy = RawPolicy(levels=[
            make_level("notebook"),
            make_level("notebook"),
        ])

        # WHEN the function is called
        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(raw_policy)

        # THEN expect an exception
        self.assertEqual(exc_info.exception.message, "duplicate declaration")

    @patch("os.path.isfile", return_value=False)
    def test_missing_source_file_raises_error(self, _mock_isfile):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Missing_Source_File

        # GIVEN a policy with a source file that does not exist
        raw_policy = RawPolicy(levels=[
            make_level("Undetectable Data",
                       source=[RawSource(file="missing.lobster", loc=LOC)]),
        ])

        # WHEN the function is called
        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(raw_policy)

        # THEN it raises an exception
        self.assertEqual(exc_info.exception.message,
                          "cannot find file missing.lobster")

    def test_self_trace_raises_error(self):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Self_Trace

        # GIVEN a policy where a level traces to itself
        raw_policy = RawPolicy(levels=[
            make_level("I just need myself!",
                       trace_to=[RawTraceTo(target="I just need myself!", loc=LOC)]),
        ])

        # WHEN the function is called
        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(raw_policy)

        # THEN it raises an exception
        self.assertEqual(exc_info.exception.message, "cannot trace to yourself")

    def test_unknown_trace_to_target_raises_error(self):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Unknown_Trace_To_Target

        # GIVEN a policy that references an unknown trace target
        raw_policy = RawPolicy(levels=[
            make_level("Real",
                       trace_to=[RawTraceTo(target="Ghost", loc=LOC)]),
        ])

        # WHEN the function is called
        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(raw_policy)

        # THEN it raises an exception
        self.assertEqual(exc_info.exception.message, "unknown item Ghost")

    def test_unknown_requires_level_raises_error(self):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Unknown_Requires_Level

        # GIVEN a policy with a "requires" reference to an unknown level
        raw_policy = RawPolicy(levels=[
            make_level("Real",
                       requires=[[RawRequiresCandidate(name="Ghost", loc=LOC)]]),
        ])

        # WHEN the function is called
        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(raw_policy)

        # THEN it raises an exception
        self.assertEqual(exc_info.exception.message, "unknown level Ghost")

    def test_requires_level_without_trace_to_raises_error(self):
        # lobster-trace: core_report_req.Policy_Builder_Rejects_Untraced_Requires

        # GIVEN a policy where a level requires another level that on its own does not
        # trace to the first level
        raw_policy = RawPolicy(levels=[
            make_level("Apple"),
            make_level("Banana",
                       requires=[[RawRequiresCandidate(name="Apple", loc=LOC)]]),
        ])

        # WHEN the function is called
        with self.assertRaises(LOBSTER_Error) as exc_info:
            build_tracing_policy(raw_policy)

        # THEN it raises an exception
        self.assertEqual(exc_info.exception.message,
                          "Apple cannot trace to Banana items")

    def test_breakdown_requirements_auto_derived_when_absent(self):
        # lobster-trace: core_report_req.Policy_Builder_Level_Order_Independent
        # lobster-trace: core_report_req.Policy_Builder_Derives_Breakdown_Requirements
        # lobster-trace: core_report_req.Policy_Builder_Derives_Tracing_Direction_Flags

        # GIVEN a policy where a level traces to another level, declared in
        # both possible orders
        vacuum_cleaner_level = make_level("vacuum cleaner")
        dryer_level = make_level(
            "dryer", trace_to=[RawTraceTo(target=vacuum_cleaner_level.name, loc=LOC)])
        raw_levels = [vacuum_cleaner_level, dryer_level]

        for ordering in ("declared order", "reverse order"):
            with self.subTest(ordering):
                raw_policy = RawPolicy(levels=raw_levels)

                # WHEN the function is called
                levels = build_tracing_policy(raw_policy)

                # THEN the breakdown requirements are one OR-group
                self.assertEqual(
                    levels[vacuum_cleaner_level.name].breakdown_requirements,
                    [[dryer_level.name]]
                )

                # THEN the tracing direction flags are set correctly
                self.assertTrue(levels[dryer_level.name].needs_tracing_up)
                self.assertFalse(levels[dryer_level.name].needs_tracing_down)
                self.assertTrue(levels[vacuum_cleaner_level.name].needs_tracing_down)
                self.assertFalse(levels[vacuum_cleaner_level.name].needs_tracing_up)

            # reverse the list for the second subtest
            raw_levels.reverse()

    def test_breakdown_requirements_from_explicit_requires_directive(self):
        # lobster-trace: core_report_req.Policy_Builder_Derives_Breakdown_Requirements

        # GIVEN a policy where a level explicitly requires other levels
        jet_engine = RawRequiresCandidate(name="jet engine", loc=LOC)
        landing_gear = RawRequiresCandidate(name="landing gear", loc=LOC)
        jet_engine_level = make_level("jet engine")
        landing_gear_level = make_level("landing gear")
        airplane_level = make_level(
            "Airplane",
            requires=[[jet_engine, landing_gear]],
        )
        raw_policy = RawPolicy(levels=[
            jet_engine_level,
            landing_gear_level,
            airplane_level,
        ])
        jet_engine_level.trace_to.append(RawTraceTo(target=airplane_level.name, loc=LOC))
        landing_gear_level.trace_to.append(RawTraceTo(target=airplane_level.name, loc=LOC))

        # WHEN the function is called
        levels = build_tracing_policy(raw_policy)

        # THEN the "breakdown requirements" contains exactly one OR-group with the required levels
        self.assertEqual(len(levels[airplane_level.name].breakdown_requirements), 1)
        actual_or_group = levels[airplane_level.name].breakdown_requirements[0]
        self.assertCountEqual(actual_or_group, [jet_engine_level.name, landing_gear_level.name])


if __name__ == "__main__":
    unittest.main()
