"""Renders the model and the findings into one self-contained HTML file.

Self-contained is a hard requirement, not a preference: the page has to open
from disk on a laptop with no network and no server. CSS and JavaScript are
inlined into template.html. No CDN, no fetch, no build step, no framework.

Interactivity is limited to what a reader needs to follow the argument:
selecting a partner or a contract and seeing what depends on it.

The visual language is the argument. Each partner is drawn as an interior with
a boundary, and an item on that boundary is solid where the consortium has an
owner for it and broken where it does not. An unowned object is not a row in an
error table, it is a hole in the boundary, which is what it actually is.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from string import Template

import schedule
from check import Finding, Severity, candidate_pairs
from model import Declaration, Direction, Partner, Provenance, all_declarations

TEMPLATE = Path(__file__).resolve().parent / "template.html"

TITLE = "ARES interface map"
LEDE = ("Every partner declaration in the consortium, read as an interface "
        "contract. Solid where an exchange has an owner on both sides, broken "
        "where it does not.")


def _key(d: Declaration) -> str:
    return f"{d.partner}:{d.item}"


def _e(s: str) -> str:
    return html.escape(str(s), quote=True)


def _matched(partners: list[Partner]) -> set[str]:
    """Keys that appear in at least one candidate pair."""
    keys = set()
    for p, c, _ in candidate_pairs(all_declarations(partners)):
        keys.add(_key(p))
        keys.add(_key(c))
    return keys


def _chip(d: Declaration, matched: set[str]) -> str:
    state = "matched" if _key(d) in matched else "orphan"
    bits = []
    if d.unit.value:
        bits.append(_e(d.unit.value))
    if d.temporal.value:
        bits.append(_e(d.temporal.value))
    if d.kind.value != "unknown":
        bits.append(_e(d.kind.value))
    unsettled = len(d.unsettled())
    bits.append(f"{unsettled} clause{'s' if unsettled != 1 else ''} unstated")
    return (
        f'<button class="chip {state}" data-key="{_e(_key(d))}" aria-pressed="false">'
        f'{_e(d.item)}<em>{" &middot; ".join(bits)}</em></button>'
    )


def _surface(label: str, decls: list[Declaration], matched: set[str]) -> str:
    if not decls:
        return (f'<div class="surface"><span>{label}</span>'
                f'<p class="empty">nothing declared</p></div>')
    chips = "".join(_chip(d, matched) for d in decls)
    return f'<div class="surface"><span>{label}</span>{chips}</div>'


def _partner_card(p: Partner, matched: set[str]) -> str:
    return (
        '<article class="partner">'
        f'<h3>{_e(p.name)}</h3><p class="role">{_e(p.role)}</p>'
        + _surface("consumes", p.consumes(), matched)
        + _surface("produces", p.produces(), matched)
        + "</article>"
    )


def _rows(findings: list[Finding], partners: list[Partner]) -> str:
    keys = [_key(d) for d in all_declarations(partners)]
    out = []
    for f in findings:
        touched = "|".join(k for k in keys if k.split(":", 1)[1] in f.message
                           or k == f.subject.replace(" produces ", ":").replace(" consumes ", ":"))
        out.append(
            f'<tr class="{f.severity.value}" data-items="{_e(touched)}">'
            f'<td class="rule">{_e(f.rule)}</td>'
            f'<td class="subject">{_e(f.subject)}</td>'
            f'<td>{_e(f.message)}</td></tr>'
        )
    return "".join(out)


def _counts(partners: list[Partner], findings: list[Finding]) -> str:
    decls = all_declarations(partners)
    stated = sum(1 for d in decls for c in Declaration.CLAUSES
                 if d.clause(c).provenance is Provenance.STATED)
    total = len(decls) * len(Declaration.CLAUSES)
    pairs = len(candidate_pairs(decls))
    blocking = sum(1 for f in findings if f.severity is Severity.BLOCKING)
    items = [
        (len(partners), "partners"),
        (len(decls), "declarations"),
        (f"{stated}/{total}", "clauses stated"),
        (pairs, "exchanges identifiable"),
        (blocking, "blocking findings"),
    ]
    return "".join(f'<div class="count"><b>{_e(v)}</b><span>{_e(l)}</span></div>'
                   for v, l in items)


def model_json(partners: list[Partner], findings: list[Finding]) -> str:
    """The model as embedded JSON, so the page carries its own data.

    Sorted keys and a fixed separator, because the page has to render
    byte-identically from identical inputs.
    """
    payload = {
        "partners": [
            {
                "name": p.name,
                "role": p.role,
                "declarations": [
                    {
                        "item": d.item,
                        "direction": d.direction.value,
                        "kind": d.kind.value,
                        "source": d.source_file,
                        "clauses": {
                            c: {"value": d.clause(c).value,
                                "provenance": d.clause(c).provenance.value,
                                "note": d.clause(c).note}
                            for c in Declaration.CLAUSES
                        },
                    }
                    for d in p.declarations
                ],
            }
            for p in partners
        ],
        "findings": [
            {"rule": f.rule, "severity": f.severity.value,
             "subject": f.subject, "message": f.message}
            for f in findings
        ],
    }
    return json.dumps(payload, indent=1, sort_keys=True)



_INITIAL = {"Solis": "S", "Tharsis": "T", "Meridian": "M", "Helix": "H"}


def _who(attendees: tuple) -> str:
    """Four markers, filled where the partner is in the room.

    The seating plan carries an argument, so it is drawn rather than described.
    Helix is present for every technical session and absent from every session
    that settles what a variable means.
    """
    dots = []
    for name, ch in _INITIAL.items():
        on = "on" if name in attendees else "off"
        dots.append(f'<i class="dot {on}" title="{_e(name)}">{ch}</i>')
    return f'<span class="who">{"".join(dots)}</span>'


def _calendar() -> str:
    weeks = range(1, 7)
    cols = []
    for w in weeks:
        ms = [m for m in schedule.MILESTONES if m.week == w]
        ss = [s for s in schedule.SESSIONS if s.week == w]
        mile = "".join(
            f'<div class="mile {_e(m.kind)}"><b>{_e(m.name)}</b>'
            f"<span>{_e(m.detail)}</span></div>" for m in ms)
        sess = "".join(
            f'<div class="sess{" auth" if s.authority else ""}">'
            f'<b>{_e(s.name)}</b>{_who(s.attendees)}'
            f'<span>{_e(s.length)}. {_e(s.purpose)}</span></div>' for s in ss)
        gate = schedule.REVIEW_POINTS.get(w)
        gatehtml = f'<div class="gate">{_e(gate)}</div>' if gate else ""
        cols.append(
            f'<div class="week"><h4>Week {w}</h4>{mile}{sess}{gatehtml}</div>')

    bars = "".join(
        f'<div class="bar{" crit" if t.critical else ""}" '
        f'style="grid-column: {min(t.weeks)} / {max(t.weeks) + 1}">'
        f"<b>{_e(t.name)}</b><span>{_e(t.detail)}</span></div>"
        for t in schedule.TRACKS)

    return (
        f'<div class="callout">{_e(schedule.ALWAYS_DEMONSTRABLE)}</div>'
        f'<div class="bars">{bars}</div>'
        f'<div class="cal">{"".join(cols)}</div>'
        '<p class="legend">Markers show who is in the room: '
        '<i class="dot on">S</i> Solis, <i class="dot on">T</i> Tharsis, '
        '<i class="dot on">M</i> Meridian, <i class="dot on">H</i> Helix. '
        'A session with a <b>blue rule</b> settles what a variable means or who '
        'owns it. Helix attends every technical session and no authority session, '
        'because a translation layer converts between vocabularies and cannot '
        'rule on meaning. A test asserts it.</p>')

def page(partners: list[Partner], findings: list[Finding]) -> str:
    """The whole artifact, as one string. No I/O, so it is testable."""
    matched = _matched(partners)
    body = (
        '<div class="wrap">'
        f"<h1>{_e(TITLE)}</h1>"
        f'<p class="lede">{_e(LEDE)}</p>'
        f'<div class="counts">{_counts(partners, findings)}</div>'
        "<h2>The boundary</h2>"
        f'<div class="grid">{"".join(_partner_card(p, matched) for p in partners)}</div>'
        '<p class="legend"><b>Solid</b> means the item is part of an exchange '
        'this tool could identify. <b>Broken</b> means it is not: an input no '
        'partner produces, or an output no partner consumes. Select any item to '
        'filter the findings to it.</p>'
        "<h2>The six weeks</h2>"
        + _calendar() +
        "<h2>Findings</h2>"
        '<div class="controls">'
        '<button data-severity="all" aria-pressed="true">all</button>'
        '<button data-severity="blocking" aria-pressed="false">blocking</button>'
        '<button data-severity="reported" aria-pressed="false">reported</button>'
        '<button data-severity="advisory" aria-pressed="false">advisory</button>'
        "</div>"
        '<div class="scroller"><table id="findings"><thead><tr><th>Rule</th><th>Subject</th>'
        f'<th>Finding (<span id="shown">{len(findings)}</span> shown)</th>'
        f"</tr></thead><tbody>{_rows(findings, partners)}</tbody></table></div>"
        "<footer>Generated from the four partner declarations in "
        "<code>data/</code>. No rule in the checker names a partner, an item or "
        "a finding: applied to a boundary where every object has an owner and "
        "every clause is stated, it returns nothing. The declarations are "
        "synthetic and were written for this exercise."
        "</footer></div>"
    )
    return Template(TEMPLATE.read_text()).substitute(
        title=TITLE, body=body, data=model_json(partners, findings))
