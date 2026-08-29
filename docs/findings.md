# Four missing objects on the boundary

What the consortium is missing is not agreement. It is four named objects that
sit on the boundary between the models and that no partner owns. Each is read
off the brief's own description of the partners, and nothing here is invented.

Each finding carries a stable identifier. The deck, the six-week plan, the
checker output and the tests all refer to a gap by its identifier, so there is
one name for one thing.

## Why these are the finding, and the vocabulary is not

The four partners use different words for adjacent ideas, and it is tempting to
call that the problem. It is not. Words can be reconciled in an afternoon by
anyone with authority to rule. What cannot be reconciled that way is an object
that has to exist for the models to exchange anything, that neither side has
agreed to produce, and that each therefore produces privately.

A private object is invisible in a status meeting and lethal in an integration.
Two teams each fill the same gap with a reasonable assumption, neither writes it
down, and the models disagree for a reason that appears nowhere in either
specification. The only way to keep two privately filled gaps consistent is to
run the models against each other continuously, which is to say tightly coupled.
That is the honest answer to the question the brief leaves open. Tight
bidirectional coupling has not been shown to be scientifically necessary because
it is not. It is what a consortium is forced into when the boundary has unowned
objects on it.

## GAP-1. The aggregation operator

- **Missing object.** The conversion from an hourly demand trajectory to a bound
that a multi-year capacity optimisation can plan against.

- **Evidence.** Solis consumes `demand envelopes`. Tharsis produces `time-series
demand`. These are not the same object. An envelope is a bound over a period, a
time series is a trajectory through it. Solis optimises "over multi-year
horizons", Tharsis simulates "hour by hour".

- **Why it is unowned.** Neither partner's produces clause names it. Solis
receives envelopes and does not say who forms them. Tharsis emits a series and
does not say what is done with it. The step between the two is real work,
requires a judgement (which percentile, over which window, under which
scenario), and is assigned to nobody.

- **What it costs today.** Somebody is forming that envelope, because Solis is
running. Whoever it is chose a percentile and a window without a mandate, and
that choice sets the installed capacity of the settlement.

- **Owner question.** Who forms the demand envelope from the hourly series, what
statistic is it, and over what window.

## GAP-2. The derate function

- **Missing object.** The conversion from a capacity decision to hour-by-hour
available capacity, after dust deposition, forced outage and maintenance.

- **Evidence.** Solis produces `capacity choices`. Tharsis consumes `available
capacity`. A choice is a decision variable, fixed at the point of planning.
Availability is a state that varies hour by hour and is always lower.

- **Why it is unowned.** The gap between installed and available is the entire
content of a Mars power system's risk, and no partner's interface names it.
Meridian defines the failure behaviour that would populate it, and Meridian
sends nothing to Tharsis.

- **What it costs today.** Tharsis is deciding, unilaterally, how much of Solis's
installed capacity is really there in a dust storm. Its shortfall results are
therefore a statement about Tharsis's derate assumption at least as much as
about the design Solis chose.

- **Owner question.** Who converts installed capacity into available capacity,
and does the derate come from Meridian's failure definitions or from a
placeholder.

## GAP-3. The service level threshold set

- **Missing object.** A routed, versioned set of thresholds that defines what
counts as a shortfall.

- **Evidence.** Meridian "defines component failures, compound events and
acceptable service levels" and produces "stress scenarios, reliability metrics
and evidence requirements". Tharsis produces `service shortfalls`. A shortfall
is measured against a threshold. Meridian's produces clause has no arrow to
Tharsis anywhere in the brief.

- **Why it is unowned.** The object exists and its owner is clear. What is missing
is the route. Meridian is described as producing and consuming nothing, which
means it is complied with rather than coupled to, and nothing in the description
carries its thresholds to the model that applies them.

- **What it costs today.** Tharsis is reporting shortfalls against a threshold it
was never sent. Meridian's stated objection is that "the current interface
cannot represent failure conditions or uncertainty well enough to support
credible mission-risk claims", which is what a body says when its criteria are
not reaching the thing being judged.

- **Owner question.** How do Meridian's acceptable service levels reach Tharsis,
in what form, and what happens to results computed against the previous set when
they change.

## GAP-4. Population schedules

- **Missing object.** A producer for the input that drives every demand profile.

- **Evidence.** Tharsis consumes `available capacity`, `operating constraints` and
`population schedules`. No partner in the consortium produces population
schedules.

- **Why it is unowned.** It is not a modelling output at all. It is a programme
assumption about who is on Mars and what they are doing, and it the mission owns it rather than any of the four
models, and that is precisely why it fell between them.

- **What it costs today.** It is the largest single driver of hourly demand, and
its provenance is unrecorded. Two runs of Tharsis are not comparable unless they
used the same schedule, and nothing in the consortium's structure guarantees
that they did.

- **Owner question.** Who owns the population schedule, at what cadence is it
revised, and is it versioned such that a demand result can be traced to one.

## What the checker must find

These four are the acceptance test for the artifact. The checker reads the four
partner declarations and computes findings. It is never told the answer, because
a checker that is told what to find demonstrates nothing.

| Gap | Rule class | What the rule detects |
|---|---|---|
| GAP-1 | resolution mismatch | a matched producer and consumer whose temporal resolutions differ with no stated conversion |
| GAP-2 | kind mismatch | a matched pair where one side is a decision variable and the other a realised state |
| GAP-3 | unrouted production | a published output with no consumer |
| GAP-4 | unmatched consumption | a required input with no producer |

Each rule is general. None of them names a partner, a variable or a gap. Applied
to a boundary where all four objects were owned, all four rules would return
nothing, which is the condition the recommendation is aiming at.

## What this does not claim

The brief does not say why Tharsis and Helix disagree about ownership of
interface variables, and this analysis does not invent a reason. It claims
something narrower and better evidenced: that a boundary carrying four unowned
objects will generate ownership disputes, and that the dispute is a symptom
rather than the disease. Only the consortium can say which specific variables
are contested, and its inability to say so in month 8 is itself a finding about
the interface rather than about the partners.
