# Decisions

What was chosen, what it was chosen over, and why. Recorded as the choices were
made rather than reconstructed afterwards. The option space they were chosen
from is in `options.md`.

## Reading the consortium

Only two partners have a declared interface. Solis and Tharsis each have a
consumes clause and a produces clause. Meridian has produces only. Helix
declares neither. The brief describes what Helix is building, not what it takes
in or hands over. That asymmetry is in the brief and it shapes
everything below.

Meridian is complied with, not coupled to. It has no consumes clause, so it
is not downstream of anything. It sets what counts as evidence and judges the
result. Treating it as a model in the loop would be a category error.

Helix is the integration layer, not a party to the exchange. Schema
translation, orchestration and surrogates are the mechanism by which an
exchange happens. It builds an adapter once a contract exists rather than
guessing at one first, which is what the brief says already went wrong.

## The recommendation

One boundary gets specified first: Solis to Tharsis. Chosen over the other
three couplings because it is the only exchange the brief describes from both
sides, it spans the largest scale gap in the programme, multi-year capacity
optimisation against hour-by-hour simulation, and it is the one the brief
already reports as broken in three ways at once: two months late, in an
unexpected format, and named differently on each side.

Three couplings are deliberately not built in six weeks, each for its own
reason rather than one blanket excuse. Meridian because compliance is not
coupling. Helix because it is the mechanism. Any second model-to-model
coupling because partner capacity will not carry two contracts at once.

The brief leaves open whether tight bidirectional coupling is scientifically
necessary, and the answer taken here is that it is. A settlement model exists to
show what a settlement will actually endure, and what ends a settlement is a
compound event in which generation falls and demand rises together because both
respond to the same weather. A one-directional pass, or a single exchange of
bounds, cannot represent that coincidence at all. It returns a worst case for
each side separately, which is the wrong quantity.

So the argument is not that a declared boundary permits loose coupling. It is
that a declared boundary is what makes tight coupling safe to build. Two models
coupled tightly across three vocabularies, two clocks and an unowned derate do
not fail loudly, they agree quickly and wrongly, once per timestep. The contract
is the precondition, not the alternative.

## What the six-week demonstration is

The brief specifies it and it does not need inventing: one repeatable
end-to-end demonstration of a proposed settlement configuration under a normal
operating case and one material stress event, with results traceable across the
relevant models. The configuration and the stress event are inputs, and the
brief permits assumed ones.

The requirement that shapes the work is the sentence after it. The consortium
must be able to explain what information was exchanged, how inconsistencies and
uncertainty were handled, what was validated, and what the demonstration does
and does not establish.

Those four are the evidence specification, and each one is a thing the contract
already records.

| The review asks | The contract holds |
|---|---|
| What information was exchanged | Which quantities crossed which boundary, in what units, at what temporal and spatial resolution |
| How inconsistencies and uncertainty were handled | The disputed cells, and the uncertainty field on each exchanged quantity |
| What was validated | The checker's output against the declared contract |
| What it does and does not establish | The scope statement, and every cell still empty |

So specifying the boundary is not a step toward the review. It is the thing the
review asks the consortium to be able to explain, and a demonstration that runs
without it can show a result but cannot account for one.

## Leadership without direct control

The coordinator convenes. Calling the workshop where units get declared is the
job, and an exercise that assumed partners would not attend would not be an
exercise. The room is available.

What "without direct control" means is narrower and more useful than an
attendance problem. The four partners are a commercial firm, a university team,
a public institute and a translation contractor. Each has its own institutional
incentives and its own deliverables, and none of them reports to ARES. They will
attend. What cannot be done by fiat is make the coordinator's ask outrank their
own priorities once the meeting ends.

So the question is not how to compel a partner to write its side down. It is
what to put on the table so that writing it down is what each partner already
wants. The brief
supplies the answer: every partner is worse off under the status quo, and three
of them do not yet know how.

- **Helix is the most exposed and has the most to gain.** It has already built
  tooling against a provisional interpretation. If a contract is later declared
  and differs, that work is wasted. If no contract is ever declared, the work
  stays unsafe indefinitely. A declared contract is the only outcome in which
  Helix's existing investment survives, which makes Helix the first ally rather
  than the first problem.
- **Meridian's objection is the ask.** It states that the interface cannot
  represent failure conditions or uncertainty well enough for credible
  mission-risk claims. That is a request for the uncertainty clause. Nobody has
  to persuade Meridian of anything, only to agree with it in public and route
  its thresholds to the model that applies them, which is GAP-3.
- **Solis is being judged on assumptions it did not set.** Tharsis derates its
  capacity choices using a function Solis never saw, which is GAP-2. Declaring
  units, envelopes and the derate is how Solis takes back control of how its own
  design is evaluated. That is a gain rather than a concession, and Solis is the
  partner who benefits most from hearing it framed that way.
- **Tharsis carries blame for numbers it had to invent.** It reports shortfalls
  against thresholds it was never sent, and runs on a population schedule nobody
  owns. Declaring the routes moves that liability off Tharsis and onto the
  partners who should hold it.

The move is therefore neither compulsion nor consensus-building. It is showing
each partner the specific way the missing contract already costs them, and
letting the contract become what they ask for. The coordinator's authority is
convening plus the diagnosis, and the diagnosis is the part that does the work.

That is also why the artifact matters beyond being a demonstration. A checker
that reports "Solis publishes capacity choices and Tharsis consumes available
capacity, and neither declares a contract linking them" is a neutral third
party. It makes the gap a fact about the interface rather than an accusation
against a partner, which is what lets four institutions look at the same finding
without anyone having to concede anything first.

Sequencing follows from the incentives. Helix and Meridian are aligned with the
contract from the start, so they are approached first and the workshop opens
with two partners already asking for it. Solis and Tharsis are then joined by a
question about one specific thing nobody produces rather than by a request to
adopt a process.

## The artifact

One contract table with two renderings, chosen over a checker alone. The table
answers the integration question, which quantity crosses which boundary and on
whose authority. A critical path computed from the same table answers the
delivery question, which the brief requires inside the same eight slides. One
data set, two views, because the plan is computed from the contract table and
every cell still empty in it is a blocking dependency.

Its levers are programme constraints, not physics. Weeks to the review,
partner capacity, which stress event, how many exchanges to attempt, and the
scope of the demonstration. Chosen over settlement parameters because none of
these needs a correct Mars number and all of them change what is possible.
These are the levers a programme lead actually pulls.

Rejected: a settlement planner. It would need invented values for power per
resident, storage sizing and failure rates. None is defensible under
questioning and all of it sits inside what the brief says it is not testing.

Rejected: a coupling-necessity test. Scientifically the most interesting
option. It rests on a threshold with no basis in the brief, and the first
question would be how that threshold was chosen.

The artifact does not diagnose the disagreement. The brief says the
partners disagree about the meaning and ownership of interface variables and
never says which, or why. An artifact that identified the disagreement would be
inventing a finding and then detecting it. This one shows that nobody has
written down enough for anyone to know.
