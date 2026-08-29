<!-- lint-role: specimen-document: synthetic partner declaration written in another organisation's voice. House style governs this repository's own prose, not a document it is quoting as evidence. -->
<!-- Synthetic partner declaration, format 2 of 4: a README paragraph.

Prose. States the interface in passing, in a section about something else, with
the units and the update cadence implied rather than given. The reader has to
infer, and parse.py must record that it inferred.

Written to be a good research README and a poor interface contract. It is
precise about method and casual about exchange, which is the normal failure of
an academic partner in a consortium.

Values are grounded in the worldbuilding research and are synthetic. -->

# Tharsis Habitat Institute

## habsim

`habsim` is the Institute's settlement demand simulator. It resolves resident
activity, equipment operation and environmental response at hourly steps across
a full Mars year, and it is the model the ARES consortium uses for anything that
depends on when a load actually occurs rather than on how much of it there is in
total.

### Running the model

A run needs a settlement configuration, a set of operating limits and a
population schedule. Configuration and limits come from Solis. The population
schedule is the roster of who is on site, what shift pattern they are on and
what activity they are doing in each hour, and it is maintained locally in
`inputs/pop/` because no upstream source publishes it in a usable form. The
current default is derived from the phase 1 crew manifest with shift patterns
assumed on the Phoenix precedent, and it has not been revised since the manifest
was superseded.

```
    habsim run --config solis_case_c --pop inputs/pop/phase1_default.yaml
```

Time is indexed in sols from arrival. A Mars year is 668 sols and a sol is 24
hours 39 minutes 35 seconds, so an hour in `habsim` is one twenty-fourth of a
sol and is not an SI hour. Everything the model emits is on this axis. Where a
partner needs a result on an Earth calendar the conversion is left to them,
since it depends on the epoch they are working from and we do not carry one.

### What the model consumes

Solis supplies the configuration as a set of installed capacities, and the
operating limits as bounds on how that configuration may be run. We take the
capacities as what is physically present and apply our own availability model on
top: outage, scheduled maintenance and dust deposition on arrays. That model
lives in `habsim/derate.py` and its parameters were fitted to the mission
reliability memo of 2028, which predates the current configuration.

### What the model produces

The primary output is a demand trace, one value per hour per commodity, for
electrical power, potable and hygiene water, oxygen, buffer gas makeup, thermal
heating and cooling, and carbon dioxide removal duty. Per-resident metabolic
rates follow the standard baseline values, with the diurnal shape taken from the
published sleep, nominal, exercise and recovery curve. Exercise dominates the
thermal profile, running about five times nominal heat output for the period it
occupies, which is why the peaks do not sit where a flat per-day rate would put
them.

The model also reports service shortfalls, meaning any hour in which a commodity
demand is not met, or in which an environmental variable leaves its acceptable
band. The bands currently applied are total pressure between 34.5 and 103 kPa,
carbon dioxide partial pressure below 3 mmHg, and oxygen partial pressure within
the standard range for the operating pressure. These were taken from the human
spaceflight standard directly, because no consortium partner has issued a set,
and they should be replaced when one exists.

Finally the model reports operational responses, which are the load shedding,
deferral and rescheduling actions it takes when a shortfall would otherwise
occur. These are how the model stays feasible and they should not be read as
recommendations.

### Known limitations

Equipment duty cycles are modelled where we have them and assumed where we do
not. Carbon dioxide removal is on a 144 minute half cycle with a documented
power penalty when the cycle is shortened, which the model represents. Crop
lighting is the largest single uncertainty: our figure is derived from photon
flux and lamp efficacy rather than measured, and at full cultivation it is
capable of dominating the electrical trace.

Results are deterministic. The model does not carry a distribution on any output
and a run represents one draw of the assumptions, not a range.

### Contact

Anything about the interface to `habsim`, or about the derate model, to the
Institute's simulation group.
