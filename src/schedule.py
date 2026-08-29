"""The six-week schedule, as data rather than as prose.

Kept here so the plan, the page and the deck all read one source. A schedule
that exists in three documents drifts, which is the failure this repository is
about, and it would be a poor look for it to happen here.

Two things the shape encodes deliberately.

The walking skeleton in week 2 runs end to end on crude inputs whose only job is
to make every format, encoding and calendar mismatch fail while there is time to
fix it. The consortium is at month 8 and has never run end to end, and an
exchange arriving late and in an unexpected format is what that produces.

Week 5 is buffer. Nothing is scheduled into it that cannot move out of it. A
plan with no slack is a plan that assumes nothing goes wrong, and the
demonstration is what second-year funding depends on.

The governing principle behind both: from week 2 there is always something that
runs. Every week after that improves the same demonstration rather than building
toward a first one, so each week's output is a superset of the week before. The
worst case in week 6 is showing week 5's version. There is no week in this plan
in which the answer to "what can you show us" is nothing, because that answer is
the one that ends the programme.
"""

from __future__ import annotations

from dataclasses import dataclass, field

PARTNERS = ["Solis", "Tharsis", "Meridian", "Helix"]

ALWAYS_DEMONSTRABLE = (
    "From week 2 the demonstration exists and runs. Each week improves it rather "
    "than building toward a first one, so the worst case is showing last week's "
    "version rather than showing nothing.")


@dataclass(frozen=True)
class Session:
    week: int
    name: str
    length: str
    attendees: tuple[str, ...]
    purpose: str
    authority: bool = False
    """True where the session settles what a variable means or who owns it.

    Helix attends every technical session and no authority session. A
    translation layer converts between vocabularies. It cannot decide what a
    variable means, and nobody in the consortium could give it that standing.
    """


@dataclass(frozen=True)
class Milestone:
    week: int
    name: str
    detail: str
    kind: str = "milestone"


@dataclass
class Track:
    name: str
    weeks: tuple[int, ...]
    detail: str
    critical: bool = False


SESSIONS = [
    Session(1, "Kickoff", "90 min", tuple(PARTNERS),
            "State the diagnosis. Agree the contract is the object, not the vocabulary. "
            "Settles the frame rather than any variable, so it is not an authority session."),
    Session(1, "Interface working session", "half day",
            ("Solis", "Tharsis", "Helix"),
            "Calendar and epoch, units, encoding. Contract v0 leaves this room."),
    Session(1, "Evidence elicitation", "90 min", ("Meridian",),
            "What makes a resilience claim credible, written down.",
            authority=True),
    Session(2, "Derate session", "90 min", ("Solis", "Meridian"),
            "Solis cannot declare how capacity degrades without Meridian's failure "
            "definitions. The expensive decision in the whole plan.",
            authority=True),
    Session(2, "Contract v1 sign-off", "half day",
            ("Solis", "Tharsis", "Helix"),
            "Every cell filled, or visibly empty. Helix re-points its existing "
            "adapter to the ruling, which is a diff rather than a rewrite, and that "
            "adapter carries the walking skeleton."),
    Session(2, "Walking skeleton review", "60 min", tuple(PARTNERS),
            "What broke when it ran end to end on crude inputs. This is the point "
            "of week 2."),
    Session(3, "Stress case selection", "60 min", ("Meridian",),
            "One material stress event, named, with its duration.", authority=True),
    Session(3, "Integration standup", "30 min weekly",
            ("Solis", "Tharsis", "Helix"),
            "Runs weekly through week 5. Blockers only."),
    Session(4, "Normal case review", "90 min", tuple(PARTNERS),
            "The normal operating case, end to end, contract enforced."),
    Session(5, "Stress case review", "90 min", tuple(PARTNERS),
            "The stress event, run iterated, with the correlation preserved."),
    Session(6, "Dress rehearsal", "half day", (),
            "The demonstration is rehearsed four days before the board sees it."),
]

MILESTONES = [
    Milestone(1, "Contract v0", "Calendar fixed, thresholds published, schedule owned."),
    Milestone(2, "End to end on junk data", "Every format and encoding mismatch fails here.",
              "skeleton"),
    Milestone(3, "Contract v1", "Complete, or with its empty cells visible.", "gate"),
    Milestone(4, "Normal case runs", "One configuration, traceable."),
    Milestone(5, "Traceability pass", "If week 4 held. Catch-up if it did not.", "buffer"),
    Milestone(6, "Board demonstration", "Normal case and one stress event.", "demo"),
]

TRACKS = [
    Track("Track A, Solis to Tharsis", (1, 2, 3), "The exchange that already failed.",
          critical=True),
    Track("Track B, Meridian", (1, 2, 3), "Runs alongside, because what Meridian "
          "requires changes what track A must carry."),
    Track("Run it", (3, 4, 5), "Normal case, stress case, traceability."),
    Track("Slack and rehearsal", (5, 6), "One week absorbed, then four days of polish."),
    Track("Helix conformance check", (2, 3, 4, 5, 6),
          "The re-pointed adapter runs on every exchange from week 2. The only role "
          "the brief supports, since it names no input and no output for Helix."),
]

REVIEW_POINTS = {
    1: "Calendar fixed and thresholds published, or week 2 carries an unowned assumption.",
    2: "It ran end to end, however badly. If it did not, that is the finding and the plan changes.",
    3: "Contract table complete or visibly incomplete. An empty cell is acceptable, an unnoticed one is not.",
    4: "The demonstration is better than last week's and still runs. That is the weekly test from here.",
    5: "Stress case has run. If not, week 5 absorbs it and week 6 still rehearses.",
}
