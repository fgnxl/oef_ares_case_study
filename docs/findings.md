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
specification.

The brief leaves open whether tight bidirectional coupling is scientifically
necessary. It is, and the reason is the stress case. Supply and demand on Mars
are not independent variables, they are driven by the same state. A dust storm
cuts generation, and it simultaneously drives crew indoors, changes activity
schedules, raises thermal load and alters life support duty cycles. Battery
state of charge at any hour depends on generation and demand at every hour
before it, and those two were correlated by a common cause throughout.

Exchange bounds once and that correlation is destroyed by construction. What
comes back is a worst-case supply and a worst-case demand as two separate
numbers, when the thing that ends a settlement is their coincidence. That is
what Meridian means by compound events, which makes its objection and the
coupling question the same question rather than two.

The contract is therefore the precondition for tight coupling and not an
alternative to it. Coupling two models tightly across three vocabularies, two
clocks and a derate nobody owns does not fail loudly. It produces fast,
confident, wrong answers, and it produces them every timestep.

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

## Six families of interface clause

The four gaps above are the worst class of defect, where an object that has to
exist is produced by nobody. There is a second and more common class, where the
object exists but a property the consumer needs is never declared. An interface
contract has clauses. This consortium has stated almost none of them.

| Family | Clauses | What the brief states |
|---|---|---|
| What it is | name, semantic kind, boundary convention | no interface variable is named anywhere, in any direction, for any partner |
| What it is measured in | unit, uncertainty representation | no units appear anywhere, and Meridian's objection is that uncertainty cannot be represented |
| When and where it applies | temporal resolution, spatial resolution, epoch | the brief names the scale mismatch and no partner names a conversion |
| Which run it belongs to | scenario identity, version | nothing, and GAP-4 means the largest demand driver is unversioned |
| How it arrives | cadence, latency, encoding | nothing, which is why an exchange can be late and in the wrong format without any contract having been broken |
| Who may change it | ownership, change protocol | nothing, which is the dispute between Tharsis and Helix |

Three of these deserve their evidence stated, because they are the ones a
consortium meeting would not surface.

- **Boundary convention.** Whether Tharsis's demand includes life support
parasitic load, or whether that sits inside Solis's own accounting, changes the
number by a large fraction. Both readings are reasonable. Neither is written
down.

- **Epoch.** Tharsis simulates hour by hour and Solis plans over multi-year
horizons. A Mars sol is 24 hours 39 minutes and 35 seconds. If one partner
indexes on sols and the other on Earth years, the two calendars drift apart by
about two and a half percent, systematically and permanently. Neither partner
states which clock it is on, and the error this produces is small enough per
step to survive review and large enough over a horizon to invalidate a capacity
decision.

- **Uncertainty representation.** Meridian judges whether a proposed system is
sufficiently resilient. If what reaches it is a point estimate, it cannot make
that judgement at all, regardless of how well the models are built. Its stated
objection is not a complaint about quality. It is a statement that the interface
lacks a clause its function requires.

## The four symptoms are one artifact

The brief lists four things that have gone wrong at month 8. They present as four
separate problems and they are four views of one missing artifact.

| Symptom in the brief | Family |
|---|---|
| an exchange is two months late and not in the planned format | how it arrives |
| Tharsis and Helix disagree about meaning and ownership | what it is, and who may change it |
| Meridian cannot represent failure conditions or uncertainty | what it is measured in |
| nobody has shown tight bidirectional coupling is necessary | when and where it applies |

None of the four is a failure of effort or goodwill, and treating them
separately produces four workstreams that each address a symptom. An exchange
cannot be late against a deadline that was never a contract term. Two partners
cannot agree on the meaning of a variable that has no declared owner. A risk
body cannot judge resilience from a value carrying no uncertainty. And a
consortium cannot couple two models tightly, which the stress case requires,
while the operators that bridge their scales are unowned.

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
