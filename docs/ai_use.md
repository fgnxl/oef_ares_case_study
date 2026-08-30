# AI use in this submission

The brief asks for the tools used, what was checked or changed as a result, and
one material error or limitation encountered. All three are below, along with
the place where AI was deliberately kept out.

## What was used

The work was done in an agentic coding environment (Anthropic's Claude, running
in the setup I use in my consulting practice) over a single session, with this
repository's commit history as the record. It was used in four ways.

- **Research.** Four background agents ran in parallel to establish that the
  synthetic partner declarations carry plausible engineering numbers: settlement
  generation, storage and life support with their units, per-resident demand
  rates and their hourly shape, environmental stressors and reliability
  thresholds, and how schema translation layers are handled in real multi-model
  consortia. Each had to cite primary institutional sources, bank a local copy of
  every source it used, and write a register with a hash per file. Those reports
  and sources are not in this repository, because the brief states no Mars
  knowledge is required and a repository full of planetary science would misread
  the exercise. They exist, and any number in `data/` traces to one.
- **Drafting.** The documents in `docs/` were drafted with assistance and edited
  throughout. The arguments in them are mine.
- **Implementation.** The code in `src/` and the tests in `tests/` were written
  with assistance, against a design I specified: general rules naming no partner,
  provenance recorded per clause, the gaps computed rather than declared.
- **Audit.** Two agents reviewed the repository against itself and against the
  brief. Both found real defects, listed below.

## What was checked, and what changed

Three findings changed the submission.

- **The README was overclaiming.** An audit found it describing scaffolded
  directories in the present tense. On a public repository that is a claim rather
  than a plan, so the file now separates what is built from what is scaffolded.
  Fixed in `0ede6d5`.
- **The checker was green while the document and the artifact disagreed.** The
  tests assert that the four gaps fall out of the general rules, and they passed.
  Run against the actual declarations, the checker returned no matched pairs at
  all, so two of the four gaps never appeared. The tests were asserting against a
  fixture written in the brief's vocabulary while the real declarations were
  written at a different level of detail. A real finding was hiding behind a
  green suite. Fixed in `8398fbe`.
- **A superseded position survived in four places.** When the recommendation on
  coupling reversed, the old argument still stood in the README, in
  `findings.md`, in `decisions.md` and in `six_week_plan.md`. Finding all four
  took a search rather than memory, which is the same failure this submission
  diagnoses, occurring inside the repository that diagnoses it. Fixed in
  `d8760fc`.

## The material limitation

I built the wrong artifact first, and kept improving it.

The original tool parsed the four synthetic partner declarations and reported
which interface clauses they failed to state. I wrote those four documents. So
the tool discovered the omissions I had put in them and reported 344 absent
clauses as a finding. It graded its own homework, and the more rigorous the
checker looked, the more clearly it did so. It also contained no energy system
and no physics, in a submission for an energy systems role.

Nobody caught that for two hours, including me, because each individual
improvement was real. Provenance panels, better figures, a cleaner layout. The
thing was wrong at the root and getting steadily more polished.

What replaced it sizes a settlement two ways, once the way the partners work
today and once with the two models revising against each other, runs both
through the same 120 sol dust storm, and reports how many sols each survives.
The two approaches do not disagree about an answer. They cause you to build
different things, and the survival number is what happens to what you built.

The second limitation is in that model and it is deliberate. One of its four
controls is the demand response to a storm, and it reaches zero. At zero the two
designs converge exactly and the recommendation refutes itself on screen. That
coefficient is assumed rather than measured, because a literature search found
no published figure for it, and the honest thing to do with an argument resting
on an unmeasured number is to put the number in the reader's hands.

A third, smaller one worth recording because it is the same class. Partway
through, a slide quoted a clause from one of those synthetic partner documents
as evidence that a partner required something. It is our own invention presented
back to the assessors as a finding. It is gone, and a rule now applies across
the submission: anything in `data/` is an input, never evidence.

## The earlier limitation

The tool produced a confident, well-argued and wrong recommendation, and a human
had to overrule it.

For most of the session this repository argued that a fully specified boundary
makes each model's interior irrelevant to the other, and therefore permits loose
coupling. That argument is internally valid, it is well supported, and it answers
the wrong question. It was rejected on the grounds that a settlement model exists
to show what a settlement will actually endure, and what ends a settlement is a
compound event in which generation falls and demand rises together because both
respond to the same weather.

The reversal is in the history at `d8760fc`, and the superseded position stands
in the commits before it.

The lesson generalises. The failure was not an obviously wrong answer that a
check would catch. It was a fluent and defensible answer to a subtly different
question, which is the class of error that survives review precisely because it
looks rigorous. The safeguard was not a better prompt and not a better tool. It
was a domain expert reading the recommendation and rejecting its premise.

## Where AI was deliberately kept out

There is no model inside the artifact. The checker is deterministic rule code. No
language model reads a declaration at runtime, classifies a finding or scores a
match.

That is a decision. The artifact exists to make an unowned object visible to four
institutions that do not currently agree with each other, and in that setting a
finding has to be reproducible byte for byte and its reasoning has to be legible
in a function. The first partner to dislike a result would otherwise be right to
question it, and there would be no answer available. `test_render.py` asserts
byte-identical output from identical input for the same reason.

The readers in `parse.py` are the boundary case. Extracting an interface from a
prose README is a task a language model does well, and doing it that way would
make the tool generalise beyond these four documents. It is hand-written instead,
and every clause records whether the document stated it or the reader inferred
it, so anyone disagreeing with an extraction can see which sentence produced it.
A probabilistic step here would put the tool's credibility on the same footing as
the assumptions it exists to expose.

The step before this one is where a model belongs: reading a partner's real
documentation and proposing a draft declaration for a person to correct. That is
a suggestion pipeline with a human in the loop, which is a different thing from
putting a model in the evidence path.
