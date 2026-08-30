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

import base64
import html
import json
from pathlib import Path
from string import Template

import schedule
import toy
from check import Finding, Severity, candidate_pairs
from model import Declaration, Direction, Partner, Provenance, all_declarations

TEMPLATE = Path(__file__).resolve().parent / "template.html"
ASSETS = Path(__file__).resolve().parent.parent / "assets"


def _data_uri(name: str) -> str:
    """A figure inlined as base64, because the page must open with no network.

    An <img src> pointing at a file beside the page would work locally and break
    the moment the page is mailed to somebody, which is the failure the
    self-contained rule exists to prevent.
    """
    raw = (ASSETS / name).read_bytes()
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")

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


def _provenance(d: Declaration) -> str:
    """Every clause of one declaration, with where its value came from.

    This is the part of the model a reader most needs and the page has been
    hiding. A finding that says a clause was inferred is an assertion. The same
    finding beside the sentence it was inferred from is evidence.
    """
    rows = []
    for c in Declaration.CLAUSES:
        cl = d.clause(c)
        state = cl.provenance.value
        val = _e(cl.value) if cl.value else "<em>not stated</em>"
        note = f'<span class="src">{_e(cl.note)}</span>' if cl.note else ""
        rows.append(
            f'<tr class="p-{state}"><td class="cn">{_e(c)}</td>'
            f'<td class="cf">{_e(Declaration.FAMILY[c])}</td>'
            f'<td class="cs">{state}</td><td>{val}{note}</td></tr>')
    return (
        f'<div class="detail" id="d-{_e(_key(d))}" hidden>'
        f'<h4>{_e(d.partner)} {_e(d.direction.value)} <b>{_e(d.item)}</b>'
        f'<span class="from">read from {_e(d.source_file)}</span></h4>'
        f'<div class="scroller"><table class="clauses"><thead><tr>'
        f'<th>Clause</th><th>Family</th><th>Provenance</th>'
        f'<th>Value, and the text it came from</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div></div>')


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


def toy_json() -> str:
    """The toy model's constants, embedded so the page carries its own data.

    Sorted keys and a fixed indent for the same reason model_json uses them: the
    page has to render byte-identically from identical inputs or the diff is
    unreadable.
    """
    return json.dumps(toy.payload(), indent=1, sort_keys=True)


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


def _who(attendees: tuple, decides: tuple = ()) -> str:
    """Four markers, filled where the partner is in the room.

    The seating plan carries an argument, so it is drawn rather than described.
    Helix is present in the sessions that settle what a variable means, because
    the contract being settled is the one its tooling was built against, and it
    holds the ruling in none of them.
    """
    dots = []
    for name, ch in _INITIAL.items():
        on = "rules" if name in decides else ("on" if name in attendees else "off")
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
            f'<b>{_e(s.name)}</b>{_who(s.attendees, s.decides)}'
            f'<span>{_e(s.length)}. {_e(s.purpose)}'
            + (f' <b>Ruling: {_e(", ".join(s.decides))}.</b>' if s.decides else "")
            + '</span></div>' for s in ss)
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
        'owns it, and names who holds the ruling. Helix is in the room for both '
        'contract sessions, because the contract being settled is the one its '
        'existing tooling was built against, and holds no ruling in any session, '
        'because converting between two vocabularies confers no standing to rule '
        'on what either one means. A test asserts both halves.</p>')


# ---------------------------------------------------------------------------
# The coupled toy model.
#
# The rest of this page renders an analysis. This section performs one. It runs
# a small settlement energy model twice, once for a design sized the way the
# current interface sizes things and once for a design iterated against a single
# dust state, and it draws both.
#
# The constants live in toy.py so they are testable and so every one of them can
# be rendered beside the tag that says whether a partner stated it or this
# exercise assumed it. The model itself runs in the browser, because the reader
# has to be able to move the uplift slider to zero and watch the argument for
# tight coupling disappear. A page that only asserts that would not be evidence.
#
# No clause identifier from data/ appears in any text below. Those documents are
# synthetic and were written for this exercise, so quoting a clause number back
# at a reader would be this repository's own invention presented as a partner
# requirement. Their numbers are read and used, which is what they are for.
# ---------------------------------------------------------------------------


def _num(x) -> str:
    """A number formatted for reading rather than for a machine."""
    f = float(x)
    if f.is_integer() and abs(f) >= 1000:
        return f"{int(f):,}"
    if f.is_integer():
        return str(int(f))
    return f"{f:g}"


def _fmt_value(v) -> str:
    if isinstance(v, list):
        if len(v) == 2:
            return f"{_num(v[0])} to {_num(v[1])}"
        mean = sum(v) / len(v)
        return (f"{len(v)} values, {_num(min(v))} to {_num(max(v))}, "
                f"mean {mean:.2f}")
    return _num(v)


def _tag(kind: str) -> str:
    return f'<span class="tag {_e(kind)}">{_e(kind)}</span>'


def _dial(ident: str, label: str, caption: str, lo: int, hi: int,
          value: int) -> str:
    """One slider, captioned with the tag on the number it moves."""
    return (
        f'<div class="dial">'
        f'<label for="{_e(ident)}">{_e(label)}'
        f'<b id="{_e(ident)}-v">{value}%</b></label>'
        f'<input type="range" id="{_e(ident)}" min="{lo}" max="{hi}" step="1" '
        f'value="{value}" />'
        f'<span class="cap">{_tag("assumed")} {_e(caption)}</span></div>'
    )


def _column(side: str, title: str) -> str:
    """One design column. Python draws the frame, the model fills the numbers."""
    def cell(key: str, label: str) -> str:
        return (f'<div><span>{_e(label)}</span>'
                f'<b id="{side}-{key}">&mdash;</b></div>')
    return (
        f'<article class="col" id="col-{side}">'
        f'<h3>{_e(title)}</h3>'
        f'<p class="sub" id="{side}-sub"></p>'
        f'<div class="caps">{cell("pv", "PV peak, kWe")}'
        f'{cell("batt", "Battery, kWh")}{cell("h2", "Hydrogen, kg")}</div>'
        f'<div class="big" id="{side}-big"><b id="{side}-surv">&mdash;</b>'
        f'<span>survives, of {int(toy.values()["RIDE_SOLS"])} sols'
        f'<br><i id="{side}-when"></i></span></div>'
        f'<div class="spark" id="{side}-spark"></div>'
        f'<p class="note" id="{side}-note"></p>'
        f"</article>"
    )


def _constants_table() -> str:
    rows = []
    for group in toy.groups():
        rows.append(f'<tr class="grp"><td colspan="4">{_e(group)}</td></tr>')
        for c in toy.entries():
            if c["group"] != group:
                continue
            rows.append(
                f'<tr><td class="cn">{_e(c["label"])}</td>'
                f'<td class="cv">{_e(_fmt_value(c["value"]))}'
                f'<em>{_e(c["unit"])}</em></td>'
                f'<td class="cs">{_tag(c["tag"])}</td>'
                f'<td class="csrc">{_e(c["source"])}</td></tr>')
    stated, assumed = toy.counts()
    return (
        '<div class="scroller"><table class="consts"><thead><tr>'
        '<th>Constant</th><th>Value</th><th>Provenance</th>'
        f'<th>Where it came from ({stated} stated, {assumed} assumed)</th>'
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


_LIMITS = (
    "Nothing here carries uncertainty. Every number is one deterministic run of "
    "one set of assumptions, and a range is not the same object as a point.",
    "Only electricity is modelled. Water, oxygen, buffer gas, thermal duty and "
    "carbon dioxide removal are the loads that actually end a settlement first, "
    "and none of them is here.",
    "The dust state is one scalar with one shape. A real event varies over the "
    "site, over the spectrum and over the sol, and its optical depth is not a "
    "slider.",
    "The reactor never turns down, no unit ever fails, and no maintenance is "
    "scheduled. The availability derate is a single assumed number standing in "
    "for a function nobody owns.",
    "The demand uplift is the pivot of the whole comparison and it is assumed. "
    "Its direction is physically robust, because the habitat loses passive "
    "solar gain and daylight has to be replaced electrically, while suspended "
    "external work pushes the other way. Its magnitude is established by "
    "nothing. Set it to zero and the comparison collapses, which is the honest "
    "way to show what the argument rests on.",
    "Per resident demand, the diurnal shape, the array capacity factor and the "
    "sheddable fraction were all chosen here. No partner publishes any of them.",
    "This is a toy. It is an argument about what coupling changes, not a "
    "settlement design, and no configuration it prints should be built.",
)


def _toy_section() -> str:
    v = toy.values()
    return (
        '<section class="toy">'
        '<h2 class="toy-h">Would this settlement survive the storm. '
        'Two ways of asking.</h2>'
        '<p class="lede">A dust storm cuts generation and raises demand from '
        'the same cause. The left column sizes a settlement the way the current '
        'interface sizes one, against a single exchanged bound, so the '
        'correlation between the two is destroyed before the sizing starts. The '
        'right column starts from that design and iterates it against one dust '
        'state, where generation and demand move together because they are '
        'driven by the same variable. Both are then run through the same '
        'coupled model. Every number below is tagged with whether a partner '
        'stated it or this page assumed it.</p>'
        '<div class="dials">'
        + _dial("sev", "Storm severity",
                "peak insolation loss at the array", 0, 95,
                int(round(v["SEVERITY_DEFAULT"] * 100)))
        + _dial("up", "Demand uplift under storm",
                "thermal and lighting load, net of suspended external work",
                0, 40, int(round(v["UPLIFT_DEFAULT"] * 100)))
        + _dial("shed", "Sheddable fraction of load",
                "load that can be switched off under stress", 0, 50,
                int(round(v["SHEDDABLE_DEFAULT"] * 100)))
        + '<div class="dial"><label>Envelope statistic'
          '<b id="env-v">P95</b></label>'
          '<div class="controls" id="env">'
          '<button type="button" data-p="50" aria-pressed="false">P50</button>'
          '<button type="button" data-p="95" aria-pressed="true">P95</button>'
          '<button type="button" data-p="99" aria-pressed="false">P99</button>'
          '</div><span class="cap">' + _tag("assumed")
        + ' which statistic of an hourly trace becomes the one exchanged bound. '
          'Left column only</span></div>'
        '</div>'
        '<div class="duo">'
        + _column("loose", "Loose, bounds exchanged once")
        + _column("tight", "Tight, iterated on one dust state")
        + '</div>'
        '<p class="sparkkey">Both charts share one pair of axes, so the columns '
        'are directly comparable. <i class="sw dem"></i> demand after shedding '
        'and uplift, <i class="sw gen"></i> generation available, '
        '<i class="sw sto"></i> energy in store, battery plus hydrogen, '
        '<i class="sw fail"></i> the first hour a load goes unserved.</p>'
        '<p class="verdict" id="verdict"></p>'
        '<div id="ceiling"></div>'
        '<h3 class="toy-sub">The constants, and where each one came from</h3>'
        + _constants_table()
        + '<p class="legend">Per resident demand is the one assumed constant '
          'chosen rather than researched. It is set where the design space the '
          'power partner declares actually closes, meaning the sizing rule '
          'lands inside the declared range for the array and the battery '
          'instead of running off the top of every one of them at once. A '
          'higher figure does not make the settlement fail more interestingly, '
          'it makes both columns identical at the ceiling and the comparison '
          'shows nothing.</p>'
        '<h3 class="toy-sub">What this does not establish</h3>'
        '<ul class="limits">'
        + "".join(f"<li>{_e(x)}</li>" for x in _LIMITS)
        + '</ul></section>'
    )


def _storage_figure() -> str:
    """The unowned-load figure, which now sits directly under the toy model.

    It answers the question the model above raises. The model shows that
    survival turns on how much load can be switched off. This shows what the
    load that cannot be switched off costs in landed mass, which is the number
    neither partner can compute alone.
    """
    return (
        "<h2>What an unowned load costs</h2>"
        '<p class="legend">GAP-5 is the split between load that can be shed '
        'under stress and load that cannot, and no partner declares it. It is '
        'the sheddable slider above, and it moves the answer there more than '
        'any other control. This is what it costs. A settlement has to ride out '
        'a planet-encircling dust event, and the reference mission sizes for '
        '120 sols, which is 2,959 hours. So every kilowatt that cannot be '
        'switched off needs 2,959 kWh of stored energy. The figure is the mass '
        'that implies. The multiplier is fixed. How many kilowatts it applies '
        'to is the number neither partner can compute alone.</p>'
        f'<figure class="fig"><img alt="Mass of stored energy required per '
        f'kilowatt of non-sheddable load through a 120 sol dust storm, by '
        f'storage technology" src="{_data_uri("storage_mass.png")}">'
        '<figcaption>Reactant mass only for the fuel cell cases, so the real '
        'system mass is higher. Comparators are illustrative and not tied to '
        'any mission cargo budget.</figcaption></figure>'
    )


def page(partners: list[Partner], findings: list[Finding]) -> str:
    """The whole artifact, as one string. No I/O, so it is testable."""
    matched = _matched(partners)
    body = (
        '<div class="wrap">'
        f"<h1>{_e(TITLE)}</h1>"
        f'<p class="lede">{_e(LEDE)}</p>'
        + _toy_section()
        + _storage_figure()
        + f'<div class="counts">{_counts(partners, findings)}</div>'
        + "<h2>The boundary</h2>"
        + f'<div class="grid">{"".join(_partner_card(p, matched) for p in partners)}</div>'
        + '<p class="legend"><b>Solid</b> means the item is part of an exchange '
        'this tool could identify. <b>Broken</b> means it is not: an input no '
        'partner produces, or an output no partner consumes. Select any item to '
        'filter the findings to it.</p>'
        "<h2>The six weeks</h2>"
        + _calendar() +
        '<h2>Where a finding comes from</h2>'
        '<p class="legend">Select any item above. Every clause of that '
        'declaration is listed with what the reader found, whether the document '
        '<b>stated</b> it, whether the reader <b>inferred</b> it and from which '
        'sentence, or whether it is <b>absent</b> and every consumer therefore '
        'decides privately. This is the whole of the evidence behind the '
        'findings below.</p>'
        '<p class="empty-detail" id="nodetail">Nothing selected.</p>'
        + "".join(_provenance(d) for d in all_declarations(partners)) +
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
        title=TITLE, body=body, data=model_json(partners, findings),
        toy=toy_json())
