"""Renders the coupled toy model into one self-contained HTML file.

The page is one thing: a settlement energy model run twice, once for a design
sized the way the current interface sizes things and once for a design iterated
against a single dust state, drawn side by side and driven by four controls.

Self-contained is a hard requirement, not a preference: the page has to open
from disk on a laptop with no network and no server. CSS and JavaScript are
inlined into template.html. No CDN, no fetch, no build step, no framework.

The constants live in toy.py so they are testable and so every one of them can
be rendered beside the tag that says whether a partner stated it or this
exercise assumed it. The model itself runs in the browser, because the reader
has to be able to move the uplift slider to zero and watch the argument for
tight coupling disappear. A page that only asserts that would not be evidence.

The checker is no longer rendered. It reads the partner declarations in data/,
applies the rules and reports on the command line, which is where a gate
belongs. `make check` still exits non-zero on a blocking finding. Nothing it
produces reaches this page.

No clause identifier from data/ appears in any text here. Those documents are
synthetic and were written for this exercise, so quoting a clause number back at
a reader would be this repository's own invention presented as a partner
requirement. Their numbers are read and used, which is what they are for.
"""

from __future__ import annotations

import base64
import html
import json
from pathlib import Path
from string import Template

import toy
from check import Finding
from model import Partner

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


TITLE = "Sizing a settlement for the storm"
HEADING = ("Sizing a settlement for a dust storm: one model alone, or two "
           "revising against each other")
LEDE = (
    "Solis sizes generation and storage over multi-year horizons. Tharsis "
    "simulates habitat demand hour by hour. On the left, Solis picks a "
    "capacity from a single demand number and stops. On the right, Solis "
    "picks, watches Tharsis run the storm against that choice, and revises. "
    "Those are two different settlement designs, one sized the way the "
    "partners work today and one sized with the two models talking to each "
    "other, and both are then put through the same storm in the same "
    f"simulation. What differs is not the prediction, it is what got built, "
    f"and how many of the {int(toy.values()['RIDE_SOLS'])} sols it lasts. "
    "Every number below is tagged with whether a partner stated it or this "
    "exercise assumed it.")


def _opening() -> list[str]:
    """Four short paragraphs that let a reader who knows nothing follow.

    Every number in them is read from toy.py rather than typed here, so the
    prose cannot drift away from the model the page actually runs.
    """
    v = toy.values()
    pop = int(v["POP"])
    per_cap = float(v["PER_CAP_KW"])
    draw = pop * per_cap
    fission = float(v["FISSION_KW"])
    ride = int(v["RIDE_SOLS"])
    sol = float(v["SOL_HOURS"])
    return [
        f"The settlement being sized here is a phase 1 Mars habitat holding "
        f"{_num(pop)} residents. At {per_cap} kW of continuous electrical "
        f"demand each it draws roughly {_num(draw)} kW around the clock, "
        f"against {_num(fission)} kW of installed fission surface power, so "
        f"the balance has to come from solar arrays and from whatever those "
        f"arrays can put into store. That power is not amenity. It runs air "
        f"revitalisation and carbon dioxide removal, water recovery, heating "
        f"against a night that falls well below freezing, lighting on a "
        f"{sol:.2f} hour sol, and the growing space. It is the reason anybody "
        f"inside is alive.",

        f"Mars has planet-encircling dust storms. The research record puts the "
        f"large events on the order of {ride} sols, and while one is overhead "
        f"the optical depth is deep enough that output from a solar array "
        f"falls to a small fraction of its clear sky figure, in the worst of "
        f"it a few percent. The load does not fall with it. If anything it "
        f"rises, because the habitat loses passive solar gain and daylight has "
        f"to be replaced electrically. NASA's own surface power planning for "
        f"Mars carries a ride through case of the same {ride} sol order, which "
        f"is where the target on this page comes from.",

        "So this model exists to ask two things. Whether a settlement sized "
        "the way such things are normally sized survives that storm at all, "
        "and whether sizing it with two models revising against each other "
        "produces a materially different design. The page runs the same "
        "settlement twice and puts both through the same storm.",

        "The two models belong to different organisations. Solis sizes "
        "generating and storage capacity over multi-year horizons, which is "
        "the long view that picks an array, a battery bank and a hydrogen "
        "store. Tharsis simulates habitat demand hour by hour, which is the "
        "short view that knows when the load actually arrives. Below, two "
        "columns compare what each way of working builds. On the left "
        "Solis picks a capacity from a single demand number and stops. On "
        "the right it picks, watches Tharsis run the storm against that "
        "choice, and revises. Both designs then face the same storm.",
    ]


def _e(s: str) -> str:
    return html.escape(str(s), quote=True)


def toy_json() -> str:
    """The toy model's constants, embedded so the page carries its own data.

    Sorted keys and a fixed indent, because the page has to render
    byte-identically from identical inputs or the diff is unreadable.
    """
    return json.dumps(toy.payload(), indent=1, sort_keys=True)


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
                f'<b id="{side}-{key}">&middot;</b></div>')
    return (
        f'<article class="col" id="col-{side}">'
        f'<h3>{_e(title)}</h3>'
        f'<p class="sub" id="{side}-sub"></p>'
        f'<p class="lab">What gets built</p>'
        f'<div class="caps">{cell("pv", "PV peak, kWe")}'
        f'{cell("batt", "Battery, kWh")}{cell("h2", "Hydrogen, kg")}</div>'
        f'<p class="lab">What the storm does to it</p>'
        f'<div class="big" id="{side}-big"><b id="{side}-surv">&middot;</b>'
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


def _storage_figure() -> str:
    """The mass under the hydrogen number the two columns disagree about.

    Supporting material for the model above rather than a topic of its own. The
    columns print a hydrogen store in kilograms and the sheddable slider moves
    that store more than any other control, so what a kilogram of it costs to
    land is part of reading the columns, not a separate subject.
    """
    return (
        '<h3 class="toy-sub">What the store above weighs</h3>'
        '<p class="legend">The two columns disagree most about the hydrogen '
        'store, and the sheddable slider moves it more than any other control. '
        'The split between load that can be switched off under stress and load '
        'that cannot is the number that sets it, and no partner declares where '
        'that split falls. This is what the half that cannot be switched off '
        'costs to land. Riding out a planet-encircling event of 120 sols is '
        '2,959 hours, so every kilowatt of it needs 2,959 kWh in store. The '
        'multiplier is fixed. How many kilowatts it applies to is the number '
        'neither partner can compute alone.</p>'
        f'<figure class="fig"><img alt="Mass of stored energy required per '
        f'kilowatt of non-sheddable load through a 120 sol dust storm, by '
        f'storage technology" src="{_data_uri("storage_mass.png")}">'
        '<figcaption>Reactant mass only for the fuel cell cases, so the real '
        'system mass is higher. Comparators are illustrative and not tied to '
        'any mission cargo budget.</figcaption></figure>'
    )


def _widget() -> str:
    """The page. Controls, two designs, a computed verdict, and the constants."""
    v = toy.values()
    return (
        '<section class="toy">'
        f'<h1>{_e(HEADING)}</h1>'
        f'<p class="lede">{_e(LEDE)}</p>'
        + "".join(f'<p class="opening">{_e(p)}</p>'
                   for p in _opening())
        +         '<div class="dials">'
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
        + _column("loose", "Loose: Solis picks a capacity and stops")
        + _column("tight", "Tight: Solis revises against Tharsis running "
                           "the storm")
        + '</div>'
        '<p class="sparkkey">Both charts share one pair of axes, so the two '
        'columns are directly comparable. <i class="sw raw"></i> demand as the '
        'storm raises it, <i class="sw dem"></i> demand actually served after '
        'shedding, <i class="sw gen"></i> generation available, '
        '<i class="sw sto"></i> energy in store, battery plus hydrogen, '
        '<i class="sw fail"></i> the first hour a load goes unserved. The '
        'dashed line rising while the green one falls is the correlation, and '
        'it is the thing a single exchanged number cannot carry.</p>'
        '<p class="verdict" id="verdict"></p>'
        '<div id="ceiling"></div>'
        + _storage_figure()
        + '<h3 class="toy-sub">The constants, and where each one came from</h3>'
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



# Where the values came from. Only sources that underpin something on this
# page: surface power, the Mars solar resource and dust, habitat load and life
# support. The partner declarations in data/ are this repository's own
# worldbuilding and are not references, so nothing below is attributed to them.
_REFERENCES: tuple[tuple[str, tuple[tuple[str, str, str, str, str], ...]], ...] = (
    ("Surface power, storage and mission architecture", (
        ("Rucker, M. A.", "2016",
         "Surface Power for Mars",
         "NASA Mars Study Capability Team, NTRS 20160014032",
         "https://ntrs.nasa.gov/api/citations/20160014032/downloads/20160014032.pdf"),
        ("Smith, B., Mason, L., Palac, D. and Gibson, M.", "2018",
         "Kilopower: Small and Affordable Fission Power Systems for Space",
         "NASA Glenn Research Center, NTRS 20180000691",
         "https://ntrs.nasa.gov/api/citations/20180000691/downloads/20180000691.pdf"),
        ("NASA Glenn Research Center", "2014",
         "Kilowatt-Class Fission Power Systems for Science and Human Precursor "
         "Missions",
         "NTRS 20140010823",
         "https://ntrs.nasa.gov/api/citations/20140010823/downloads/20140010823.pdf"),
        ("Guzik, M. C., Jakupca, I. J., Gilligan, R. P., Bennett, W. R., "
         "Smith, P. J. and Fincannon, J.", "2017",
         "Regenerative Fuel Cell Power Systems for Lunar and Martian Surface "
         "Exploration, AIAA-2017-5368",
         "NASA Glenn Research Center, AIAA SPACE Forum, NTRS 20170009088",
         "https://ntrs.nasa.gov/api/citations/20170009088/downloads/20170009088.pdf"),
        ("NASA Glenn Research Center", "2006",
         "Round Trip Energy Efficiency of NASA Glenn Regenerative Fuel Cell "
         "Systems",
         "NTRS 20060008706",
         "https://ntrs.nasa.gov/api/citations/20060008706/downloads/20060008706.pdf"),
        ("NASA", "2010",
         "A Study on Advanced Lithium-Based Battery Cell Design",
         "NTRS 20100033740",
         "https://ntrs.nasa.gov/api/citations/20100033740/downloads/20100033740.pdf"),
        ("NASA", "1995",
         "Solar-Electrochemical Power System for a Mars Mission",
         "NTRS 19950012155",
         "https://ntrs.nasa.gov/api/citations/19950012155/downloads/19950012155.pdf"),
        ("NASA Mars Architecture Steering Group (Drake, B. G., ed.)", "2009",
         "Human Exploration of Mars Design Reference Architecture 5.0, "
         "NASA-SP-2009-566",
         "NASA",
         "https://www.nasa.gov/wp-content/uploads/2015/09/373665main_nasa-sp-2009-566.pdf"),
    )),
    ("The Mars solar resource and dust", (
        ("Appelbaum, J. and Flood, D. J.", "1989",
         "Solar Radiation on Mars, NASA Technical Memorandum 102299",
         "NASA, NTRS 19890018252",
         "https://ntrs.nasa.gov/api/citations/19890018252/downloads/19890018252.pdf"),
        ("Landis, G. A. and others", "2004",
         "Mars Solar Power",
         "NASA, NTRS 20040191326",
         "https://ntrs.nasa.gov/api/citations/20040191326/downloads/20040191326.pdf"),
        ("Hartwick, V. L., Toon, O. B., Lundquist, J. K., Pierpaoli, O. and "
         "Kahre, M.", "2022",
         "Assessment of Wind Energy Resource Potential for Future Human "
         "Missions to Mars",
         "Research Square preprint of Nature Astronomy, "
         "doi 10.1038/s41550-022-01851-4",
         "https://www.researchsquare.com/article/rs-1510777/v1.pdf"),
        ("Guzewich, S. D. and others", "2019",
         "Mars Science Laboratory Observations of the 2018 / Mars Year 34 "
         "Global Dust Storm",
         "Geophysical Research Letters",
         ""),
    )),
    ("Habitat load and life support", (
        ("Ewert, M. K., Chen, T. T. and Powell, C. D.", "2022",
         "Life Support Baseline Values and Assumptions Document, "
         "NASA/TP-2015-218570/REV2",
         "NASA Johnson Space Center, NTRS 20210024855",
         "https://ntrs.nasa.gov/api/citations/20210024855/downloads/BVAD_2.15.22-final.pdf"),
        ("NASA", "2010",
         "Human Integration Design Handbook, NASA/SP-2010-3407",
         "NTRS 20130000738",
         "https://ntrs.nasa.gov/api/citations/20130000738/downloads/20130000738.pdf"),
        ("NASA Office of the Chief Health and Medical Officer", "2023",
         "NASA-STD-3001 Volume 2 Revision D: Human Factors, Habitability and "
         "Environmental Health",
         "NASA",
         "https://www.nasa.gov/wp-content/uploads/2023/11/nasa-std-3001-vol-2-rev-d-with-signature.pdf"),
        ("NASA Office of the Chief Health and Medical Officer", "2023",
         "NASA-STD-3001 Technical Brief: Carbon Dioxide, OCHMO-TB-004 Rev D",
         "NASA",
         "https://www.nasa.gov/wp-content/uploads/2023/12/ochmo-tb-004-carbon-dioxide.pdf"),
        ("NASA Office of the Chief Health and Medical Officer", "2023",
         "NASA-STD-3001 Technical Brief: Exercise Overview, OCHMO-TB-031",
         "NASA",
         "https://www.nasa.gov/wp-content/uploads/2023/12/ochmo-tb-031-exercise-overview.pdf"),
        ("NASA Johnson Space Center", "2023",
         "Environmental Control and Life Support System Options for Mars "
         "Transit and Mars Surface Missions",
         "52nd International Conference on Environmental Systems, "
         "NTRS 20230002103",
         "https://ntrs.nasa.gov/api/citations/20230002103/downloads/Environmental%20Control%20and%20Life%20Support%20System%20(ECLSS)%20Options%20for%20Mars%20Transit%20and%20Mars%20Surface%20Missions%20(ICES%202023)%20-%20Final%20Submission.pdf"),
        ("Knox, J. and others", "2015",
         "Optimization of the Carbon Dioxide Removal Assembly in Support of "
         "the International Space Station and Advanced Exploration Systems",
         "NASA, NTRS 20150016500",
         "https://ntrs.nasa.gov/api/citations/20150016500/downloads/20150016500.pdf"),
        ("NASA Johnson Space Center", "2023",
         "Status of ISS Water Management and Recovery",
         "52nd International Conference on Environmental Systems, "
         "NTRS 20230006217",
         "https://ntrs.nasa.gov/api/citations/20230006217/downloads/ICES%202023-097%20Status%20of%20ISS%20Water%20Management%20and%20Recovery.pdf"),
        ("NASA", "2015",
         "Environmental Control and Life Support System, NASA Facts sheet",
         "NASA",
         "https://www.nasa.gov/wp-content/uploads/2015/03/104840main_eclss.pdf"),
    )),
    ("Settlement scale and the sol", (
        ("Multiple authors", "2021",
         "How to Live on Mars With a Proper Circadian Clock?",
         "Frontiers in Astronomy and Space Sciences",
         "https://www.frontiersin.org/journals/astronomy-and-space-sciences/articles/10.3389/fspas.2021.796943/pdf"),
        ("Author per arXiv listing", "2021",
         "Plan for Building a 1000 Person Martian Colony (preprint, not peer "
         "reviewed, used only as a scale illustration)",
         "arXiv 2112.06145",
         "https://arxiv.org/pdf/2112.06145"),
    )),
)

_NOT_RETRIEVED = ("Not retrieved. Wiley paywalls it and no open copy was "
                  "found, so this page uses none of the optical depth "
                  "figures it reports.")


def _references() -> str:
    """The reference list at the foot of the page.

    URLs are printed as text rather than as anchors, because an href to an
    external host is exactly what the self-contained rule forbids and what the
    test for it catches.
    """
    parts = [
        '<div class="refs"><h2>Where the values came from</h2>'
        '<p class="legend">These are the published sources behind the numbers '
        'on this page. The four partner organisations named here are '
        'fictional, and the declarations this repository reads them from were '
        'written for this exercise, so nothing below is attributed to a '
        'partner. Every reference is a real document.</p>'
    ]
    for group, items in _REFERENCES:
        parts.append(f"<h3>{_e(group)}</h3><ol>")
        for author, year, title, venue, url in items:
            tail = (f'<span class="u">{_e(url)}</span>' if url
                    else _e(_NOT_RETRIEVED))
            parts.append(
                f"<li><b>{_e(author)} ({_e(year)}).</b> {_e(title)}. "
                f"{_e(venue)}. {tail}</li>")
        parts.append("</ol>")
    parts.append("</div>")
    return "".join(parts)


def reference_count() -> int:
    """How many references the page carries. Asserted by the tests."""
    return sum(len(items) for _, items in _REFERENCES)

def page(partners: list[Partner], findings: list[Finding]) -> str:
    """The whole artifact, as one string. No I/O, so it is testable.

    The parsed declarations and the checker's findings are accepted and not
    rendered. The checker is a command line gate now, so build.py can hold the
    model it checked without any of it reaching the page, and the signature
    stays the one build.py calls inside write_text.
    """
    body = (
        '<div class="wrap">'
        + _widget()
        + _references()
        + "<footer>A toy, built for a candidate case study. One deterministic "
        "run of one set of assumptions, and no configuration it prints should "
        "be built. Its constants are read from four synthetic partner "
        "declarations written for this exercise, which live in <code>data/"
        "</code> and are checked on the command line by <code>make check</code>."
        "</footer></div>"
    )
    return Template(TEMPLATE.read_text()).substitute(
        title=TITLE, body=body, toy=toy_json())
