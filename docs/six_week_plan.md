# The next six weeks

## This is triage

Month 8. An exchange between the two central models is two months late and
arrived in a format the receiver did not plan for. Two partners disagree about
what several interface variables mean and who owns them, and one of them has
already built against its own reading. The risk laboratory says the interface
cannot carry the claims it exists to make. Nobody has demonstrated that the
coupling everyone assumed is either necessary or achievable. Second-year funding
is in question.

That is an acute crisis rather than a programme that needs improving, and the
plan below is shaped accordingly. A consortium in this position does not run six
weeks of discovery and present findings. It gets one thing running in two weeks,
however crudely, and improves it every week after that.

The framing also changes what can be asked for. Partners accept direction in an
acute crisis that they would decline in business as usual, and the window for
that closes as soon as the crisis is declared over. Week 1 uses it.

## What has to be true at the end

The brief fixes the target. One repeatable end-to-end demonstration of a
proposed settlement configuration, under a normal operating case and one
material stress event, with results traceable across the relevant models. The
consortium must then be able to explain what information was exchanged, how
inconsistencies and uncertainty were handled, what was validated, and what the
demonstration does and does not establish.

Traceable and explainable are the words that do the work. A demonstration that produces a
number nobody can account for fails the review while appearing to succeed.

## The shape: two tracks, one critical path

Track A, Solis to Tharsis, is the critical path. These are the two models
that have to exchange anything at all. If their interface is not resolved there
is no end-to-end demonstration to run, no configuration to stress, and nothing
for the other partners to act on. Everything else in the programme is downstream
of this pair working.

Track B, Meridian's requirements, runs in parallel and not afterwards, which
is a dependency argument rather than a preference. Meridian defines what
evidence makes a resilience claim credible, and that determines what Track A's
interface has to be able to carry. Resolve Track A first and Meridian second and
the contract gets agreed twice, because the first version will not carry
uncertainty and Meridian will say so. Running them together means Track A knows
by week two what Track B will require of it.

## The test every item has to pass

Second-year funding depends on this demonstration, so the six weeks are not an
engineering plan with a demo at the end. They are a plan to get one
demonstration onto a board table, and each item is there because it passes that
test rather than because it is good practice.

Applied honestly, the test removes one item and adds two.

Removed. Implementing uncertainty propagation does not pass. A demonstration can
be traceable and deterministic at the same time, and Meridian's requirement is
for a credible mission-risk claim rather than for this demonstration. What the
six weeks produce is Meridian's evidence requirement written down, which is
cheap and shapes everything built afterwards. The implementation is deferred
with Meridian's agreement and a stated reason, which is a different thing from
being quietly descoped.

Added, because the test found them missing. Somebody has to propose the
configuration being evaluated, and nothing else in the plan produces one. Solis
does, in week two, and the brief permits an assumed configuration. And somebody
has to define what the normal operating case is, meaning which season, which
point in the dust cycle and which population state count as normal. That is a
decision rather than a default, and half the demonstration rests on it.

Everything else survives the test. Without a fixed calendar the two models produce numbers that
cannot be lined up. Without the aggregation operator Solis cannot consume what
Tharsis emits, so there is no end-to-end run. Without an owned derate the stress
case is Tharsis's private assumption, which fails the traceability requirement
precisely when it matters most, since the stress event is a derate event.
Without a versioned population schedule the run is not repeatable, and the brief
asks for repeatable. Without Meridian's thresholds the question of whether the
settlement met service levels has no answer any partner agrees with.

## Track A: resolve the Solis to Tharsis interface

Weeks 1 to 3. The objective is a declared, written contract covering the two
exchanges that already happen implicitly.

| Action | Closes | Output |
|---|---|---|
| Fix the calendar and epoch for every exchanged series | part of GAP-1 | one stated time basis, sols or Earth, with the conversion owned by name |
| Name the aggregation from hourly trace to planning envelope | GAP-1 | the statistic, the window, and the partner who computes it |
| Move the derate out of Tharsis and into the contract | GAP-2 | availability as a declared quantity with a named owner, not a private module |
| Assign ownership of the population schedule | GAP-4 | a producer, a revision cadence, and a version identifier on every run |
| Declare units, boundary and encoding on both sides | six families | a contract table with no empty cells, or empty cells that are visible |

Two of these are cheap and one is not. The calendar, the units and the schedule
ownership are afternoons. The derate is the hard one, because it currently sits
inside Tharsis fitted to a memo that predates the configuration it is applied
to, and moving it means Solis has to say publicly how its capacity degrades.
That is the meeting to schedule first and to allow most time for.

## Track B: understand what Meridian actually needs

Weeks 1 to 3, in parallel. The objective is the evidence specification, written
down, before the demonstration is designed around it.

| Action | Closes | Output |
|---|---|---|
| Elicit what a credible mission-risk claim requires | Meridian's stated objection | the evidence requirement, as a document |
| Fix how uncertainty crosses the boundary | six families | the representation, whether ensemble, interval or scenario set |
| Route the acceptable service levels to the model that applies them | GAP-3 | a published, versioned threshold set, replacing the ones Tharsis took from a standard |
| Choose the one material stress event | brief requirement | a named scenario, with its duration and what it stresses |

The third row costs nobody anything and should happen in week one. Tharsis is
currently reporting shortfalls against thresholds it lifted from a human
spaceflight standard because no partner issued any. Meridian has the set.
Publishing it is not a negotiation.

## Where Helix sits

The brief gives Helix no consumes clause and no produces clause. It says only
that Helix is developing a schema translation and compatibility layer, and that
it has already built tooling against a provisional interpretation of an
interface. Nothing else about it is stated, and nothing else is assumed here.

Helix stays in every technical session because it has working code sitting on the
one exchange that has already failed, and nobody else does. That is the reason,
rather than any deliverable the plan has given it. If the week-2 skeleton
needs something to move data between Solis and Tharsis, the fastest available
answer is the adapter Helix has already built, re-pointed to whatever the week-one
ruling says, which is a diff rather than a rewrite. That would turn its existing
work from the cause of a dispute into the thing that gets the consortium to an
end-to-end run weeks earlier.

Whether it plays out that way is not knowable from the brief, so the plan does
not depend on it. Helix is in the room because it might have something to bring,
and because the variables under dispute are the ones it has already interpreted.
Keeping it out would mean settling a contract that contradicts working code.

One thing Helix is deliberately not given, and this part is not a judgement about
Helix. A translation layer converts between vocabularies and cannot rule on what
a variable means, and nobody in the consortium could confer that standing on it.
So it attends every technical session and no session that settles meaning or
ownership. A test in `tests/test_check.py` asserts the seating plan honours that,
rather than leaving it as an intention.

## Weeks 4 to 6: run it

Week 4, the normal operating case, end to end, with the contract enforced.
Week 5, the stress event, using Meridian's named scenario.
Week 6, the traceability pass and the review pack.

The traceability pass is the deliverable, not the run. For every number in the
result, which model produced it, against which declared contract, on which
version of the population schedule, under which threshold set. That is the four
questions the review asks, and the contract answers all four by construction.

## Review points

End of week 1: the threshold set is published and the calendar is fixed, or
Track A is already carrying an unowned assumption into week 2.
End of week 3: the contract table exists with every cell either filled or
visibly empty. An empty cell is an acceptable outcome. An unnoticed one is not.
End of week 5: the stress case has run. If it has not, week 6 reports on the
normal case and says so, rather than compressing the traceability pass.

## What is deliberately not in the six weeks

No second model-to-model coupling. Partner capacity will not carry two contracts
at once and the first one is not finished.

No general co-simulation platform. Tight bidirectional coupling is the
recommendation and it is not six weeks of work. What the demonstration does
instead is run the stress case iterated: Solis proposes, Tharsis simulates with
the derate applied from the shared declared state rather than privately, and
Solis revises at least once. That shows the correlation between falling
generation and rising demand survives the exchange, which is the property the
platform would have to preserve, without building the platform to prove it.

No tooling beyond what the contract needs. The checker exists to make an unowned
object visible, and a dashboard built on top of an unresolved interface displays
the same private assumptions more attractively.

## Approach order is not work order

The leadership section sequences who is approached first, which is Helix and
Meridian, because both are already worse off under the status quo and will ask
for the contract rather than have to be persuaded of it. This section sequences
where the work goes, which is Solis to Tharsis first because nothing runs
without it. The two orders are different and both hold. The workshop that opens
Track A is easier to run when two of the four partners walked in wanting it.
