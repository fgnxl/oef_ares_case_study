"""The checker. Runs rules over the model and returns findings, it does not print.

Separated from build.py so the rules are testable without touching the
filesystem, and separated from render.py so a finding is a value rather than a
paragraph of HTML.

Every rule here is general. None of them names a partner, an item or a gap. Run
against a boundary where every object has an owner and every clause is stated,
all of them return nothing, which is the condition the recommendation aims at.
The gaps in docs/findings.md are the expected OUTPUT of this file and never an
input to it, because a checker told what to find demonstrates nothing. Four of
the five fall out of the rules below. GAP-5 does not, because it is a
distinction missing inside a declared object rather than an object missing from
the boundary, and no rule reading these declarations can see it.

Pairing deserves a word. A producer and a consumer are matched by similarity of
wording, not by a declared link, because no partner in this consortium declares
a link. Guessing is the wrong way to run an interface and the fact that the
checker has to guess is itself the finding, reported as UNLINKED_PAIR.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from model import Declaration, Direction, Kind, Partner, Provenance, all_declarations


class Severity(Enum):
    BLOCKING = "blocking"
    REPORTED = "reported"
    ADVISORY = "advisory"


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: Severity
    subject: str
    message: str

    def __str__(self) -> str:
        return f"[{self.severity.value}] {self.rule}: {self.subject}: {self.message}"


# Words that carry no discriminating meaning when matching one partner's wording
# against another's. Kept explicit rather than inline so the matching is auditable.
_NOISE = frozenset(
    "a an the of for and or to in on at by with per its it is are be available "
    "system systems level data".split()
)

_PAIR_THRESHOLD = 0.34
"""Token overlap above which two opposite-direction items are treated as a
candidate pair. Set low deliberately. A false candidate is reported and dismissed
by a human in seconds. A missed candidate is an unowned object nobody sees."""


def _tokens(item: str) -> frozenset[str]:
    words = "".join(c.lower() if c.isalnum() else " " for c in item).split()
    return frozenset(w.rstrip("s") for w in words if w not in _NOISE)


def _overlap(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def candidate_pairs(decls: list[Declaration]) -> list[tuple[Declaration, Declaration, float]]:
    """Every producer and consumer whose wording is close enough to be the same
    object, best score first, then alphabetically so the order is stable."""
    produced = [d for d in decls if d.direction is Direction.PRODUCES]
    consumed = [d for d in decls if d.direction is Direction.CONSUMES]
    pairs = []
    for p in produced:
        for c in consumed:
            if p.partner == c.partner:
                continue
            score = _overlap(p.item, c.item)
            if score >= _PAIR_THRESHOLD:
                pairs.append((p, c, score))
    pairs.sort(key=lambda t: (-t[2], t[0].partner, t[0].item, t[1].partner, t[1].item))
    return pairs


def unmatched_consumption(decls, pairs) -> list[Finding]:
    """A required input that no partner produces. The consortium cannot run."""
    matched = {id(c) for _, c, _ in pairs}
    out = []
    for d in decls:
        if d.direction is Direction.CONSUMES and id(d) not in matched:
            out.append(Finding(
                "UNMATCHED_CONSUMPTION", Severity.BLOCKING, str(d),
                f"{d.partner} requires {d.item!r} and no partner produces anything "
                f"resembling it. The input has no owner."))
    return out


def unrouted_production(decls, pairs) -> list[Finding]:
    """A published output nobody consumes. Either wasted work or a missing route."""
    matched = {id(p) for p, _, _ in pairs}
    out = []
    for d in decls:
        if d.direction is Direction.PRODUCES and id(d) not in matched:
            out.append(Finding(
                "UNROUTED_PRODUCTION", Severity.BLOCKING, str(d),
                f"{d.partner} publishes {d.item!r} and no partner consumes anything "
                f"resembling it. The output has no route."))
    return out


def unlinked_pair(pairs) -> list[Finding]:
    """Two partners are almost certainly exchanging this, and neither says so."""
    out = []
    for p, c, score in pairs:
        if p.link is not None and p.link == c.link:
            continue
        out.append(Finding(
            "UNLINKED_PAIR", Severity.BLOCKING, f"{p.partner} -> {c.partner}",
            f"{p.item!r} and {c.item!r} overlap {score:.0%} and neither declares a "
            f"contract linking them. The exchange is real and undeclared."))
    return out


def kind_mismatch(pairs) -> list[Finding]:
    """The pair is the same subject and a different sort of object."""
    out = []
    for p, c, _ in pairs:
        if Kind.UNKNOWN in (p.kind, c.kind) or p.kind is c.kind:
            continue
        out.append(Finding(
            "KIND_MISMATCH", Severity.BLOCKING, f"{p.partner} -> {c.partner}",
            f"{p.item!r} is a {p.kind.value} and {c.item!r} is a {c.kind.value}. "
            f"Converting one to the other is real work and no partner claims it."))
    return out


def resolution_mismatch(pairs) -> list[Finding]:
    """The pair meets at different scales, with no conversion named."""
    out = []
    for p, c, _ in pairs:
        for axis in ("temporal", "spatial", "epoch"):
            pc, cc = p.clause(axis), c.clause(axis)
            if pc.value is None or cc.value is None or pc.value == cc.value:
                continue
            out.append(Finding(
                "RESOLUTION_MISMATCH", Severity.BLOCKING, f"{p.partner} -> {c.partner}",
                f"{p.item!r} is {axis} {pc.value} and {c.item!r} is {axis} {cc.value}. "
                f"The conversion between them is unowned."))
    return out


def undeclared_clause(pairs) -> list[Finding]:
    """A clause the consumer needs and the producer never settles."""
    out = []
    for p, c, _ in pairs:
        for name in p.unsettled():
            out.append(Finding(
                "UNDECLARED_CLAUSE", Severity.REPORTED, f"{p.partner}: {p.item}",
                f"{name} is unstated ({Declaration.FAMILY[name]}). "
                f"{c.partner} must assume it, and its assumption is invisible."))
    return out


def inferred_clause(decls) -> list[Finding]:
    """A clause a reader inferred. Two readers will infer differently."""
    out = []
    for d in decls:
        for name in Declaration.CLAUSES:
            if d.clause(name).provenance is Provenance.INFERRED:
                out.append(Finding(
                    "INFERRED_CLAUSE", Severity.ADVISORY, f"{d.partner}: {d.item}",
                    f"{name} was inferred, not stated: {d.clause(name).value!r}."))
    return out


_ORDER = ("UNMATCHED_CONSUMPTION", "UNROUTED_PRODUCTION", "UNLINKED_PAIR",
          "KIND_MISMATCH", "RESOLUTION_MISMATCH", "UNDECLARED_CLAUSE",
          "INFERRED_CLAUSE")


def run(partners: list[Partner]) -> list[Finding]:
    """Apply every rule and return the findings in a stable order."""
    decls = all_declarations(partners)
    pairs = candidate_pairs(decls)
    findings = (
        unmatched_consumption(decls, pairs)
        + unrouted_production(decls, pairs)
        + unlinked_pair(pairs)
        + kind_mismatch(pairs)
        + resolution_mismatch(pairs)
        + undeclared_clause(pairs)
        + inferred_clause(decls)
    )
    findings.sort(key=lambda f: (_ORDER.index(f.rule), f.subject, f.message))
    return findings


def blocking(findings: list[Finding]) -> list[Finding]:
    return [f for f in findings if f.severity is Severity.BLOCKING]
