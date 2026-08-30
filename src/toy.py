"""Constants for the coupled toy model, each carrying where its value came from.

The page runs a small settlement energy model twice, once for a design sized the
way the current interface sizes things and once for a design iterated against a
single dust state. The two runs need about thirty numbers. Some of those numbers
a partner declared. Most of them nobody did, and somebody had to choose them for
this to run at all.

That distinction is the whole subject of the repository, so it is carried in the
data rather than in a caption. Every constant is a Const with a tag in
{stated, assumed} and a source, the page renders the tag beside the value, and a
test asserts that no entry can reach the page without both.

The constants live in Python rather than in the template so they are testable
and so there is one place to change a number. The model that consumes them runs
in JavaScript in the browser, because the reader has to be able to move a slider
and watch the answer move.

Nothing here cites a clause identifier from data/. The declarations in data/ are
synthetic and were written for this exercise, so a clause number quoted back at
a reader would be this repository's own invention presented as a partner's
requirement. The values are read from those documents, which is what they are
for. The provenance strings name the parameter in words instead.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Union

STATED = "stated"
ASSUMED = "assumed"
TAGS = (STATED, ASSUMED)

Value = Union[float, int, Sequence[float]]


@dataclass(frozen=True)
class Const:
    """One constant, its units, and whether a partner stated it or we chose it.

    `tag` is the load-bearing field. STATED means a partner's own document
    carries the value and the consortium can hold them to it. ASSUMED means this
    exercise picked it, and a reader who disagrees is entitled to move it.
    """

    key: str
    label: str
    value: Value
    unit: str
    tag: str
    source: str
    group: str

    def __post_init__(self) -> None:
        if self.tag not in TAGS:
            raise ValueError(f"{self.key}: tag {self.tag!r} not in {TAGS}")
        if not self.source.strip():
            raise ValueError(f"{self.key}: empty source")
        if not self.label.strip() or not self.group.strip():
            raise ValueError(f"{self.key}: empty label or group")


# The diurnal demand multipliers. Twenty four hourly values on the Mars clock,
# mean exactly 1.0, trough 0.75 through the sleep block and peak 1.35 inside a
# three hour exercise block. Shaped on the sleep, nominal, exercise and recovery
# description in the habitat simulator's README, which gives the shape and not
# the numbers, so the numbers are ours.
SHAPE: tuple[float, ...] = (
    0.75, 0.75, 0.75, 0.75, 0.75, 0.75,   # sleep
    0.95,                                  # wake
    1.05, 1.10, 1.12, 1.12, 1.08,          # morning work
    0.98,                                  # midday
    1.05, 1.12, 1.12, 1.08,                # afternoon work
    1.22, 1.35, 1.31,                      # exercise block
    1.15, 1.00, 0.90, 0.80,                # recovery and wind down
)

# Physical, not assumed. Hydrogen lower heating value in kWh per kilogram.
H2_LHV_KWH_PER_KG = 33.3

ETA_FC = 0.55

CONSTANTS: tuple[Const, ...] = (
    # ---------------------------------------------------------------- settlement
    Const("POP", "Resident population", 1000, "residents", STATED,
          "The brief, phase 1 settlement", "The settlement"),
    Const("PER_CAP_KW", "Continuous electrical demand per resident", 0.45, "kW",
          ASSUMED,
          "Chosen so the design space the power partner declares actually "
          "closes. See the note below the table",
          "The settlement"),
    Const("SHAPE", "Diurnal demand multipliers, 24 hourly values", SHAPE,
          "multiplier, mean 1.0", ASSUMED,
          "Shaped on the habitat simulator's sleep, nominal, exercise and "
          "recovery description, which gives a shape and not a curve",
          "The settlement"),
    Const("SOL_HOURS", "Length of a sol", 24.6597, "hours", STATED,
          "Habitat simulator, 24 hours 39 minutes 35 seconds",
          "The settlement"),

    # ---------------------------------------------------- declared design space
    Const("FISSION_KW", "Installed fission surface power", 400.0, "kW", STATED,
          "Power partner, fission surface power units installed",
          "The declared design space"),
    Const("FISSION_MIN", "Reactor minimum stable output", 0.25,
          "fraction of rating", STATED,
          "Power partner, reactor minimum stable output. Carried but not "
          "exercised, because the model never turns the reactor down",
          "The declared design space"),
    Const("PV_RANGE", "Installed array peak rating", (400.0, 2400.0), "kWe peak",
          STATED, "Power partner, installed array peak rating",
          "The declared design space"),
    Const("BATT_RANGE", "Battery bank capacity", (800.0, 4800.0), "kWh", STATED,
          "Power partner, battery bank capacity", "The declared design space"),
    Const("SOC_FLOOR", "Battery state of charge floor", 0.40, "fraction", STATED,
          "Power partner, battery state of charge floor",
          "The declared design space"),
    Const("H2_RANGE", "Reactant storage", (220.0, 1300.0), "kg hydrogen", STATED,
          "Power partner, regenerative fuel cell reactant storage",
          "The declared design space"),
    Const("ELY_RANGE", "Electrolyser rating", (18.0, 340.0), "kW", STATED,
          "Power partner, electrolyser turndown band",
          "The declared design space"),
    Const("RIDE_SOLS", "Dust storm ride through target", 120, "sols", STATED,
          "Power partner, dust storm ride through target",
          "The declared design space"),

    # ------------------------------------------------------ physics and losses
    Const("PV_CLEAR", "Clear sky array capacity factor at solar noon", 0.43,
          "fraction of peak rating", ASSUMED,
          "Mars insolation and array temperature at beginning of life. No "
          "partner publishes this number",
          "Physics and losses"),
    Const("DAY_MEAN", "Mean of the daylight profile over a whole sol",
          0.318, "fraction", STATED,
          "Analytic. The mean of a half sine over a full cycle is 1/pi",
          "Physics and losses"),
    Const("ETA_BATT", "Battery charge efficiency", 0.90, "fraction", ASSUMED,
          "Round trip figure taken on the charge leg", "Physics and losses"),
    Const("ETA_ELY", "Electrolyser efficiency", 0.65, "fraction", ASSUMED,
          "Typical of a pressurised alkaline stack", "Physics and losses"),
    Const("ETA_FC", "Fuel cell efficiency", ETA_FC, "fraction", ASSUMED,
          "Typical of a regenerative fuel cell on the discharge leg",
          "Physics and losses"),
    Const("H2_LHV_KWH_PER_KG", "Hydrogen lower heating value",
          H2_LHV_KWH_PER_KG, "kWh per kg", STATED,
          "Physical constant", "Physics and losses"),
    Const("H2_KWH_PER_KG", "Electrical energy recovered per kg of hydrogen",
          round(H2_LHV_KWH_PER_KG * ETA_FC, 6), "kWh per kg", ASSUMED,
          "Lower heating value is physical, the fuel cell efficiency it is "
          "multiplied by is not", "Physics and losses"),
    Const("SOIL_RATE", "Array soiling rate", 0.002, "per sol", ASSUMED,
          "Dust deposition on the arrays through the event", "Physics and losses"),
    Const("SOIL_FLOOR", "Soiling floor", 0.70, "fraction of clean output",
          ASSUMED, "Where deposition and removal reach balance",
          "Physics and losses"),

    # ------------------------------------------------------- stand-ins for gaps
    Const("DERATE_ASSUMED", "Availability derate applied when sizing", 0.85,
          "fraction", ASSUMED,
          "Stands in for the derate function no partner owns. Outage, "
          "maintenance and deposition all land in this one number",
          "Stand-ins for what nobody owns"),
    Const("BATT_NIGHT_HOURS", "Night hours the battery is sized to carry", 12,
          "hours", ASSUMED,
          "Half a sol. Nobody declares how the battery is sized, only how "
          "large it may be", "Stand-ins for what nobody owns"),
    Const("ELY_SIZE_FRACTION",
          "Electrolyser rating as a fraction of clear sky array output", 0.30,
          "fraction", ASSUMED,
          "Nobody declares how the electrolyser is sized against the array, "
          "only the band it may run in", "Stand-ins for what nobody owns"),

    # ------------------------------------------------------------- storm shape
    Const("RAMP_SOLS", "Storm ramp in and ramp out", 5, "sols", ASSUMED,
          "How fast the optical depth builds and clears",
          "The dust state"),
    Const("STORM_HOLD_SOL", "Last sol at full storm depth", 115, "sol", ASSUMED,
          "The event holds to here and clears by the end of the ride through "
          "window", "The dust state"),
    Const("SEVERITY_DEFAULT", "Storm severity, peak insolation loss", 0.90,
          "fraction", ASSUMED,
          "The depth of a planet encircling event. Adjustable on the page",
          "The dust state"),
    Const("UPLIFT_DEFAULT", "Demand uplift under storm", 0.25, "fraction",
          ASSUMED,
          "The direction is physically robust: the habitat loses passive solar "
          "gain so heating load rises, and daylight has to be replaced "
          "electrically. Extravehicular activity stops, which pushes the other "
          "way. The magnitude is not established by anything, and the page "
          "lets you set it to zero",
          "The dust state"),
    Const("SHEDDABLE_DEFAULT", "Sheddable fraction of load", 0.30, "fraction",
          ASSUMED,
          "Which load can be switched off under stress is the split no partner "
          "declares. This is a placeholder for it",
          "The dust state"),

    # -------------------------------------------------------- the two designs
    Const("ENVELOPE_DEFAULT", "Envelope statistic", 95, "percentile", ASSUMED,
          "Which statistic of an hourly trace becomes the single exchanged "
          "bound is chosen by whoever forms it, and nobody has agreed to",
          "The two designs"),
    Const("PV_ITER_STEP", "Array increment per iteration", 0.08, "fraction",
          ASSUMED, "Step size for the coupled sizing loop", "The two designs"),
    Const("MAX_ITER", "Iteration limit", 8, "iterations", ASSUMED,
          "Cap on the coupled sizing loop", "The two designs"),
)


def by_key() -> dict[str, Const]:
    """Every constant, keyed. Raises on a duplicate key rather than shadowing."""
    out: dict[str, Const] = {}
    for c in CONSTANTS:
        if c.key in out:
            raise ValueError(f"duplicate constant key {c.key!r}")
        out[c.key] = c
    return out


def values() -> dict[str, Value]:
    """A flat key to value map, which is what the model in the page consumes."""
    return {c.key: (list(c.value) if isinstance(c.value, (tuple, list))
                    else c.value)
            for c in CONSTANTS}


def entries() -> list[dict]:
    """Every constant as a plain dict, tag and source included, in table order.

    The tag and the source are not optional and not decoration. A number on this
    page without them is a number a reader cannot check, which is the failure
    mode the whole repository is about.
    """
    return [
        {
            "key": c.key,
            "label": c.label,
            "value": list(c.value) if isinstance(c.value, (tuple, list)) else c.value,
            "unit": c.unit,
            "tag": c.tag,
            "source": c.source,
            "group": c.group,
        }
        for c in CONSTANTS
    ]


def groups() -> list[str]:
    """Group names in first-appearance order, so the table has a stable shape."""
    seen: list[str] = []
    for c in CONSTANTS:
        if c.group not in seen:
            seen.append(c.group)
    return seen


def payload() -> dict:
    """Everything the page needs: the values to run on, the entries to render."""
    return {
        "values": values(),
        "entries": entries(),
        "groups": groups(),
        "tags": list(TAGS),
    }


def counts() -> tuple[int, int]:
    """How many constants are stated and how many are assumed."""
    stated = sum(1 for c in CONSTANTS if c.tag == STATED)
    return stated, len(CONSTANTS) - stated


by_key()  # fail at import rather than at render if a key is duplicated
