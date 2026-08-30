# Five missing objects on the boundary

What the consortium is missing is not agreement. It is five named objects that
sit on the boundary between the models and that no partner owns. Each is read
off the brief's own description of the partners, and nothing here is invented.

Each finding carries a stable identifier. The deck, the six-week plan and the
tests all refer to a gap by its identifier, so there is one name for one thing.
The checker does not, because no rule in it names a gap.

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

There is a second argument for the same conclusion and it is the one that
decides the matter, because it does not depend on the statistics at all.

This is the credibility threshold, and it is not a principle invented for this
exercise. Li et al. (2019) put it as a line on a spectrum: below it a model is a
substitute, disconnected from the world and useful as a test bed, and above it a
model becomes a surrogate, close enough to the real system that a decision maker
can use it to act. The paper's own words: "there is a credibility threshold
beyond which models resemble reality well enough to be used by decision makers
as surrogate systems, useful for productively informing real world decisions."
The limiting case at the far end is a digital twin.

A settlement model exists so that somebody can commit to a design that has to
keep people alive. That purpose sets a floor on fidelity. Below some level of
resolution and coupling, a model is not a less useful version of the same tool.
It is inadmissible as evidence for the decision it was built to inform, because
no engineer would sign a habitat design on the strength of a tool whose own
authors would not trust it to design one. The question is not whether tight
coupling is scientifically interesting. It is where the line sits between a
model that can carry a life-safety design decision and one that cannot, and this
consortium is currently on the wrong side of it.

Read that way, the four partners are not producing four models that would be
nice to connect. They are producing three quarters of one instrument, and the
missing quarter is the coupling: engineering capacity from Solis, human life
support demand from Tharsis, and failure behaviour under stress from Meridian
have to propagate into each other, or the thing being asked of the model, would
this settlement survive a bad year, has no answer that anybody should act on.

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

## GAP-3. The service thresholds and the stress scenarios

- **Missing object.** Two things travelling the same absent route. A versioned
  set of thresholds defining what counts as a shortfall, and the stress
  scenarios themselves, meaning the environmental state that drives both models
  at once.

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

- **Owner question.** How do Meridian's acceptable service levels and stress
  scenarios reach Solis and Tharsis, in what form, and what happens to results
  computed against a previous set when it changes.

This is why the interface asserts independence. Both models need the dust state
over time. Solis needs it to derate generation, Tharsis needs it to drive
sheltering, activity and thermal load. Neither consumes it, and the partner who
produces it is the one with no route to either. The common cause exists, it has
an owner, and it reaches nobody, so each model treats its own half of a
correlated event as an independent input. Restoring that one route is the single
highest-value edge in the whole consortium.

## GAP-4. The population schedule

- **Missing object.** A producer for the input that drives every demand profile.

- **Evidence.** Tharsis consumes `available capacity`, `operating constraints` and
`population schedules`. No partner in the consortium produces population
schedules.

- **Why it is unowned.** It is not a modelling output at all. It is a programme
assumption about who is on Mars and what they are doing, and the mission owns it
rather than any of the four models, which is precisely why it fell between
them.

- **What it costs today.** It is the largest single driver of hourly demand, and
its provenance is unrecorded. Two runs of Tharsis are not comparable unless they
used the same schedule, and nothing in the consortium's structure guarantees
that they did.

- **Owner question.** Who owns the population schedule, at what cadence is it
revised, and is it versioned such that a demand result can be traced to one.

## GAP-5. The load taxonomy

- **Missing object.** A split of demand into loads that can be shed under
  stress and loads that cannot.
- **Evidence.** Tharsis produces `time-series demand`, which is one number per
  commodity per hour. Solis consumes `demand envelopes` and sizes against them.
  Neither document distinguishes a load that can be interrupted from one that
  cannot.
- **Why it is unowned.** In nominal operation the distinction does not matter,
  because everything is met. It only matters in the case the whole exercise is
  about.
- **What it costs today.** Life support is not a system running alongside the
  power system, it is a load on it. Oxygen generation, carbon dioxide removal,
  water recovery, thermal control and crop lighting are all kilowatts. Under a
  long dust event crop lighting can go dark and hygiene water can wait, while
  carbon dioxide removal cannot stop, and shortening its cycle costs more power
  rather than less. Sizing against an undifferentiated total hides the only
  distinction that decides whether the settlement survives.
- **Owner question.** Who classifies each load as non-deferrable, deferrable or
  droppable, on what authority, and how does that classification reach the
  partner sizing the generation.

## Six families of interface clause

The five gaps above are the worst class of defect, where an object that has to
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

Four of the five are the acceptance test for the artifact. GAP-5 is a
distinction missing inside a declared object rather than an object missing from
the boundary, so no rule reading these declarations can see it. The checker reads the four
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

## Reference

Li, F.G.N., Bataille, C., Pye, S., and O'Sullivan, A. (2019). Prospects for
energy economy modelling with big data: hype, eliminating blind spots, or
revolutionising the state of the art? *Applied Energy*, 239, pages 991 to 1002.
https://doi.org/10.1016/j.apenergy.2019.02.002

One reference, for one idea. The credibility threshold is the only concept here
taken from outside the brief, and it is named rather than paraphrased so that a
reader can check whether it has been used as the source intends.

## What this does not claim

The brief does not say why Tharsis and Helix disagree about ownership of
interface variables, and this analysis does not invent a reason. It claims
something narrower and better evidenced: that a boundary carrying four unowned
objects will generate ownership disputes, and that the dispute is a symptom
rather than the disease. Only the consortium can say which specific variables
are contested, and its inability to say so in month 8 is itself a finding about
the interface rather than about the partners.
