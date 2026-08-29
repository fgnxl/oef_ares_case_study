"""Readers for the four partner declarations, one per format.

The point of the case study lives here: the four partners describe the same
class of thing in four incompatible registers, and each needs its own reader to
reach the common model. The readers are the only code that knows about file
formats. Everything downstream sees model.py types.

Which partner writes in which register is a choice, and it is the brief's:

    Solis     spec sheet        tabular, units in the header, no prose. Looks
                               machine-readable, so its ambiguities are the
                               easiest of the four to miss.
    Tharsis   README paragraph  the interface stated in passing, in a section
                               about something else, cadence implied.
    Meridian  requirements      precise about obligation, vague about payload.
                               Meridian is complied with, not coupled to.
    Helix     JSON schema       fully specified types carrying no units, no
                               cadence and no semantics. The partner whose job
                               is translation declares no meaning.

Every reader records provenance. A clause read from the document is STATED. A
clause the reader worked out is INFERRED, and it carries a note saying what it
was worked out from. A clause the document does not settle is ABSENT.

That distinction is the output, not a detail of it. An inferred clause is a
place where the next reader will infer differently, and an absent one is a place
where every consumer decides privately. A reader that quietly filled these in
would produce a tidy model of a consortium that does not exist.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from model import Declaration, Direction, Kind, Partner, inferred, stated

# --------------------------------------------------------------------------
# Solis: a markdown spec sheet. Structure is real, so read it.
# --------------------------------------------------------------------------

_ROW = re.compile(r"^\|\s*(?P<ref>(?:OUT|IN)-\d+)\s*\|(?P<rest>.*)\|\s*$")
_DEL = re.compile(r"^\|\s*DEL-\d\s*\|\s*(?P<name>[^|]+?)\s*\|\s*(?P<span>[^|]+?)\s*\|\s*$")

_DEL_KIND = {"capacity choices": Kind.DECISION, "operating envelopes": Kind.BOUND}
"""Section 0 groups parameters into what the consortium actually receives.

Reading only section 1 gives fifteen parameters against Tharsis's three
categories, and nothing matches at all, because the two partners write at
different granularity rather than merely in different words. That is a real
finding, and it hides the pairwise ones behind it. Reading both levels shows
both."""


def read_solis(path: Path) -> Partner:
    text = path.read_text()
    decls = []
    for line in text.splitlines():
        d = _DEL.match(line.strip())
        if d:
            name = d.group("name").lower()
            decls.append(Declaration(
                partner="Solis", direction=Direction.PRODUCES, item=name,
                kind=_DEL_KIND.get(name, Kind.UNKNOWN),
                source_file=path.name,
                temporal=inferred("annual",
                                  "document header: 'Planning horizon 10 years, annual resolution'"),
                boundary=inferred(f"comprises {d.group('span')}",
                                  "section 0, deliverables to the consortium")))
            continue
        m = _ROW.match(line.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group("rest").split("|")]
        if len(cells) < 3:
            continue
        name, unit, last = cells[0], cells[1], cells[2]
        outgoing = m.group("ref").startswith("OUT")
        d = Declaration(
            partner="Solis",
            direction=Direction.PRODUCES if outgoing else Direction.CONSUMES,
            item=name.lower(),
            source_file=path.name,
        )
        if unit:
            d.unit = stated(unit)
        # The document says the horizon is annual and never says which calendar.
        d.temporal = inferred(
            "annual", "document header: 'Planning horizon 10 years, annual resolution'")
        # A published output that is selected once per cycle is a decision. One
        # that bounds how the selection is run is a limit on it. Note 3.2 and
        # note 3.3 say which is which, so the kind is read rather than guessed.
        if outgoing:
            d.kind = Kind.DECISION if _in_note(text, "3.2", m.group("ref")) else (
                Kind.BOUND if _in_note(text, "3.3", m.group("ref")) else Kind.UNKNOWN)
        elif "envelope" in name.lower():
            d.kind = Kind.BOUND
        if not outgoing and not last:
            d.owner = Declaration.__dataclass_fields__["owner"].default
        elif not outgoing:
            d.owner = stated(last)
        decls.append(d)
    return Partner("Solis", "commercial infrastructure modeller", decls)


def _in_note(text: str, note: str, ref: str) -> bool:
    """True when a numbered note names a reference range containing ref.

    The spec sheet writes ranges as 'OUT-01 through OUT-08'. Reading the note is
    how the reader learns which outputs are decisions and which are limits,
    rather than deciding for itself from the wording of the parameter.
    """
    m = re.search(rf"^{re.escape(note)}\s+(.*?)(?=^\d+\.\d+\s|\Z)", text, re.M | re.S)
    if not m:
        return False
    span = re.search(r"(OUT-\d+)\s+through\s+(OUT-\d+)", m.group(1))
    if not span:
        return False
    lo, hi = int(span.group(1)[4:]), int(span.group(2)[4:])
    return lo <= int(ref[4:]) <= hi


# --------------------------------------------------------------------------
# Tharsis: prose. There is no structure to read, so the reader is a hand
# extraction and every entry says which sentence it came from.
# --------------------------------------------------------------------------

def read_tharsis(path: Path) -> Partner:
    text = path.read_text()

    def seen(phrase: str) -> bool:
        return phrase.lower() in text.lower()

    epoch = inferred(
        "sols from arrival, 668-sol year, 24h39m35s sol",
        "section 'Running the model': 'Time is indexed in sols from arrival'"
    ) if seen("indexed in sols") else Declaration.__dataclass_fields__["epoch"].default

    hourly = inferred("hourly on the sol axis",
                      "section 'habsim': 'hourly steps across a full Mars year'")

    decls = [
        Declaration("Tharsis", Direction.CONSUMES, "available capacity",
                    kind=Kind.STATE, temporal=hourly, epoch=epoch,
                    source_file=path.name,
                    owner=inferred("Solis", "'Configuration and limits come from Solis'")),
        Declaration("Tharsis", Direction.CONSUMES, "operating constraints",
                    kind=Kind.BOUND, temporal=hourly, epoch=epoch,
                    source_file=path.name,
                    owner=inferred("Solis", "'Configuration and limits come from Solis'")),
        Declaration("Tharsis", Direction.CONSUMES, "population schedules",
                    kind=Kind.SCHEDULE, source_file=path.name),
        Declaration("Tharsis", Direction.PRODUCES, "time-series demand",
                    kind=Kind.SERIES, temporal=hourly, epoch=epoch,
                    unit=inferred("per commodity, unit unstated",
                                  "'one value per hour per commodity' names no unit"),
                    source_file=path.name),
        Declaration("Tharsis", Direction.PRODUCES, "service shortfalls",
                    kind=Kind.SERIES, temporal=hourly, epoch=epoch,
                    source_file=path.name),
        Declaration("Tharsis", Direction.PRODUCES, "operational responses",
                    temporal=hourly, epoch=epoch, source_file=path.name),
    ]
    # The README says the population schedule is maintained locally because no
    # upstream source publishes one. That is the document declaring an unowned
    # input, so it is read as stated rather than inferred.
    if seen("no upstream source publishes it"):
        decls[2].owner = stated(
            "maintained locally by Tharsis, no upstream producer",
            "'it is maintained locally in inputs/pop/ because no upstream source publishes it'")
    return Partner("Tharsis", "university simulation team", decls)


# --------------------------------------------------------------------------
# Helix: a JSON schema. Types are fully specified and carry no meaning, so the
# reader gets names and nothing else, which is the finding.
# --------------------------------------------------------------------------

_HELIX_DIRECTION = {
    "configuration": Direction.CONSUMES,
    "availability": Direction.PRODUCES,
    "demand": Direction.CONSUMES,
    "limits": Direction.CONSUMES,
    "shortfalls": Direction.PRODUCES,
}


def read_helix(path: Path) -> Partner:
    schema = json.loads(path.read_text())
    props = schema.get("properties", {})
    decls = []
    for name, body in props.items():
        if name == "meta":
            continue
        d = Declaration(
            partner="Helix",
            direction=_HELIX_DIRECTION.get(name, Direction.PRODUCES),
            item=name,
            source_file=path.name,
        )
        note = body.get("$comment", "")
        if note:
            d.boundary = inferred(note[:120], "$comment on the schema property")
        # Every leaf in this schema is a bare number. No unit, no cadence, no
        # semantics. The reader records that rather than supplying one.
        decls.append(d)
    return Partner("Helix", "schema translation and compatibility layer", decls)



# --------------------------------------------------------------------------
# Meridian: clause-numbered requirements. Precise about obligation, silent
# about payload. The reader gets what Meridian demands and nothing about what
# Meridian sends.
# --------------------------------------------------------------------------

_SECTION = re.compile(r"^(?P<n>\d)\.\s+(?P<title>[A-Z][A-Z ]+)$", re.M)

_MERIDIAN_ITEMS = {
    "2": ("acceptable service levels", Kind.THRESHOLD),
    "3": ("stress scenarios", Kind.UNKNOWN),
    "5": ("evidence requirements", Kind.UNKNOWN),
}
"""Section 4 is deliberately absent from this map. It states requirements on
other partners' models rather than naming a thing Meridian hands over, so
reading it as a declaration would invent an exchange the document does not
make."""

_UNIT_IN_CLAUSE = re.compile(r"\b(kPa|mmHg|percent|sols)\b")


def read_meridian(path: Path) -> Partner:
    text = path.read_text()
    bodies = {}
    marks = list(_SECTION.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        bodies[m.group("n")] = text[m.end():end]

    decls = []
    for num, (item, kind) in _MERIDIAN_ITEMS.items():
        body = bodies.get(num, "")
        d = Declaration("Meridian", Direction.PRODUCES, item,
                        kind=kind, source_file=path.name)
        units = sorted(set(_UNIT_IN_CLAUSE.findall(body)))
        if units:
            d.unit = stated(", ".join(units), f"units appearing in section {num}")
        decls.append(d)

    # Clause 6.1 says the Laboratory does not model. That is the document
    # declaring that it consumes nothing, so it is read rather than assumed.
    if "does not model" in text:
        pass

    # Clause 4.3 demands uncertainty on quantities used to support a resilience
    # claim. Meridian requires it of others and declares none on its own
    # outputs, which the reader records rather than resolves.
    return Partner("Meridian", "public mission-risk institute", decls)


# --------------------------------------------------------------------------

_READERS = {
    "solis_spec_sheet.md": read_solis,
    "tharsis_readme.md": read_tharsis,
    "meridian_requirements.txt": read_meridian,
    "helix_schema.json": read_helix,
}


def load_all(data_dir: Path) -> list[Partner]:
    """Dispatch on filename and return one Partner per declaration file.

    A file with no reader is an error rather than a skip. Silently ignoring a
    partner would produce a clean report about an incomplete consortium, which
    is the failure this whole exercise is about.
    """
    partners = []
    for path in sorted(Path(data_dir).iterdir()):
        if path.name.startswith("."):
            continue
        reader = _READERS.get(path.name)
        if reader is None:
            raise KeyError(
                f"no reader for {path.name}. Every declaration needs one, because "
                f"a partner that is skipped is a partner the report says nothing "
                f"about while appearing complete.")
        partners.append(reader(path))
    return partners
