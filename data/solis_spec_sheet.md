<!-- lint-role: specimen-document: synthetic partner declaration written in another organisation's voice. House style governs this repository's own prose, not a document it is quoting as evidence. -->
<!-- Synthetic partner declaration, format 1 of 4: a spec sheet.

Tabular, terse, units in the header row, no prose. The format that looks most
machine-readable and is therefore the one whose ambiguities are easiest to miss.

Written to be a good engineering document and a poor interface contract, which
is the common case. It settles units and ranges. It does not settle what clock
the horizon is measured on, what is inside the system boundary, how uncertainty
is carried, or who may change a value.

Values are grounded in the worldbuilding research and are synthetic. Keep the
filename: parse.py dispatches on it, and the partner name is half of what it
dispatches on. -->

# Solis Systems

## ARES interface specification

    Document        SOL-ARES-IS-004
    Revision        C
    Issued          2029-03-14
    Scope           ARES settlement, phase 1 build-out, 1,000 residents
    Planning horizon 10 years, annual resolution

## 0. Deliverables to the consortium

The parameters in section 1 are grouped for issue as four deliverables. The
consortium receives the deliverable, not the parameter list.

| Ref | Deliverable | Comprising |
|---|---|---|
| DEL-1 | capacity choices | OUT-01 through OUT-08 |
| DEL-2 | operating envelopes | OUT-09 through OUT-12 |
| DEL-3 | resource allocations | OUT-13, OUT-14 |
| DEL-4 | system trade-offs | OUT-15 |

## 1. Published outputs

| Ref | Parameter | Unit | Typical range |
|---|---|---|---|
| OUT-01 | Installed PV array peak rating | kWe, AM0, 28 C, beginning of life | 400 to 2,400 |
| OUT-02 | Fission surface power units installed | count x kWe per unit | 4 x 10 to 20 x 100 |
| OUT-03 | Battery bank capacity | kWh | 800 to 4,800 |
| OUT-04 | Regenerative fuel cell reactant storage | kg H2, kg O2 | 220 to 1,300 |
| OUT-05 | Electrolyser rated power | kW | 60 to 340 |
| OUT-06 | Water recovery loop throughput | kg/day | 3,600 to 4,900 |
| OUT-07 | Oxygen generation rated capacity | kg/day | 840 to 1,020 |
| OUT-08 | Crop growing area under cultivation | m2 | 0 to 27,000 |
| OUT-09 | Battery state of charge floor | percent | 40 |
| OUT-10 | Reactor minimum stable output | fraction of rated | 0.25 |
| OUT-11 | Electrolyser turndown band | kW min to kW max | 18 to 340 |
| OUT-12 | Dust storm ride-through target | sols at reduced insolation | 120 |
| OUT-13 | Power apportioned by consumer | kWe per consumer class | see 1.1 |
| OUT-14 | Water apportioned by consumer | kg/day per consumer class | see 1.1 |
| OUT-15 | Landed mass per guaranteed kWe | kg/kWe | 150 to 400 |

### 1.1 Consumer classes for OUT-13 and OUT-14

    habitat  life support  ISRU  agriculture  science  reserve

## 2. Required inputs

| Ref | Parameter | Unit | Supplied by |
|---|---|---|---|
| IN-01 | Specific mass by generation technology | kg/kWe | technology baseline |
| IN-02 | Specific energy by storage technology | Wh/kg | technology baseline |
| IN-03 | Round-trip efficiency by storage technology | percent | technology baseline |
| IN-04 | PV conversion efficiency at reference conditions | percent | technology baseline |
| IN-05 | Launch mass available per cargo window | kg per synodic period | mission programme |
| IN-06 | In-situ water availability at site | kg/sol extractable | site survey |
| IN-07 | Crew maintenance hours available | crew-hours/week | mission programme |
| IN-08 | Demand envelope, electrical | kWe | |
| IN-09 | Demand envelope, potable and hygiene water | kg/day | |
| IN-10 | Demand envelope, oxygen | kg/day | |

## 3. Notes

3.1 Ranges in section 1 are the design space, not a committed configuration. A
    committed configuration is issued as a separate case file.

3.2 OUT-01 through OUT-08 are selected once per planning cycle and held for the
    cycle.

3.3 OUT-09 through OUT-12 are limits on how the selected configuration may be
    operated.

3.4 Demand envelopes at IN-08 through IN-10 are taken as the binding case over
    the planning period. Solis does not size against a trajectory.

3.5 Queries on this specification to the Solis systems engineering lead.
