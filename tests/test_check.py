"""Rules the checker must enforce, and the four gaps it must find unaided.

Two kinds of test here. The rule tests use the smallest fixture that isolates
one rule, so a failure names the rule. The acceptance tests at the bottom assert
that the four gaps in docs/findings.md fall out of the general rules, which is
what stops the document and the code drifting apart: weaken a rule and they go
red.

No test tells the checker what to find. Every fixture is a set of partner
declarations, and the expected finding is computed from them.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from check import Severity, blocking, candidate_pairs, run  # noqa: E402
from model import (Declaration, Direction, Kind, Partner,  # noqa: E402
                   all_declarations, inferred, stated)


def decl(partner, direction, item, **kw):
    return Declaration(partner, direction, item, **kw)


def rules(findings):
    return {f.rule for f in findings}


def by_rule(findings, rule):
    return [f for f in findings if f.rule == rule]


class TestPairing(unittest.TestCase):
    def test_a_partner_is_never_paired_with_itself(self):
        p = Partner("Solis", declarations=[
            decl("Solis", Direction.PRODUCES, "operating envelopes"),
            decl("Solis", Direction.CONSUMES, "operating envelopes"),
        ])
        self.assertEqual([], candidate_pairs(all_declarations([p])))

    def test_close_wording_across_partners_is_a_candidate_pair(self):
        a = Partner("Solis", declarations=[decl("Solis", Direction.PRODUCES, "capacity choices")])
        b = Partner("Tharsis", declarations=[decl("Tharsis", Direction.CONSUMES, "available capacity")])
        pairs = candidate_pairs(all_declarations([a, b]))
        self.assertEqual(1, len(pairs))

    def test_unrelated_wording_is_not_a_candidate_pair(self):
        a = Partner("Solis", declarations=[decl("Solis", Direction.PRODUCES, "capacity choices")])
        b = Partner("Tharsis", declarations=[decl("Tharsis", Direction.CONSUMES, "population schedules")])
        self.assertEqual([], candidate_pairs(all_declarations([a, b])))


class TestContractRules(unittest.TestCase):
    def test_unmatched_consumption_is_a_blocking_finding(self):
        a = Partner("Tharsis", declarations=[decl("Tharsis", Direction.CONSUMES, "population schedules")])
        found = by_rule(run([a]), "UNMATCHED_CONSUMPTION")
        self.assertEqual(1, len(found))
        self.assertIs(Severity.BLOCKING, found[0].severity)

    def test_unrouted_production_is_a_blocking_finding(self):
        a = Partner("Meridian", declarations=[decl("Meridian", Direction.PRODUCES, "acceptable service levels")])
        found = by_rule(run([a]), "UNROUTED_PRODUCTION")
        self.assertEqual(1, len(found))
        self.assertIs(Severity.BLOCKING, found[0].severity)

    def test_a_candidate_pair_with_no_declared_link_is_blocking(self):
        a = Partner("Solis", declarations=[decl("Solis", Direction.PRODUCES, "capacity choices")])
        b = Partner("Tharsis", declarations=[decl("Tharsis", Direction.CONSUMES, "available capacity")])
        found = by_rule(run([a, b]), "UNLINKED_PAIR")
        self.assertEqual(1, len(found))

    def test_a_declared_link_silences_the_unlinked_rule(self):
        a = Partner("Solis", declarations=[
            decl("Solis", Direction.PRODUCES, "capacity choices", link="C-1")])
        b = Partner("Tharsis", declarations=[
            decl("Tharsis", Direction.CONSUMES, "available capacity", link="C-1")])
        self.assertEqual([], by_rule(run([a, b]), "UNLINKED_PAIR"))

    def test_kind_mismatch_on_a_pair_is_a_blocking_finding(self):
        a = Partner("Solis", declarations=[
            decl("Solis", Direction.PRODUCES, "capacity choices", kind=Kind.DECISION, link="C-1")])
        b = Partner("Tharsis", declarations=[
            decl("Tharsis", Direction.CONSUMES, "available capacity", kind=Kind.STATE, link="C-1")])
        self.assertEqual(1, len(by_rule(run([a, b]), "KIND_MISMATCH")))

    def test_an_unknown_kind_does_not_raise_a_kind_mismatch(self):
        a = Partner("Solis", declarations=[
            decl("Solis", Direction.PRODUCES, "capacity choices", kind=Kind.DECISION, link="C-1")])
        b = Partner("Tharsis", declarations=[
            decl("Tharsis", Direction.CONSUMES, "available capacity", link="C-1")])
        self.assertEqual([], by_rule(run([a, b]), "KIND_MISMATCH"))

    def test_resolution_mismatch_names_the_axis_it_fired_on(self):
        a = Partner("Solis", declarations=[
            decl("Solis", Direction.PRODUCES, "capacity choices",
                 temporal=stated("multi-year"), link="C-1")])
        b = Partner("Tharsis", declarations=[
            decl("Tharsis", Direction.CONSUMES, "available capacity",
                 temporal=stated("hourly"), link="C-1")])
        found = by_rule(run([a, b]), "RESOLUTION_MISMATCH")
        self.assertEqual(1, len(found))
        self.assertIn("temporal", found[0].message)

    def test_an_unstated_axis_cannot_raise_a_resolution_mismatch(self):
        a = Partner("Solis", declarations=[
            decl("Solis", Direction.PRODUCES, "capacity choices",
                 temporal=stated("multi-year"), link="C-1")])
        b = Partner("Tharsis", declarations=[
            decl("Tharsis", Direction.CONSUMES, "available capacity", link="C-1")])
        self.assertEqual([], by_rule(run([a, b]), "RESOLUTION_MISMATCH"))

    def test_an_unstated_clause_is_reported_and_names_its_family(self):
        a = Partner("Solis", declarations=[
            decl("Solis", Direction.PRODUCES, "capacity choices", link="C-1")])
        b = Partner("Tharsis", declarations=[
            decl("Tharsis", Direction.CONSUMES, "available capacity", link="C-1")])
        found = by_rule(run([a, b]), "UNDECLARED_CLAUSE")
        self.assertEqual(len(Declaration.CLAUSES), len(found))
        self.assertTrue(all(f.severity is Severity.REPORTED for f in found))
        self.assertTrue(any("what it is measured in" in f.message for f in found))

    def test_an_inferred_clause_is_reported_but_not_blocking(self):
        a = Partner("Solis", declarations=[
            decl("Solis", Direction.PRODUCES, "capacity choices", unit=inferred("MW"))])
        found = by_rule(run([a]), "INFERRED_CLAUSE")
        self.assertEqual(1, len(found))
        self.assertIs(Severity.ADVISORY, found[0].severity)

    def test_a_stated_clause_raises_nothing(self):
        a = Partner("Solis", declarations=[
            decl("Solis", Direction.PRODUCES, "capacity choices", unit=stated("MW"))])
        self.assertEqual([], by_rule(run([a]), "INFERRED_CLAUSE"))

    def test_findings_are_deterministically_ordered(self):
        a = Partner("Solis", declarations=[
            decl("Solis", Direction.PRODUCES, "capacity choices", kind=Kind.DECISION,
                 temporal=stated("multi-year"), unit=inferred("MW"))])
        b = Partner("Tharsis", declarations=[
            decl("Tharsis", Direction.CONSUMES, "available capacity", kind=Kind.STATE,
                 temporal=stated("hourly")),
            decl("Tharsis", Direction.CONSUMES, "population schedules")])
        first = [str(f) for f in run([a, b])]
        self.assertEqual(first, [str(f) for f in run([a, b])])
        self.assertEqual(first, [str(f) for f in run([b, a])])


class TestTheFourGapsFallOut(unittest.TestCase):
    """docs/findings.md names four gaps. They must be computed, not asserted.

    The fixture below is the consortium as the brief describes it, and nothing
    more. If a rule is weakened so that a gap stops being found, one of these
    goes red and the document is no longer supported by the artifact.
    """

    def setUp(self):
        self.partners = [
            Partner("Solis", "commercial infrastructure modeller", [
                decl("Solis", Direction.CONSUMES, "technology assumptions"),
                decl("Solis", Direction.CONSUMES, "resource limits"),
                decl("Solis", Direction.CONSUMES, "demand envelopes",
                     kind=Kind.BOUND, temporal=stated("multi-year")),
                decl("Solis", Direction.PRODUCES, "capacity choices",
                     kind=Kind.DECISION, temporal=stated("multi-year")),
                decl("Solis", Direction.PRODUCES, "operating envelopes",
                     kind=Kind.BOUND, temporal=stated("multi-year")),
                decl("Solis", Direction.PRODUCES, "resource allocations"),
                decl("Solis", Direction.PRODUCES, "system trade-offs"),
            ]),
            Partner("Tharsis", "university simulation team", [
                decl("Tharsis", Direction.CONSUMES, "available capacity",
                     kind=Kind.STATE, temporal=stated("hourly")),
                decl("Tharsis", Direction.CONSUMES, "operating constraints",
                     kind=Kind.BOUND, temporal=stated("hourly")),
                decl("Tharsis", Direction.CONSUMES, "population schedules",
                     kind=Kind.SCHEDULE),
                decl("Tharsis", Direction.PRODUCES, "time-series demand",
                     kind=Kind.SERIES, temporal=stated("hourly")),
                decl("Tharsis", Direction.PRODUCES, "service shortfalls",
                     kind=Kind.SERIES, temporal=stated("hourly")),
                decl("Tharsis", Direction.PRODUCES, "operational responses"),
            ]),
            Partner("Meridian", "public mission-risk institute", [
                decl("Meridian", Direction.PRODUCES, "stress scenarios"),
                decl("Meridian", Direction.PRODUCES, "reliability metrics"),
                decl("Meridian", Direction.PRODUCES, "evidence requirements"),
                decl("Meridian", Direction.PRODUCES, "acceptable service levels",
                     kind=Kind.THRESHOLD),
            ]),
            Partner("Helix", "schema translation", []),
        ]
        self.findings = run(self.partners)

    def _messages(self, rule):
        return " ".join(f.message for f in by_rule(self.findings, rule))

    def test_gap_1_the_aggregation_operator_is_found(self):
        """Multi-year planning against hourly simulation, no conversion owned."""
        self.assertIn("multi-year", self._messages("RESOLUTION_MISMATCH"))
        self.assertIn("hourly", self._messages("RESOLUTION_MISMATCH"))

    def test_gap_2_the_derate_function_is_found(self):
        """A capacity decision is not the same object as available capacity."""
        msg = self._messages("KIND_MISMATCH")
        self.assertIn("decision", msg)
        self.assertIn("state", msg)

    def test_gap_3_the_service_level_thresholds_are_unrouted(self):
        self.assertIn("acceptable service levels", self._messages("UNROUTED_PRODUCTION"))

    def test_gap_4_population_schedules_have_no_producer(self):
        self.assertIn("population schedules", self._messages("UNMATCHED_CONSUMPTION"))

    def test_a_partner_declaring_nothing_raises_nothing_which_is_the_point(self):
        """Helix declares no interface, so no rule can say anything about it.

        This is not the checker being lenient. It is the checker being unable to
        see a partner that has not described its boundary, which is a worse
        position than a partner with a wrong description.
        """
        self.assertEqual([], [f for f in self.findings if "Helix" in f.subject])

    def test_the_consortium_as_described_does_not_pass(self):
        self.assertGreater(len(blocking(self.findings)), 0)


if __name__ == "__main__":
    unittest.main()


class TestSchedule(unittest.TestCase):
    """The seating plan carries a rule, so the rule is asserted rather than stated."""

    def setUp(self):
        import schedule
        self.s = schedule

    def test_helix_attends_no_authority_session(self):
        """A translator converts between vocabularies. It cannot rule on meaning.

        Stating that in prose and then inviting Helix to the session that settles
        ownership would be the same class of drift this repository is about, so
        the seating plan is checked instead.
        """
        offending = [s.name for s in self.s.SESSIONS
                     if s.authority and "Helix" in s.attendees]
        self.assertEqual([], offending)

    def test_every_session_falls_inside_six_weeks(self):
        self.assertTrue(all(1 <= s.week <= 6 for s in self.s.SESSIONS))

    def test_week_five_is_buffer_and_carries_no_new_commitment(self):
        """Slack that gets scheduled into is not slack."""
        new_work = [s.name for s in self.s.SESSIONS
                    if s.week == 5 and "review" not in s.name.lower()]
        self.assertEqual([], new_work)

    def test_the_skeleton_runs_before_the_halfway_point(self):
        """Integration failures have to surface with time left to fix them."""
        skeleton = [m for m in self.s.MILESTONES if m.kind == "skeleton"]
        self.assertEqual(1, len(skeleton))
        self.assertLessEqual(skeleton[0].week, 2)
