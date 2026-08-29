> Working notes, unedited. This is the option space considered before choosing,
> kept so the choices in `decisions.md` can be checked against what they were
> chosen over. It is not part of the recommendation and is not required reading.

# ARES case study: options exploration

Divergent exploration of what could be built for the NEST ARES candidate case study, written
before any convergent decision. Sourced from the brief alone
(`NEST_ARES_Candidate_Case_Study.pdf`). No other material consulted.

Everything below is an option, not a plan. The recommendation section at the end picks, but the
earlier sections deliberately keep incompatible ideas alive.

---

## 1. What the brief actually asks for

For a reader coming to this cold.

A philanthropic foundation has given $12M over three years to the ARES Consortium to build an
integrated energy-and-life-support modelling capability for a future Mars settlement (1,000
residents growing to 20,000). ARES does not build the settlement and owns no core model. Four
partners each govern, validate and release their own model:

| Partner | Type | Produces | Scale |
|---|---|---|---|
| Solis Systems | Commercial infrastructure modeller | Capacity choices, operating envelopes, resource allocations, trade-offs | Multi-year |
| Tharsis Habitat Institute | University simulation team | Time-series demand, service shortfalls, operational responses | Hourly |
| Meridian Risk Laboratory | Public mission-risk institute | Stress scenarios, reliability metrics, evidence requirements | Event and scenario |
| Helix Methods | AI and methods vendor | Schema translation, quality checks, orchestration, surrogates, interpretation tools | Cross-cutting, no domain authority |

It is month 8. The foundation review is in six weeks. Four symptoms are stated:

1. A Solis to Tharsis exchange is two months late and the earliest available output is not in the
   format Tharsis planned around.
2. Tharsis and Helix disagree about the meaning and ownership of several interface variables.
   Helix has already built tooling against a provisional interpretation.
3. Meridian believes the current interface cannot represent failure conditions or uncertainty
   well enough to support credible mission-risk claims.
4. The models run at different temporal and spatial scales, and nobody has shown that tight
   bidirectional coupling is scientifically necessary or even desirable.

The review question is narrow and explicit. Not a platform. **One repeatable end-to-end
demonstration**: evaluate how a proposed settlement configuration performs under a normal
operating case and one material stress event, with results traceable across the relevant models.
The consortium must be able to say what was exchanged, how inconsistencies and uncertainty were
handled, what was validated, and what the demonstration does and does not establish.

Deliverables: up to 8 board slides that also make the next six weeks executable (decisions,
ownership, dependencies, sequencing, review points), plus one small AI-enabled artifact that is
demoable in 3 to 5 minutes, plus an AI-use disclosure. Three hours of preparation. Sixty-minute
interview: 20 minutes pitch and demo, 30 minutes panel probing with at least one changed
constraint, 10 minutes reflection.

Assessed on: cross-scale reasoning, scientific integration, leadership across institutions,
applied AI judgment and build craft, prioritisation and communication.

Explicitly **not** assessed: Mars expertise, aerospace trivia, production-ready software,
literature review, exhaustive programme plans.

---

## 2. The specification asymmetry (read this before choosing an artifact)

Three of the four symptoms are specified well enough to build against. One is not.

| Symptom | What the brief gives us | Safe to build against? |
|---|---|---|
| Late exchange, wrong format | The failure mode is named (lateness plus format mismatch). A schema and adapter problem is fully implied. | Yes |
| Meridian: interface cannot carry failure or uncertainty | The requirement is stated in the partner's own words. Turning it into executable acceptance tests is operationalising a given, not inventing one. | Yes |
| Coupling necessity unproven | The gap itself is the stated fact. A protocol that tests necessity is a direct response. | Yes |
| Tharsis and Helix disagree on meaning and ownership of interface variables | **Which** variables, **why**, and **what each side believes** are all absent. | Mechanism only, never diagnosis |

This asymmetry drives the single sharpest hazard in the whole exercise, treated separately in
section 6. In short: any artifact whose demo output is a claim about what the disagreement *is*
has invented a finding and then detected it. Artifacts that provide a mechanism for surfacing
disagreements, demonstrated on openly labelled placeholder inputs, are fine. The difference is
whether the artifact's screen output reads as "here is the dispute" or "here is how the dispute
gets caught and closed".

One thing about symptom 2 **is** specified and is quietly the most useful sentence in the brief:
Helix built tooling against a provisional interpretation. That is a governance fact, not a
semantic one. It implies an answer (provisional interpretations need a named owner of record and
an expiry date) that requires knowing nothing about which variables are in dispute.

---

## 3. Deck: three fundamentally different arguments

These are not three orderings of the same slides. They are three different claims about what is
wrong and therefore three different asks of the board.

### Narrative A: "Coupling must be earned"

**The argument.** The programme is not failing at engineering, it is failing at a scientific
question nobody has answered: how tightly do these models actually need to be coupled? Symptoms 1
to 3 are downstream costs of trying to build an interface whose required fidelity has never been
established. The recommendation is to run an explicit coupling-necessity test, couple loosely
(scenario-driven, one-way with a bounded reconciliation step) everywhere the test says feedback
does not change the decision, and reserve tight bidirectional coupling for the few couplings that
earn it. The brief invites this directly ("You may decide that some models should not be tightly
coupled, if so, make the case").

**Puts first.** A scientific claim about system boundaries and feedback strength. The opening
slide is a coupling map with strength annotations and a stated test for each.

**Risks.** The board may hear "we are going to do less than we promised". Needs an immediate,
crisp answer to "how do you know feedback does not matter" or it becomes an assertion dressed as
a principle. It also does the least to address the political problem between Tharsis and Helix,
and a panel that cares about leadership without authority may find it thin.

**Best reader.** The scientifically literate board member and Meridian. This is the argument that
most directly demonstrates cross-scale reasoning, which sits first on the assessment list.

**Spine.** Diagnosis as one root cause, coupling map with earned strengths, the necessity test and
what it would show, the six-week demonstration this implies, partner work split, decisions and
dates, what it does not establish, risks.

### Narrative B: "Work backwards from the demonstration"

**The argument.** A programme that is not converging does not need a governance overhaul, it needs
one forcing artifact. Fix the end-to-end demonstration precisely, including the configuration, the
normal case, the one stress event and the exact result the board will see, then derive everything
else from it. The interface is only what the demonstration requires. Each partner's six-week
commitment is only what the demonstration requires. Anything not on that path is deferred to year
two, explicitly and in writing.

**Puts first.** A picture of the six-week deliverable itself, drawn as the board will see it, on
slide 1. Then the backward chain.

**Risks.** Reads as tactical and could look like ducking the deeper scientific and institutional
problems. A demonstration-first plan can degenerate into demoware, and a sharp panellist will ask
whether you have built a capability or a rehearsal. Needs an explicit answer for how the
demonstration generalises. Also risks under-serving the "leadership across institutions"
criterion unless the backward chain is expressed as partner commitments with owners.

**Best reader.** The board member holding the money and the milestone. It is the most obviously
responsive to the stated review question, and it makes prioritisation visible, which is an
assessed criterion.

### Narrative C: "The interface is the product"

**The argument.** ARES owns no model, so its deliverable cannot be a model. Its deliverable is a
governed exchange layer: a versioned, owned, machine-checkable interface contract carrying
semantics, units, boundary definitions, temporal and spatial resolution with aggregation rules,
uncertainty representation, failure-state encoding and validity domain. All four symptoms are the
same missing artifact seen from four sides. Solis's format mismatch is an adapter against a
contract that does not exist. The Tharsis and Helix dispute is an ownership field that was never
filled in. Meridian's objection is a requirement the contract must satisfy. The coupling question
is a decision the contract should record rather than assume.

**Puts first.** The diagnosis that four problems are one problem. Slide 1 is the four symptoms
collapsing into a single missing object.

**Risks.** Sounds like standards bureaucracy to a board that wants science. Six weeks of schema
work with no numbers at the end would be a fail against the review question, so this narrative
must carry the demonstration alongside it, not instead of it. Also risks appearing to impose
process on partners the lead does not manage.

**Best reader.** The technical panellist and the partners themselves. It is the argument that
most cleanly demonstrates scientific integration as an explicit competence, and it converts the
leadership problem into artifacts rather than meetings, which is the strongest available answer to
"momentum without direct control".

### Two framings considered and set aside

**"Risk requirements drive the architecture."** Start from Meridian: if the interface cannot carry
failure states and uncertainty, no coupling scheme produces a credible mission-risk claim, so
acceptable service levels sit at the top of the design tree and everything else is derived. Strong
and honest, but it privileges one partner visibly, which is awkward for a lead with no authority,
and it tilts the deck toward risk formalism at the cost of the energy-systems reasoning the panel
says it wants to see. Better used as the strongest single slide inside A or C than as the spine.

**"The missing skill is the integrator's."** A leadership-first deck about decision rights,
escalation paths and cadence. Almost certainly true, and almost certainly a losing deck, because
it under-serves three of the five assessment criteria and reads as programme management rather
than scientific integration.

### Note on hybridisation

A and C are compatible and arguably stronger together: the coupling decision determines what the
contract must carry, and the contract is where the decision is recorded. B is best treated as the
back half of either, since the brief demands the six weeks be executable regardless of the front
half. The real choice is which claim occupies slide 1, because that is what the board will
remember and what the panel will attack.

---

## 4. Artifact candidates

Twelve options. Each carries what it does, what it demonstrates about the builder, the 45-minute
build, the 3 to 5 minute demo, and the single biggest weakness under hostile questioning. The
brief names script, validator, interactive notebook, schema tool, decision aid, dashboard and
working mock-up as examples rather than a menu, so a few of these sit outside those categories.

### A1. Interface contract registry plus conformance validator
*Category: schema tool plus validator*

**Does.** A small machine-readable registry (YAML) of interface variables. Each entry carries a
single owner of record, a one-sentence semantic definition, units, the physical or system boundary
it is measured at, temporal resolution with an explicit aggregation rule, spatial scope, how
uncertainty is represented, how a failed or unavailable state is encoded (distinct from zero),
validity domain, version and consumer list. A CLI validator checks a candidate exchange payload
against the registry and emits typed violations: unit mismatch, resolution mismatch, missing
uncertainty field, failure state indistinguishable from zero, undeclared owner, consumer reading a
variable not in contract, value outside declared validity domain.

**Demonstrates.** That the builder thinks in contracts rather than converters, understands that
semantics and ownership are the root failure rather than file formats, and can ship working code.
Directly addresses symptoms 1, 2 and 3 at once.

**45-minute build.** Realistic. Roughly ten registry entries, a validator of 150 to 200 lines of
Python with no dependencies beyond PyYAML, and two synthetic payloads (one failing, one clean).

**Demo.** Show the registry entry for one variable and narrate the fields nobody usually fills in.
Run the validator against a synthetic Solis-shaped payload, get six typed failures, fix three,
re-run, show the remaining three escalate to a named human owner rather than auto-resolving.

**Biggest weakness.** You wrote both the contract and the test data, so the pass and fail are
staged. It also cannot tell you what the correct semantics is, only that two declared definitions
differ. The honest framing is that it is a gate, not an oracle.

**Invention risk.** Medium, and controllable. Safe if registry contents are labelled illustrative
and the demo never asserts what the real Tharsis and Helix dispute is.

### A2. Coupling-necessity screener
*Category: script plus decision aid*

**Does.** A deliberately crude two-model toy (a capacity and dispatch surrogate standing in for
Solis, a demand and response surrogate standing in for Tharsis) run in three modes: one-way, one
reconciliation pass, and iterated to convergence. Measures not the state variables but the
**decision**: does the configuration still pass the service-level test under the stress event, and
at what iteration does the answer stop flipping. Outputs one chart and a threshold rule.

**Demonstrates.** Cross-scale reasoning, and the discipline of making complexity earn its cost.
This is the assessed criterion listed first, addressed with executable evidence rather than a
diagram.

**45-minute build.** Feasible only if the toy stays crude. Fifty lines of physics, numpy, one
matplotlib figure. Serious scope-creep hazard, because the temptation to make the toy realistic is
strong and unrewarded.

**Demo.** One chart, one sentence. "Under this toy, feedback changes the decision only above
storage utilisation of X, so here is the test we ask each partner pair to run on their real
models."

**Biggest weakness.** The result is a property of a model the candidate wrote in half an hour, not
of the real ARES models. "You engineered the coupling to be weak" is the obvious attack. The only
defence is to present it as an executable specification of a test protocol rather than as a
finding, and to say so before being asked.

**Invention risk.** Low to medium. It fabricates a physics result, not an institutional one, and
is safe if framed as protocol.

### A3. End-to-end provenance ledger for one demonstration run
*Category: script plus working mock-up*

**Does.** Runs a synthetic chain (configuration to Solis-like output to adapter to Tharsis-like
run to Meridian-like stress case to result) and emits a machine-readable run record capturing every
exchange: source model, version, content hash, units, adapter or transform applied, assumptions
injected, uncertainty carried forward, and which board-facing claim each artifact supports. Renders
to a single-page HTML evidence trail with a mandatory "what this does not establish" panel that is
generated from the record, not typed by hand.

**Demonstrates.** Data provenance depth, and a literal reading of the review question, which asks
for results "traceable across the relevant models" and for an account of what was exchanged, how
inconsistencies were handled, what was validated and what the demonstration does not establish.
The artifact is a miniature of the deliverable the board asked for.

**45-minute build.** Yes, since the computations can be trivial. The value is in the record
structure and the rendering.

**Demo.** Show the rendered page, then click through from a headline number back to the exact
exchange and assumption that produced it. Then show the limits panel and point out that it is
derived, so it cannot be quietly softened.

**Biggest weakness.** It is careful plumbing around a fake computation. "You have traced nothing
real." Secondary risk of reading as documentation rather than capability.

**Invention risk.** Low.

### A4. AI-assisted adapter proposal with a semantic escalation gate
*Category: schema tool with an explicit AI boundary*

**Does.** Given a synthetic Solis output in the wrong shape and Tharsis's expected input schema, an
LLM proposes a field mapping. The tool then classifies each proposed mapping and enforces a rule:
mechanical transformations (unit conversion, renaming, dtype, ordering) are auto-applied and
logged, while anything involving a semantic judgement (aggregation rule across a resolution change,
boundary definition, treatment of missing values, sign convention) is **refused** and routed to the
variable's named owner of record with the model's reasoning attached as a suggestion only. Output
is a patch plus a human-review queue.

**Demonstrates.** Precisely the brief's request to show "where AI materially helps and where it
should remain constrained", expressed as enforced code rather than as a slide bullet. Probably the
single most on-brief statement of AI judgment available.

**45-minute build.** Feasible. The gate is rule-based and cheap. Cache the LLM response to a file
so the demo does not depend on a live API call.

**Demo.** Eight fields in, five auto-mapped with a diff, three escalated with reasons and owners.
Then the key line: the tool is designed to be unable to resolve a semantic question, because that
authority belongs to a partner.

**Biggest weakness.** The classification of what counts as semantic versus mechanical is the
candidate's own judgement and is unvalidated. A panellist can reasonably ask why unit conversion is
safe when a unit label can itself encode a boundary assumption, and the honest answer weakens the
clean split.

**Invention risk.** Medium to high if the escalated fields are narrated as "the disputed
variables". Keep them as generic classes of ambiguity.

### A5. Structured elicitation and disagreement diff
*Category: decision aid*

**Does.** For each interface variable, each partner independently answers seven fixed questions
(what does this measure, at what boundary, at what resolution and under what aggregation, what does
a missing value mean, who may change the definition, what does it mean when the subsystem has
failed, over what range is it valid). A small tool diffs independent answers, produces a
disagreement map, ranks each by severity (blocks the demonstration, moves the numbers, cosmetic)
and assigns a named decision owner and a deadline.

**Demonstrates.** Leadership without authority made mechanical. It converts a political argument
into a dated decision list, which is exactly the move an integrator with no line management has
available.

**45-minute build.** Yes, and it is the lowest-code option here. A form definition, a diff, a
ranking, a rendered table.

**Demo.** Good in structure. Weak in substance without invented answers, which is the problem.

**Biggest weakness and flag.** **This is the primary invention trap.** To show output at all you
must invent what Tharsis and Helix each believe, and the resulting screen looks like a diagnosis of
a dispute the brief never described. Two mitigations exist. Fill it with visibly generic placeholder
text so nobody mistakes it for a finding, or run it live on the panel during the demo by asking two
panellists to answer the seven questions for a variable of their choosing. The live version is
genuinely strong and removes the trap entirely, at the cost of demo risk.

**Invention risk.** High as built, near zero as a live exercise.

### A6. Stress-scenario compiler
*Category: script with a natural-language front end*

**Does.** Takes a plain-language failure description and compiles it into a structured, versioned
scenario object every model can consume: perturbation vectors keyed to contract variables, time
window, affected components, service-level metrics to record, required uncertainty treatment, and
the compound-event structure if more than one perturbation coincides. The LLM does the language to
structure parse, and the schema constrains what it is allowed to emit.

**Demonstrates.** Joins Meridian's stated requirement to the interface contract, and uses AI where
language to structure genuinely is the right tool rather than as decoration. Makes the "one material
stress event" in the review question a first-class, versioned object rather than a spreadsheet row.

**45-minute build.** Feasible with a constrained output schema and a cached response.

**Demo.** Type one sentence, get a scenario file, feed it into the toy chain, see the service-level
metric move.

**Biggest weakness.** Expressiveness is capped at what the schema anticipated, and compound events
are precisely where the hard part lives. A 45-minute tool will handle a coincidence of two
perturbations and nothing subtler. There is also a drift hazard toward Mars-specific failure
detail, which scores nothing.

**Invention risk.** Low. Scenarios are synthetic by definition and are declared as such.

### A7. Board configuration explorer dashboard
*Category: dashboard*

**Does.** A small interactive page where the board picks a configuration (generation mix, storage
hours, habitat count) and sees normal versus stress performance with uncertainty bands.

**Demonstrates.** Communication instinct and board empathy.

**45-minute build.** Tight but possible with pre-computed synthetic results.

**Demo.** Visually the most impressive option in the set.

**Biggest weakness.** Severe and structural. It looks like a result. Invented Mars energy numbers
presented interactively invite exactly the Mars-expertise conversation the brief says is not being
tested, and it implies a capability ARES does not have and will not have in six weeks. It is the
clearest demoware risk on the list.

**Invention risk.** High, of a different kind. It fabricates results rather than findings about the
consortium.

### A8. Failure and uncertainty representation conformance suite
*Category: validator, narrower than A1*

**Does.** A focused executable test suite asking one question of a candidate exchange format: can it
express a censored value, a failed sensor distinguished from a genuine zero, a probabilistic band,
an ensemble member identity, a degraded-but-operating state, and a service-level breach with its
duration. Each becomes a test with a pass or fail.

**Demonstrates.** The integrator's core move, which is turning a partner's objection into a testable
acceptance criterion the partner can sign off. It also lands on Meridian's concern, which is the one
partner grievance the brief states in enough detail to build against without inventing anything.

**45-minute build.** Yes, and quickly. It is a subset of A1 and could be built as A1's second half.

**Demo.** Run the suite against the current provisional interface (synthetic), fail four of six,
then show the contract change that would make them pass and the cost of that change.

**Biggest weakness.** The test list is the candidate's opinion about what Meridian needs, and
Meridian was not consulted. Also narrow enough that on its own it may look like a fragment.

**Invention risk.** Low. It operationalises a stated grievance rather than inventing one.

### A9. Six-week critical-path and dependency simulator
*Category: decision aid, programme side*

**Does.** Encodes the six-week plan as tasks with owners, dependencies and duration distributions,
including uncertainty on the already-late Solis exchange, and runs a small Monte Carlo to show which
dependency actually threatens the review date and where slack sits. Output is the one or two
decisions that must close in week one.

**Demonstrates.** That the plan on the delivery slide is computed rather than decorative, and that
the candidate can identify the true critical path under uncertainty.

**45-minute build.** Yes.

**Biggest weakness.** It drifts toward the exhaustive programme plan the brief explicitly excludes,
and every duration in it is invented. Risk of being read as project-management theatre.

**Invention risk.** Medium, and of the least defensible sort, since it fabricates partner capacity.

### A10. Decision-relevance filter for interface variables
*Category: decision aid, pairs with A1 and A2*

**Does.** Screens candidate interface variables by whether they change the board's decision, using a
coarse sensitivity pass on the toy chain, then proposes that only the top tier receives a hard,
owned contract in six weeks while the rest stay provisional with an expiry date.

**Demonstrates.** Prioritisation made defensible rather than asserted, and gives a principled answer
to "why did you only fix five variables". It also produces the governance answer to the Helix
provisional-tooling problem without needing to know which variables are disputed.

**45-minute build.** Only as an add-on to A2, since it needs the toy chain. Not standalone.

**Biggest weakness.** Circular. The sensitivity screen depends on a toy whose structure already
encodes assumptions about which variables matter.

**Invention risk.** Low to medium, same class as A2.

### A11. Partner release note and admission gate
*Category: schema tool, outside the named list*

**Does.** A short standard release note that every partner attaches to any output entering the
demonstration chain: model version, validity domain, known failure modes, what the output must not
be used for, uncertainty method, named contact. A checker refuses admission to the chain without a
complete note.

**Demonstrates.** Governance made mechanical, and respect for the structural constraint that
partners release rather than surrender their models. It gives ARES leverage over quality without
demanding access to anyone's IP, which is a genuinely non-obvious answer to the leadership criterion.

**45-minute build.** Yes, and very cheaply.

**Biggest weakness.** Reads as paperwork, and a hostile panellist will ask what stops a partner
writing "valid everywhere" in the validity field. The honest answer is nothing, which weakens it
unless paired with A8's tests.

**Invention risk.** Low.

### A12. Surrogate with a refusal boundary
*Category: outside the named list*

**Does.** Fits a fast surrogate to the toy habitat model, then ships a companion check that reports
where the surrogate is not trustworthy (outside training domain, near a failure threshold, in a
regime with too few samples) and **refuses to return a value** there rather than extrapolating.

**Demonstrates.** AI where it helps and constrained where it does not, in the specific form most
relevant to a modelling consortium, since Helix is explicitly developing surrogate methods.
Refusal-by-design is a stronger signal than an accuracy metric.

**45-minute build.** Tight. Achievable with scikit-learn on toy data if the toy already exists,
which makes it an add-on to A2 rather than a standalone.

**Biggest weakness.** It is a surrogate of a fake model, so it is doubly synthetic, and the accuracy
numbers mean nothing. Its only real content is the refusal logic.

**Invention risk.** Low.

---

## 5. Assessment against the stated criteria

Scored against the brief's own "What we will focus on" list. High, medium or low is the signal each
artifact sends on that criterion, not a quality judgement.

| Artifact | Cross-scale reasoning | Scientific integration | Leadership across institutions | AI judgment and build craft | Prioritisation and communication |
|---|---|---|---|---|---|
| A1 Contract registry plus validator | Medium | High | High | Medium | Medium |
| A2 Coupling-necessity screener | High | High | Low | Medium | Medium |
| A3 Provenance ledger | Medium | High | Medium | Medium | High |
| A4 AI adapter with escalation gate | Low | Medium | High | High | Medium |
| A5 Elicitation diff | Low | Medium | High | Low | Medium |
| A6 Scenario compiler | Medium | Medium | Low | High | Medium |
| A7 Dashboard | Low | Low | Low | Medium | High |
| A8 Failure and uncertainty suite | Medium | High | Medium | Low | Medium |
| A9 Critical-path simulator | Low | Low | Medium | Low | Medium |
| A10 Decision-relevance filter | High | Medium | Medium | Low | High |
| A11 Release note gate | Low | Medium | High | Low | Low |
| A12 Surrogate with refusal | Medium | Medium | Low | High | Low |

Reading across the rows, no single artifact covers all five. The clusters that do cover well are
A1 plus A8 plus A3 (integration, provenance and governance, weak on AI signal) and A4 plus A6
(AI judgment, weak on scientific integration). A2 plus A10 is the strongest scientific pairing and
the weakest institutional one.

Since the deck carries the leadership and prioritisation argument on its own, the artifact's job is
to cover what a slide cannot prove. That favours something executable and checkable over something
persuasive.

---

## 6. The invention trap, stated plainly

The brief says partners disagree about the meaning and ownership of several interface variables. It
never says which variables, what either side believes, or why. Anything that presents a specific
disagreement as an output has invented a finding and then detected it. The panel wrote the brief and
will know immediately.

**Flagged options, in order of exposure:**

| Option | Exposure | Why | Mitigation |
|---|---|---|---|
| A5 Elicitation diff | **High** | Its entire output is a claim about who believes what. Cannot be demonstrated without inventing partner positions. | Run it live on the panel, or fill it with visibly generic placeholders and narrate it as a mechanism only. |
| A4 AI adapter gate | Medium to high | The escalated fields will be read as the disputed variables unless framed as generic ambiguity classes. | Name escalations by class (aggregation rule, boundary, missing-value convention), never by partner position. |
| A1 Contract registry | Medium | The registry entries could be read as authoritative statements of contested semantics. | Label the registry illustrative, and demo the validator's behaviour rather than the registry's content. |
| A7 Dashboard | High, different class | Fabricates results rather than institutional findings, which is arguably worse in front of a board. | None that preserves the artifact. |
| A9 Critical-path simulator | Medium | Fabricates partner capacity and durations. | Present durations as placeholders and the structure as the point. |
| A2, A6, A8, A11, A12 | Low | Each builds against something the brief states explicitly, or against openly synthetic inputs whose synthetic status is the point. | Standard disclosure. |

**The general rule.** An artifact may demonstrate a mechanism on synthetic inputs. It may not
present the output of that mechanism as knowledge about ARES. The test to apply before the demo:
if the panel asked "where did that come from", is the answer "I made it up to show the tool works"
comfortable to say out loud? If yes, safe. If it would be embarrassing, the artifact is diagnosing
something it cannot know.

There is a second and more useful move available. The absence of detail about the dispute is itself
a fact worth naming to the board. An integrator who says "I do not know which variables are in
dispute, and the fact that ARES cannot answer that question in month 8 is the finding" is making a
stronger and more honest point than one who invents an answer. That line belongs in the deck.

---

## 7. Traps and drift costs

Everything here is effort with no score attached, drawn from the brief's own exclusion list.

**Mars expertise and aerospace trivia.** Any slide that discusses dust storm statistics, regolith
properties, ISRU chemistry, radiation shielding or launch windows. The brief says no Mars knowledge
is required, so displaying it reads as a misread of the exercise. Keep the settlement generic:
generation, storage, habitat load, life support, service levels.

**Production-ready software.** Packaging, CI, test coverage targets, type stubs, a CLI framework,
Docker. Every minute spent here is invisible to the assessment and consumes the 45-minute artifact
budget. Ship a script that runs, with one clean entry point.

**Literature review.** Citations to real coupled-model integration papers or Mars mission
literature. Not assessed. A single reference to a named practice is fine, a bibliography is a cost.

**Exhaustive programme plan.** A full Gantt across three years, a RACI matrix for twenty
workstreams, a risk register with thirty rows. The brief asks for the next six weeks to be
executable, which means decisions, owners, dependencies, sequencing and review points, not a plan
document. A9 sits close to this line.

**Over-modelling the physics.** Building a real dispatch optimiser or a genuine habitat energy
balance. This is the most seductive trap for an energy-systems modeller and will silently consume
the whole three hours. The toy in A2 must stay a toy, and its crudeness should be stated proudly
rather than apologised for.

**Building the coupler.** Attempting an actual orchestration framework or a real bidirectional
solver. Six weeks of consortium time, not 45 minutes of preparation.

**Solving the dispute.** Arriving with a proposed canonical definition for the contested variables.
Beyond the invention problem, it also usurps partner authority, which is precisely the failure mode
a lead without line management must avoid. The deck should propose a process for closing the
dispute and a deadline, not a verdict.

**Demoware polish.** Time spent on animation, theming or a landing page. The brief says explicitly
that it rewards prioritisation and judgment rather than production polish, and an intentionally
incomplete answer with explicit trade-offs beats an overbuilt one.

One trap worth naming that is not on the exclusion list: **answering all three artifact purposes.**
The brief says the artifact may support scientific integration, programme coordination or
communication of results, and that it is not expected to address all three. Attempting all three
guarantees a shallow build in 45 minutes.

---

## 8. Recommendation

### Primary: A1 plus A8, with A3 as the stretch

Build the interface contract registry with a conformance validator, where the conformance tests
include the failure-state and uncertainty representation checks from A8. If time remains, wrap a
single synthetic run in the A3 provenance record so the demo ends on a rendered evidence trail with
a derived limits panel.

Why this combination. It builds only against symptoms the brief specifies. It gives the validator a
reason to exist beyond format checking, since the uncertainty and failure tests come from a stated
partner grievance rather than from invention. It is a mechanism rather than a diagnosis, so it sits
on the safe side of the invention line. It scores high on scientific integration and leadership, the
two criteria a deck alone struggles to prove. And it is the artifact most likely to still work at
minute 44, because every component degrades gracefully: a registry with fewer variables and three
tests instead of six is still a complete demonstration.

Build order, with drop points:

1. Registry schema and five variable entries (12 minutes). Drop point: five is enough.
2. Validator with four typed checks including one failure-state check (18 minutes). Drop point: this
   alone is a shippable artifact.
3. Two synthetic payloads, one failing and one clean (7 minutes).
4. Two more conformance tests from the A8 list (8 minutes). Drop first if behind.
5. Provenance record and rendered page (stretch only). Drop without hesitation.

### Alternative: A4 plus A6

If the deck's argument is B or C and needs a stronger AI signal, build the adapter proposal with the
semantic escalation gate, and feed it from the scenario compiler. This pairing makes the clearest
possible statement about where AI helps and where it must be constrained, which is one of the two
things the brief asks the artifact to prove. It is riskier, because it depends on an LLM call that
must be cached before the interview, and because its escalation taxonomy is defensible only as far
as the candidate can argue it live.

### Deck pairing

Narrative C ("the interface is the product") pairs most naturally with the primary artifact, since
the artifact is literally the argument in executable form. Narrative A ("coupling must be earned")
is the stronger scientific claim and the better answer to the first assessment criterion, but it
would want A2 as its artifact, which carries the higher fabrication and scope-creep risk.

The hybrid worth considering: open with A's claim that coupling strength must be earned by evidence,
land the middle on C's diagnosis that the four symptoms are one missing artifact, and close on B's
backward chain from the six-week demonstration. The artifact then proves the middle, and the opening
and closing are argued rather than demonstrated, which is the correct division of labour between a
deck and a 45-minute build.

### What to say about limits, in every version

The demonstration establishes that information can move between the models with declared semantics,
that inconsistencies are caught rather than absorbed, and that one stress case can be traced end to
end. It does not establish that the settlement configuration is good, that the coupled result is
accurate, that the stress case is the right stress case, or that the models are individually
validated. Saying this before the panel asks is worth more than any additional feature.
