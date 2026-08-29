# ARES Consortium Partner Profiles

Evidence-marked profiles of the four fictional partner organisations in the ARES consortium.

## Purpose and status of this document

This file exists to be the upstream source for two later artefacts: a set of synthetic interface declarations written in each partner's own voice and format, and a register of assumptions. Anything invented here would be inherited downstream as if it were fact. So every statement below carries an evidence mark.

Everything in this document derives from exactly one source: the NEST candidate case study brief for the Energy Systems and AI Research Lead role, hereafter "the brief". No other document, dataset or outside knowledge has been used. The four organisations are fictional. Any resemblance to real bodies is not evidence and has not been drawn on.

## How to read the marks

Every statement is one of exactly three kinds.

- **STATED** the brief says this. The quote is given.
- **INFERRED** it follows from what the brief says. The reasoning is given in one line.
- **UNKNOWN** the brief does not say, and it matters.

An UNKNOWN is a finding, not a gap in the work. The most useful thing this document does is show how little the brief actually specifies about each partner. Roughly speaking the brief gives each partner one or two sentences, and everything an interface designer would want to know sits outside those sentences.

## Two standing cautions

The first caution is about the disagreement. The brief states that two partners disagree about interface variables. It never says which variables, or why. The disagreement is recorded here as UNKNOWN in content, and nothing downstream infers it.

The second caution is about the Solis text. In the source PDF, the Solis Systems entry begins mid-clause. The extracted line reads "strategic infrastructure optimization." with no preceding subject or verb on that line and no capital letter. The words that governed that phrase are not recoverable from the source. This is noted where it applies rather than patched over.

## Programme facts that frame all four partners

These are context, not partner attributes, and every partner profile below sits inside them.

- STATED. The grant is "a $12 million, three-year research grant to the ARES Consortium".
- STATED. "ARES is not building the settlement." Its job is "to create the integrated energy-and-life-support modelling capability".
- STATED. The colony "would begin with about 1,000 residents and could eventually support 20,000".
- STATED. "Each partner governs, validates and releases its own model."
- STATED. Partners "have different incentives, vocabularies, scales, IP constraints and quality processes".
- STATED. "ARES owns no core model."
- STATED. The programme is at "Month 8" and "The foundation's major milestone review is in six weeks".
- STATED. "The models operate at different temporal and spatial scales, and nobody has yet shown that a tight, bidirectional coupling is scientifically necessary."
- UNKNOWN. How the $12 million is split across the four partners. Budget share usually drives who absorbs integration cost, and the brief is silent.
- UNKNOWN. Whether the partners hold subcontracts with ARES, direct grants from the foundation, or some other instrument. This determines what use exists over any of them.
- UNKNOWN. Headcount, seniority, location and timezone for every partner.

---

# Solis Systems

## What kind of organisation it is

- STATED. Solis Systems is a "commercial infrastructure modeller".
- STATED. Its work is described as "strategic infrastructure optimization". Note the caution above. In the source text this phrase appears without the verb that governs it.
- INFERRED. A commercial firm carries client obligations and margin pressure, so its release pace is likely governed by contract milestones rather than by publication or peer review.
- INFERRED. "Optimization" as the named activity implies a solver-centred workflow, which typically means long batch runs and a scenario turnaround measured in days rather than minutes.
- INFERRED. Of the four, Solis is the partner whose commercial position is most exposed by releasing internals, because a capacity optimiser's formulation and cost assumptions are the sellable asset.
- UNKNOWN. Whether Solis has other paying clients whose work competes with ARES for the same modelling team.
- UNKNOWN. Whether Solis is a subcontractor, a grant recipient, or a partner with its own IP carve-out. The brief says only that IP constraints differ across partners, without saying whose bind hardest.
- UNKNOWN. Company size, whether the model is one product or many, and whether the ARES work uses a standard product or a bespoke build.

## What it models, and at what resolution

- STATED. It "Chooses candidate generation, storage and life-support capacity over multi-year horizons."
- STATED temporal resolution boundary. "multi-year horizons" gives the horizon.
- UNKNOWN temporal resolution. A multi-year horizon says nothing about the time step inside it. Annual, seasonal, representative-day and full-hourly optimisers all describe themselves this way, and they produce incompatible outputs.
- UNKNOWN spatial resolution. The brief never says whether Solis models the colony as one node, as a small set of zones, or as a sited network. This is the single most consequential missing fact for any coupling to Tharsis.
- INFERRED. Because it "Chooses" capacity, Solis is a decision model rather than a descriptive one, so its outputs are the results of an objective function rather than measurements.
- UNKNOWN. What that objective function is. Cost, mass, reliability, launch payload and area are all plausible and the brief names none.
- UNKNOWN. Whether Solis is deterministic or stochastic, and whether it produces one plan or a set.

## What it consumes and produces

Solis is one of only two partners given both a consumes clause and a produces clause.

- STATED, consumes. "It consumes technology assumptions, resource limits and demand envelopes".
- STATED, produces. "it produces capacity choices, operating envelopes, resource allocations and system-level trade-offs".
- INFERRED. Because it consumes "demand envelopes" and Tharsis produces "time-series demand", the demand it takes in is a bounded or aggregated form rather than an hourly trace.
- UNKNOWN. What a "demand envelope" contains. Peak and minimum, a percentile band, a set of representative profiles and an annual total are all consistent with the word.
- UNKNOWN. What an "operating envelope" contains, and whether it is the same object as the "operating constraints" Tharsis consumes. See the cross-partner section.
- UNKNOWN. Units, file formats, schema, delivery mechanism and release cadence for every one of those items.
- UNKNOWN. Where "technology assumptions" and "resource limits" come from. No partner is stated to produce them, so they enter the consortium from outside the four, or from ARES, or from the foundation, and the brief does not say which.

## Likely internal vocabulary

This section is inference throughout. The brief supplies no sample of any partner's own writing, so nothing here is evidence about how Solis actually speaks.

- STATED terms the brief itself puts in Solis's frame: "capacity", "storage", "generation", "life-support capacity", "operating envelopes", "resource allocations", "system-level trade-offs", "technology assumptions", "resource limits", "demand envelopes", "horizons".
- INFERRED. An optimisation shop usually speaks in objective, constraint, decision variable, feasible, committing, shadow price, scenario, case and run.
- INFERRED. A commercial infrastructure firm usually frames output as a recommendation or a portfolio rather than as a finding or a result.
- UNKNOWN. Whether Solis names things by asset, by technology, by node or by contract. Any interface declaration written in its voice has to pick one, and that pick is an assumption.

## What it needs and what needs it

- STATED, it is needed by Tharsis. "A critical exchange from Solis to Tharsis is two months late." The brief calls this exchange "critical".
- STATED, the format is wrong. "the earliest available output is not in the format Tharsis planned around".
- INFERRED. Solis sits upstream in the intended flow, because Tharsis consumes "available capacity" and Solis produces "capacity choices".
- UNKNOWN. What that critical exchange actually contains. The brief names neither the payload nor the format on either side.
- UNKNOWN. Why it is two months late. Capacity, dependency, contractual dispute and technical blocker are all consistent with the text.
- UNKNOWN. Whether Solis consumes anything from any of the other three. Its consumes clause names three items, and no partner in the brief is stated to produce any of them.
- UNKNOWN. Whether Solis has any stated relationship with Meridian or Helix at all. The brief mentions none.

## What would make it hard, and what would make it cooperative

- INFERRED, hard. It is already the late partner on the one exchange the brief calls critical, so it starts the six weeks carrying the schedule risk.
- INFERRED, hard. As a commercial modeller its formulation is likely the asset it sells, so requests to expose internals or to be audited run against its interest.
- INFERRED, hard. An optimiser that has to be re-run to answer a question is expensive to put inside a tight loop.
- INFERRED, cooperative. It already produces "system-level trade-offs", which is close to what the review asks for, so a demonstration built around its existing outputs asks little new of it.
- INFERRED, cooperative. Commercial partners respond to a clearly specified deliverable with a date, because that is the form their normal work takes.
- UNKNOWN. Whether the format mismatch is cheap or expensive for Solis to fix. Nothing in the brief indicates effort.

---

# Tharsis Habitat Institute

## What kind of organisation it is

- STATED. Tharsis Habitat Institute is a "university simulation team".
- INFERRED. A university team's incentives run to publication and to methodological defensibility, so it is likely to resist changes that weaken the scientific standing of its model.
- INFERRED. Academic pace is set by terms, students and grant cycles, so its capacity is likely lumpy and its staff turnover higher than a commercial partner's.
- INFERRED. Of the four, it is the one most likely to be able to share model detail, since IP pressure on a university team is usually lower than on a vendor or a commercial firm. The brief does not confirm this.
- UNKNOWN. Which university, which department, and whether the team is one principal investigator with students or a standing research group.
- UNKNOWN. Whether the model is a research code or a maintained product, which decides whether anyone else can run it.

## What it models, and at what resolution

- STATED. It "Simulates residents, habitat activity, equipment operation and local demand hour by hour."
- STATED temporal resolution. "hour by hour". This is the only explicit time step in the brief for any partner.
- INFERRED spatial scope. The word "local" in "local demand" and the word "habitat" imply a within-settlement spatial frame rather than a colony-wide aggregate.
- UNKNOWN spatial resolution. Whether "habitat" means one module, a cluster, or the whole settlement is never said.
- UNKNOWN. Simulation length. Hourly for a week, a year or a decade are very different objects and the brief gives no run duration.
- UNKNOWN. Whether it is agent-based, physics-based, statistical or a mix. "Simulates residents" is compatible with all of them.
- UNKNOWN. Whether it is stochastic, and if so how many replicates constitute a result.
- UNKNOWN. Which population size it is built for. The brief gives the colony as 1,000 rising to 20,000 but never says what Tharsis assumes.

## What it consumes and produces

Tharsis is the other of the two partners given both a consumes clause and a produces clause.

- STATED, consumes. "It consumes available capacity, operating constraints and population schedules".
- STATED, produces. "it produces time-series demand, service shortfalls and operational responses".
- INFERRED. It is both downstream and upstream of Solis in principle, because it consumes capacity and produces the demand that a capacity optimiser needs. That circularity is exactly the coupling question the brief raises.
- UNKNOWN. What "population schedules" are and who supplies them. No partner is stated to produce them.
- UNKNOWN. What a "service shortfall" is measured in. Energy not served, hours of degraded service, a count of events and a per-resident metric are all consistent.
- UNKNOWN. What an "operational response" is as a data object. It could be a control action, a dispatch decision, a behavioural adjustment or a log of what the simulation did.
- UNKNOWN. Units, schema, formats and cadence, as with every partner.

## Likely internal vocabulary

Inference throughout. No sample of Tharsis's own writing exists in the brief.

- STATED terms the brief puts in Tharsis's frame: "residents", "habitat activity", "equipment operation", "local demand", "hour by hour", "available capacity", "operating constraints", "population schedules", "time-series demand", "service shortfalls", "operational responses".
- INFERRED. A simulation team usually speaks in run, replicate, seed, time step, warm-up, calibration, validation, sensitivity and ensemble.
- INFERRED. A university team is likely to describe outputs as results with uncertainty attached rather than as answers.
- INFERRED. It is the partner most likely to name a variable after the physical thing it represents rather than after its role in an interface.
- UNKNOWN. Whether it uses SI units throughout, and what its timestamp convention is. Both matter for a synthetic interface declaration and neither is stated.

## What it needs and what needs it

- STATED, it needs Solis. The late exchange runs "from Solis to Tharsis" and Tharsis "planned around" a format it did not get.
- STATED, it has an interface with Helix. "Tharsis and Helix disagree about the meaning and ownership of several interface variables."
- INFERRED. Solis needs Tharsis, because demand is what a capacity chooser must be given and Tharsis is the only stated producer of demand.
- INFERRED. Meridian probably needs Tharsis output to judge service levels, since Tharsis produces "service shortfalls" and Meridian defines "acceptable service levels". The brief never states an exchange between them.
- UNKNOWN. Whether any Tharsis to Meridian exchange exists in the programme plan.
- UNKNOWN. What Tharsis was promised by Solis, in writing, and by when.

## What would make it hard, and what would make it cooperative

- INFERRED, hard. It has already built around a format that did not arrive, so it has sunk work and a legitimate grievance.
- INFERRED, hard. It is one of the two parties to the interface disagreement, which makes any interface decision political rather than purely technical.
- INFERRED, hard. Academic quality processes are slow to sign off changes, and the brief confirms quality processes differ across partners.
- INFERRED, cooperative. Hourly simulation output is the richest data in the consortium, so a demonstration that shows it serves its interest.
- INFERRED, cooperative. A university team responds well to being asked to define and defend a method, since that is publishable work.
- UNKNOWN. Whether the sunk work on the planned format is recoverable.

---

# Meridian Risk Laboratory

## What kind of organisation it is

- STATED. Meridian Risk Laboratory is a "public mission-risk institute".
- INFERRED. A public institute answers to a mandate rather than to a client, so its incentive is to protect the credibility of the risk claim rather than to hit a delivery date.
- INFERRED. As the body that sets "acceptable service levels" it holds an assurance role, which usually carries independence requirements and a slower, documented sign-off.
- INFERRED. Public status makes it the partner most likely to be able to publish openly and least likely to accept a result it cannot trace.
- UNKNOWN. Which public body, and whether it has any formal authority over the programme or is simply one partner of four.
- UNKNOWN. Whether it can veto, or only object. The brief records it as believing something, not as blocking anything.

## What it models, and at what resolution

- STATED. It "Defines component failures, compound events and acceptable service levels."
- INFERRED. The verb is "Defines", not "simulates". Meridian appears to specify the conditions under which other models are exercised rather than to run a physical model of the settlement.
- UNKNOWN. Whether Meridian runs any model at all. If it does not, the phrase "ARES owns no core model" plus "Each partner governs, validates and releases its own model" sits oddly with it, and the brief does not resolve this.
- UNKNOWN temporal resolution. None stated. A component failure specification could be an annual rate, a per-hour hazard or an event list, and these are not interchangeable.
- UNKNOWN spatial resolution. None stated. Whether a failure is defined against a named component, a subsystem or the whole colony is not said.
- UNKNOWN. What a "compound event" is in its usage, beyond that it is distinct from a single component failure.
- UNKNOWN. Whether its reliability metrics are frequentist rates, probabilistic distributions or scenario-based.

## What it consumes and produces

This is the first of two significant absences and it is worth stating plainly. Meridian has a produces clause and no consumes clause.

- STATED, produces. "It produces stress scenarios, reliability metrics and evidence requirements for judging whether a proposed system is sufficiently resilient."
- ABSENT, consumes. The brief gives Meridian no consumes clause at all. Every other characteristic of its inputs is therefore UNKNOWN.
- INFERRED. It cannot produce "reliability metrics" about a proposed system without receiving something describing that system's behaviour, so inputs must exist even though none are named. This is inference about the existence of inputs only, not about their content.
- UNKNOWN. What Meridian consumes, from whom, in what form and at what cadence. This is the largest single hole in the four partner descriptions.
- UNKNOWN. What an "evidence requirement" is as an artefact. It could be a written criterion, a checklist, a schema, a threshold or a test specification.
- UNKNOWN. Whether "stress scenarios" are parameter sets, narrative descriptions, time-series perturbations or model configurations.
- INFERRED. "Evidence requirements" is unusual among the twelve produced items in that it is a governance object rather than a data object, which suggests Meridian's output partly takes the form of rules that bind the other partners.

## Likely internal vocabulary

Inference throughout. No sample of Meridian's own writing exists in the brief.

- STATED terms the brief puts in Meridian's frame: "component failures", "compound events", "acceptable service levels", "stress scenarios", "reliability metrics", "evidence requirements", "sufficiently resilient", "mission-risk", "failure conditions", "uncertainty", "credible mission-risk claims".
- INFERRED. A risk institute usually speaks in hazard, failure mode, initiating event, consequence, exposure, likelihood, severity, margin, criterion, threshold and assurance case.
- INFERRED. It is the partner most likely to insist on the word "credible" and on a distinction between a result and evidence for a claim. The brief already uses both phrasings in its voice.
- INFERRED. It is the partner most likely to treat uncertainty as a explicit field on every variable rather than as an optional annotation.
- UNKNOWN. Whether it works to a named standard or framework. None is mentioned.

## What it needs and what needs it

- STATED, its position. "Meridian believes the current interface cannot represent failure conditions or uncertainty well enough to support credible mission-risk claims."
- INFERRED. Meridian therefore has a stake in the interface even though no exchange involving it is stated anywhere in the brief.
- INFERRED. The consortium needs Meridian for the review, because the review question requires "one material stress event" and stress scenarios are Meridian's stated product.
- UNKNOWN. Which interface "the current interface" refers to. The brief uses the definite article without antecedent. It could be the Solis to Tharsis exchange, the Tharsis to Helix interface, a general consortium-wide interface, or something else.
- UNKNOWN. Whether Meridian has ever received anything from another partner, or produced anything into the programme yet.
- UNKNOWN. Who consumes Meridian's stress scenarios. No partner's consumes clause names them.

## What would make it hard, and what would make it cooperative

- INFERRED, hard. Its objection is a standard-of-evidence objection, and those cannot be settled by a format fix. Meeting it may require changes to what other partners compute, not only to how they transmit it.
- INFERRED, hard. As the assurance voice it can withhold endorsement of the demonstration without ever having missed a deliverable of its own.
- INFERRED, hard. Its input requirements are undocumented in the brief, so anyone building the interface is guessing at what it needs.
- INFERRED, cooperative. It has already told the consortium what is wrong, which is more than a silent partner offers, and it has an explicit product to contribute to the required stress event.
- INFERRED, cooperative. A public institute is usually willing to write down criteria in advance, and "evidence requirements" suggests it already does.
- UNKNOWN. Whether its objection has been written down anywhere, or is only a stated belief.

---

# Helix Methods

## What kind of organisation it is

- STATED. Helix Methods is an "AI and computational-methods vendor".
- STATED. "It does not own the authoritative domain models."
- INFERRED. As a vendor it is paid to deliver tooling, so its incentive is to ship and to be seen to be useful, which explains why it has already built against an unconfirmed reading.
- INFERRED. Owning no authoritative model leaves it structurally dependent. It cannot validate anything on its own authority and needs another partner to vouch for correctness.
- INFERRED. It is the fastest-moving of the four. Tooling can be rebuilt in days, where a domain model carries a validation history that has to be redone with it.
- INFERRED. It is also the partner with the least standing in a scientific dispute, since the brief explicitly denies it ownership of authoritative models.
- UNKNOWN. Whether Helix is a small specialist shop or a large vendor, and whether its tooling is bespoke to ARES or a platform it also sells elsewhere.
- UNKNOWN. Whether Helix's tooling IP belongs to Helix, to ARES or to the foundation.

## What it does, and at what resolution

- STATED. "It is developing schema translation, automated quality checks, model orchestration, surrocontrol methods and tools for interpreting results across the consortium."
- INFERRED. Those five activities describe an integration layer rather than a domain model, which is consistent with the explicit statement that it owns no authoritative domain model.
- INFERRED. Surrocontrol methods imply it intends to approximate other partners' models, which requires access to their inputs and outputs at some volume.
- UNKNOWN. Which model or models the surrocontrols are meant to approximate. No target is named.
- UNKNOWN temporal and spatial resolution. Helix has none of its own that the brief states. A translation and orchestration layer inherits the resolutions of whatever it connects, and the brief does not say what it currently connects.
- UNKNOWN. How far along any of the five activities is, apart from the tooling built against a provisional interpretation.
- UNKNOWN. What "automated quality checks" check, and against what definition of correct.

## What it consumes and produces

This is the second and larger absence. Helix has neither a consumes clause nor a produces clause.

- ABSENT, consumes. The brief gives Helix no consumes clause.
- ABSENT, produces. The brief gives Helix no produces clause either. The verb used for Helix is "is developing", which describes work in progress rather than an output the consortium can receive.
- INFERRED. Helix is described in a different grammatical frame from the other three. Solis, Tharsis and Meridian are described by what they take and give. Helix is described by what it is building. That difference is in the source text and is worth carrying downstream.
- INFERRED. Schema translation implies it must consume at least two partners' data formats, so inputs exist even though none are named. This is inference about existence only.
- UNKNOWN. What Helix consumes, from whom, in what form.
- UNKNOWN. What Helix delivers as a product, to whom, and on what schedule.
- UNKNOWN. Whether any partner is contractually obliged to use Helix tooling, or whether adoption is voluntary.

## Likely internal vocabulary

Inference throughout. No sample of Helix's own writing exists in the brief.

- STATED terms the brief puts in Helix's frame: "schema translation", "automated quality checks", "model orchestration", "surrocontrol methods", "interpreting results", "tooling", "provisional interpretation", "interface variables", "authoritative domain models".
- INFERRED. A methods vendor usually speaks in schema, adapter, pipeline, contract, validation rule, endpoint, version, mapping, emulator and training set.
- INFERRED. It is the partner most likely to name a variable after its role in a data structure rather than after the physical quantity, which is precisely the kind of divergence that produces an ownership dispute.
- INFERRED. It is the most likely of the four to version things explicitly and to talk about breaking changes.
- UNKNOWN. Which languages, formats or standards its tooling actually uses. None is named.

## What it needs and what needs it

- STATED, it has an interface with Tharsis. "Tharsis and Helix disagree about the meaning and ownership of several interface variables."
- STATED, it has already committed work. "Helix has already built tooling against a provisional interpretation."
- INFERRED. It needs authoritative definitions from the domain partners, because it is stated not to own authoritative models and cannot therefore settle a definition itself.
- INFERRED. The consortium needs it for translation between partners whose vocabularies the brief says differ.
- UNKNOWN. Whether Helix has any relationship with Solis or with Meridian. The brief mentions neither.
- UNKNOWN. Whose provisional interpretation Helix built against. The brief says "a provisional interpretation" without saying whose, or whether anyone approved it.

## What would make it hard, and what would make it cooperative

- INFERRED, hard. It has sunk work into a reading that is disputed, so any resolution that goes against it costs it rework it may resist.
- INFERRED, hard. A vendor's instinct is to solve a problem by building, and the consortium's problem at Month 8 may be a definition problem rather than a tooling problem.
- INFERRED, hard. Owning no authoritative model means it can be overruled by any domain partner on any semantic question, which makes its position unstable and possibly defensive.
- INFERRED, cooperative. Of the four it can change fastest, so it is the cheapest partner to ask for rework.
- INFERRED, cooperative. Its five stated activities map directly onto the integration problem, so its interests and the programme's interests are closely aligned.
- INFERRED, cooperative. It has no domain turf to defend, which makes it a plausible neutral implementer of whatever the domain partners decide.

---

# Across the four

## Which pairs actually exchange anything, per the brief

Only two pairs are given any stated relationship. Everything else is absent.

- STATED, Solis to Tharsis. "A critical exchange from Solis to Tharsis is two months late, and the earliest available output is not in the format Tharsis planned around." Direction is stated. Content is not.
- STATED, Tharsis and Helix. "Tharsis and Helix disagree about the meaning and ownership of several interface variables." A shared set of interface variables is stated. Direction of flow is not.
- INFERRED, Tharsis to Solis. Solis consumes "demand envelopes" and Tharsis produces "time-series demand". A return path is implied by the two clauses but the brief never states such an exchange, and the two phrases are not the same object.
- ABSENT, Solis and Meridian. No exchange stated.
- ABSENT, Solis and Helix. No exchange stated.
- ABSENT, Tharsis and Meridian. No exchange stated, despite Meridian defining "acceptable service levels" and Tharsis producing "service shortfalls".
- ABSENT, Meridian and Helix. No exchange stated.
- Summary. Of six possible pairs, two are stated and four are absent. Meridian in particular is named in the crisis list but appears in no stated exchange with any partner.

## Where two partners appear to name one quantity differently

The brief never says these are the same quantity. What follows is a list of near-collisions in wording, marked as inference, offered so that a downstream reader can see where a naming conflict is plausible. None of this is a claim about the actual disagreement between Tharsis and Helix.

- Capacity. Solis produces "capacity choices". Tharsis consumes "available capacity". INFERRED that these plausibly refer to the same underlying quantity. UNKNOWN whether they do, and whether "choices" and "available" mark a real difference in meaning.
- Operating envelopes against operating constraints. Solis produces "operating envelopes". Tharsis consumes "operating constraints". INFERRED that these are plausibly the same object under two names, since Solis is the stated upstream partner. UNKNOWN whether an envelope and a constraint are the same thing in either partner's usage.
- Demand. Solis consumes "demand envelopes". Tharsis produces "time-series demand". INFERRED that these are the same quantity at different resolutions, since Tharsis works "hour by hour" and Solis over "multi-year horizons". UNKNOWN what aggregation converts one into the other, and who performs it.
- Service. Meridian defines "acceptable service levels". Tharsis produces "service shortfalls". INFERRED that a shortfall is measured against a level, so these are plausibly two halves of one quantity. UNKNOWN whether either partner defines service the same way, and no exchange between them is stated.
- Uncertainty and failure. Meridian produces "stress scenarios" and complains about representing "failure conditions or uncertainty". No other partner's consumes clause names either. UNKNOWN how failure and uncertainty enter any other partner's model.

## The Tharsis and Helix disagreement

- STATED. "Tharsis and Helix disagree about the meaning and ownership of several interface variables."
- STATED. "Helix has already built tooling against a provisional interpretation."
- STATED. The dispute covers two distinct things, meaning and ownership. The brief names both.
- UNKNOWN. Which variables. The brief says "several" and names none.
- UNKNOWN. What each partner's interpretation is.
- UNKNOWN. Why they differ.
- UNKNOWN. Which of the two, if either, is correct, and who has the authority to decide.
- UNKNOWN. Whether "ownership" here means data ownership, definitional authority, IP, or responsibility for producing the value.
- No content is inferred or reconstructed here. Any downstream artefact that fills this in is inventing, and the invention would sit at the root of the interface declarations and the assumption register.

## What the brief does not tell us about any interface

Listed plainly. Each item applies to every interface in the consortium, stated or absent.

- No variable names. Not one interface variable is named anywhere in the brief.
- No units for any quantity.
- No data formats, file types, schemas or encodings, for any exchange, in any direction.
- No delivery mechanism. Nothing about files, APIs, repositories, shared storage or manual handoff.
- No cadence. Nothing about how often any exchange happens or is meant to happen.
- No versioning convention, and no statement of how a partner signals that an output has changed.
- No time step or timestamp convention for any partner except Tharsis's "hour by hour".
- No spatial index or geography for any partner.
- No uncertainty representation. Meridian says the current interface cannot represent uncertainty well enough, but the brief never says how it represents it now.
- No failure representation, for the same reason.
- No metadata or provenance convention, despite the review question requiring "results traceable across the relevant models".
- No validation criteria. The brief says each partner validates its own model, and says nothing about how an exchanged quantity is checked.
- No agreed definitions document, and no statement that one exists or ever existed.
- No named owner for any interface. Ownership is stated to be disputed for the Tharsis and Helix variables and is simply unaddressed everywhere else.
- No format specification for the late Solis to Tharsis exchange, on either the delivered side or the side Tharsis "planned around".
- No identity for "the current interface" that Meridian objects to.
- No stated producer for four of the six consumed items. Solis's "technology assumptions", "resource limits" and "demand envelopes" and Tharsis's "population schedules" are consumed by someone and produced by no one named in the brief.
- No consumer for any of Meridian's three produced items.
- No stated inputs or outputs for Helix at all.
- No IP or confidentiality terms on any exchange, despite the brief stating that IP constraints differ across partners.
- No coupling decision. The brief states that "nobody has yet shown that a tight, bidirectional coupling is scientifically necessary", so even the intended topology is open.

## Closing note on completeness

Twelve produced items and six consumed items are named across the four partners. Every one of them is a noun phrase with no unit, no format, no schema and no cadence. Two partners have a full pair of clauses, one has produces only, one has neither. Two of six possible partner pairs have any stated exchange. That is the whole factual base. Any interface declaration written downstream will be mostly assumption, and the value of that exercise depends on the assumptions being visible as assumptions rather than dressed as facts.
