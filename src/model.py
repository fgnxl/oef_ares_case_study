"""The contract model. Types only, no I/O, no rules.

A partner declaration is not just a name. It is a name plus the clauses a
consumer needs in order to use the thing: what it is, what it is measured in,
when and where it applies, which run it belongs to, how it arrives, and who may
change it. Those six families are the structure of Declaration below.

Every clause carries its own provenance, because the difference between a value
a partner stated and a value a reader inferred is the whole subject of this
exercise. An inferred clause is a place where two teams will infer differently.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Direction(Enum):
    PRODUCES = "produces"
    CONSUMES = "consumes"


class Kind(Enum):
    """What sort of object a declaration names.

    A decision is chosen once and holds. A bound constrains a period. A state
    varies and is observed. A series is a trajectory through time. A threshold
    is a limit something is judged against. A schedule is an exogenous plan.

    Two partners can agree on a name and still be exchanging different kinds,
    which is GAP-2: a capacity choice is a decision, available capacity is a
    state, and the difference between them is every derate that applies.
    """

    DECISION = "decision"
    BOUND = "bound"
    STATE = "state"
    SERIES = "series"
    THRESHOLD = "threshold"
    SCHEDULE = "schedule"
    UNKNOWN = "unknown"


class Provenance(Enum):
    """Where a clause value came from.

    ABSENT is the important one. It means the declaration does not settle the
    clause at all, so every consumer settles it privately. STATED and INFERRED
    are both present values, but only STATED is one the partner can be held to.
    """

    STATED = "stated"
    INFERRED = "inferred"
    ABSENT = "absent"


@dataclass(frozen=True)
class Clause:
    """One clause of a declaration, with where its value came from."""

    value: Optional[str] = None
    provenance: Provenance = Provenance.ABSENT
    note: str = ""

    @property
    def is_settled(self) -> bool:
        return self.provenance is Provenance.STATED

    def __str__(self) -> str:
        return self.value if self.value is not None else "unstated"


ABSENT = Clause()


def stated(value: str, note: str = "") -> Clause:
    return Clause(value, Provenance.STATED, note)


def inferred(value: str, note: str = "") -> Clause:
    return Clause(value, Provenance.INFERRED, note)


@dataclass
class Declaration:
    """One item a partner says it produces or consumes, with its six families.

    The clause names map to the families in docs/findings.md:
        what it is              item, kind, boundary
        what it is measured in  unit, uncertainty
        when and where          temporal, spatial, epoch
        which run               scenario
        how it arrives          cadence, encoding
        who may change it       owner
    """

    partner: str
    direction: Direction
    item: str

    kind: Kind = Kind.UNKNOWN
    boundary: Clause = ABSENT
    unit: Clause = ABSENT
    uncertainty: Clause = ABSENT
    temporal: Clause = ABSENT
    spatial: Clause = ABSENT
    epoch: Clause = ABSENT
    scenario: Clause = ABSENT
    cadence: Clause = ABSENT
    encoding: Clause = ABSENT
    owner: Clause = ABSENT

    source_file: str = ""
    link: Optional[str] = None
    """The contract this declaration belongs to, if the partner named one.

    None everywhere in this case study, which is why the checker has to guess at
    pairs rather than read them off, and why the guessing is itself a finding.
    """

    CLAUSES = (
        "boundary", "unit", "uncertainty", "temporal", "spatial",
        "epoch", "scenario", "cadence", "encoding", "owner",
    )

    FAMILY = {
        "boundary": "what it is",
        "unit": "what it is measured in",
        "uncertainty": "what it is measured in",
        "temporal": "when and where it applies",
        "spatial": "when and where it applies",
        "epoch": "when and where it applies",
        "scenario": "which run it belongs to",
        "cadence": "how it arrives",
        "encoding": "how it arrives",
        "owner": "who may change it",
    }

    def clause(self, name: str) -> Clause:
        return getattr(self, name)

    def unsettled(self) -> list[str]:
        """Clause names this declaration does not settle, in a stable order."""
        return [c for c in self.CLAUSES if not self.clause(c).is_settled]

    def __str__(self) -> str:
        return f"{self.partner} {self.direction.value} {self.item!r}"


@dataclass
class Partner:
    """A named organisation and everything it declares."""

    name: str
    role: str = ""
    declarations: list[Declaration] = field(default_factory=list)

    def produces(self) -> list[Declaration]:
        return [d for d in self.declarations if d.direction is Direction.PRODUCES]

    def consumes(self) -> list[Declaration]:
        return [d for d in self.declarations if d.direction is Direction.CONSUMES]


def all_declarations(partners: list[Partner]) -> list[Declaration]:
    """Every declaration across every partner, in partner then file order."""
    return [d for p in partners for d in p.declarations]
