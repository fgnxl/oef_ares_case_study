# Decisions

What was chosen, what it was chosen over, and why. Recorded as the choices were
made rather than reconstructed afterwards. The option space they were chosen
from is in `options.md`.

## Reading the consortium

Only two partners have a declared interface. Solis and Tharsis each have a
consumes clause and a produces clause. Meridian has produces only. Helix has
neither. That asymmetry is in the brief and it shapes everything below.

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

**Tight coupling is necessary exactly to the extent that the boundary is
underspecified.** This is the argument, and it answers the question the brief
leaves open about whether tight bidirectional coupling is scientifically
necessary. A fully specified boundary makes the interior of each model
irrelevant to the other, which is what permits loose coupling. Where the boundary is vague, tight coupling is the only remaining way to
keep the two consistent.

## The artifact

A constraint model with two renderings, over a validator alone. The
contract matrix answers the integration problem. A critical path derived from
the same data answers the executable half, which the brief requires inside the
same eight slides. One object, two views, because the plan is a projection of
the contract state and every empty cell is a blocking dependency.

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
