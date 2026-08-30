# Assumptions

The brief asks for the assumptions that materially shape the recommendation.
Materiality is the test rather than completeness. An assumption belongs here
when the recommendation depends on it.

The third column is the useful one. If nothing changes when an assumption is
wrong, it does not belong in this file.

## About the judgements that shape the recommendation

These came later than the rest and each of them changes what the
recommendation is, rather than only what it costs.

| Assumed | Why it is reasonable | What changes if it is false |
|---|---|---|
| Tight bidirectional coupling is scientifically necessary | Two independent reasons. The stress case is a correlated-failure case, and exchanging bounds once destroys that correlation by construction. And the model exists to support a design decision that has to keep people alive, which sets a floor on fidelity below which the model is inadmissible as evidence rather than merely coarse | The contract is still needed, but a single pass would suffice and the recommendation over-invests in the exchange. The five gaps stand either way |
| The model has to sit above the credibility threshold, meaning a decision maker can use it as a surrogate for the real system rather than as a test bed (Li et al., 2019) | It is a settlement model. Somebody eventually signs a habitat design on the strength of it, and no engineer signs on a tool whose own authors would not trust it to design one | The fidelity floor disappears and the exercise becomes a planning study, where loose coupling is defensible. This assumption, more than any other here, is what makes tight coupling non-negotiable rather than preferable |
| The coordinator can convene the partners and they will attend | Coordination is the role, and an exercise assuming partners would not come to meetings would not be an exercise | No plan of any shape works, and the problem is governance rather than interfaces |
| This is an acute crisis, and partners will accept direction they would decline in business as usual | Month 8, an exchange two months late, a live dispute over meaning, a risk laboratory saying the interface cannot carry its claims, and second-year funding in question | Week 1 cannot land four decisions, the sequencing lengthens, and the six weeks probably does not reach a stress case |
| Second-year funding depends on this demonstration | The brief frames the six weeks around what the foundation needs to see, and treats the demonstration as the thing being judged | The plan is too aggressive. With no funding cliff there is no reason to run a crude end-to-end in week 2 rather than build properly and demonstrate later |
| A long dust storm raises habitat demand by enough to matter | The physics of the direction is not in doubt. Less insolation means less passive solar gain into the habitat and any daylight contribution to habitat or crop lighting has to be replaced electrically, and dust mitigation work rises. Note that crew are always inside a pressurised habitat, so a storm changes no sheltering behaviour, and some loads fall, because extravehicular activity stops and suit charging, airlock cycling and rover operations fall with it | The size of the uplift is assumed here, not measured, and it is the weak link in the empirical argument. If it is near zero the correlation is one-sided, the compound event is a supply event only, and the necessity claim rests on the fidelity argument alone. This is the first thing the consortium should ask Tharsis, the habitat modelling partner, to establish |

## About the plan

| Assumed | Why it is reasonable | What changes if it is false |
|---|---|---|
| An end-to-end run on crude inputs is achievable in week 2 | It requires no correctness, no polish and one sol of data. Its only job is to make format, encoding and calendar mismatches fail early | Week 5's buffer absorbs one week of slip. Beyond that the stress case is dropped and week 6 shows the normal case, which is the review point at end of week 5 |
| Helix's existing adapter is of unknown usability | The brief says Helix built tooling against a provisional interpretation and says nothing about whether it works | Nothing, by construction. The plan is arranged to gain if the adapter helps and to lose nothing if it does not, which is why this assumption is safe to hold |
| Moving the derate into the contract is the expensive decision, not the expensive work | Implementing a derate is small. Getting a commercial partner to state publicly how its capacity degrades is not | The week 2 to 3 allocation is wrong in one direction or the other, and the review point at end of week 3 catches it |

## About the scenario

| Assumed | Why it is reasonable | What changes if it is false |
|---|---|---|
| The partners' stated consumes and produces describe their interface | It is the only interface description available, and it is where a real integrator would start on day one | The exchanges in the artifact are the wrong ones. The method of contracting them is unaffected |
| Solis's `capacity choices` and Tharsis's `available capacity` may be the same quantity | They sit on either side of one exchange and are described in different vocabularies | Nothing breaks. The artifact records this as a candidate awaiting confirmation and never as a fact, because the brief does not say they are the same |
| ARES can require a partner to declare a boundary variable without renegotiating that partner's IP position | Declaring what crosses a boundary is not disclosing what happens inside a model | The recommendation holds but the sequencing changes, because declaration becomes a contract negotiation rather than a technical task |
| The six-week review date is fixed and the scope is not | The funder set the date and the brief treats it as given | The recommendation is wrong. It trades scope for certainty only because the date cannot move |

## About the programme

| Assumed | Why it is reasonable | What changes if it is false |
|---|---|---|
| Partner capacity is uneven and constrains what can be attempted | A dedicated postdoc is not equivalent to a fraction of somebody's time | More than one exchange could be contracted in six weeks, and narrowing the scope becomes over-cautious |

## About the demonstration

| Assumed | Why it is reasonable | What changes if it is false |
|---|---|---|
| The settlement configuration under test can be a stated given rather than an optimised result | The brief asks whether the system can be evaluated, not whether a particular configuration is best, and it permits assumed inputs | The demonstration becomes a Solis optimisation run first, which is a second deliverable and does not fit six weeks |
| One material stress event is sufficient, and Meridian chooses it | The brief says one, and Meridian is the partner that defines stress scenarios and acceptable service levels | If ARES chooses it instead, the demonstration proves less, because the evidence requirement was set by the party being convinced |
| Traceable means the four explain-requirements can be answered from the record, rather than a full audit trail | The brief defines traceability by what the consortium must explain, not by a standard | A heavier provenance mechanism is needed and the six weeks does not carry it |

## Deliberately not assumed

Why the partners disagree. The brief states that Tharsis and Helix disagree
about the meaning and ownership of several interface variables. It never says
which variables, or why. Nothing here infers it and the artifact does not
diagnose it. What the artifact shows is that nobody has written down enough for
anyone to know, which is a narrower claim and a defensible one.

Anything requiring Mars or aerospace knowledge. The brief says none is required
and lists it under what is not being tested. Where a physical quantity is
needed it is a labelled given rather than a modelled result.
