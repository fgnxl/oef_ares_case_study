# AI use in this submission

The brief asks what tools were used, what changed as a result, and one material
limitation.

## What was used

An agentic coding environment (Anthropic's Claude, in the setup I use in my
consulting practice), over one session, with this repository's commit history as
the record. Four uses.

- **Research, to establish that the numbers are plausible.** Four agents ran in
  parallel on settlement generation and storage, per-resident demand and its
  hourly shape, dust storm severity and duration, and how schema translation is
  handled in real multi-model consortia. Each had to cite primary institutional
  sources and bank a local copy of every one it used. Those reports are not in
  this repository, because the brief says no Mars knowledge is required and a
  repository full of planetary science would misread the exercise. Every number
  in the artifact traces to one, and the page carries the reference list.
- **Implementation, to buy time for the argument.** The code in `src/` and the
  tests in `tests/` were written with assistance, against a design I specified:
  constants separated from the model, every constant tagged stated or assumed,
  provenance carried in the data rather than in a caption. Three hours does not
  otherwise contain a working model, a deck and a written diagnosis.
- **Drafting.** The documents in `docs/` were drafted with assistance and edited
  throughout. The arguments in them are mine.
- **Audit, because I was working alone.** Agents reviewed the repository against
  itself and against the brief, which on a fixed clock is the closest thing
  available to a second reader.

## What changed as a result

- The test suite was green while the checker matched nothing. The tests asserted
  against a fixture written in the brief's vocabulary while the real declarations
  sat at a different level of detail, so two of the four gaps never appeared.
  Fixed in `8398fbe`.
- A superseded position survived in four documents after the recommendation
  reversed. Finding all four took a search rather than memory, which is the
  failure this submission diagnoses. Fixed in `d8760fc`.
- The README described scaffolded directories in the present tense, which on a
  public repository is a claim rather than a plan. Fixed in `0ede6d5`.

## The material limitation

For most of the session the tool argued, fluently and with support, that a fully
specified boundary makes each model's interior irrelevant to the other and
therefore permits loose coupling. That argument is internally valid and it
answers the wrong question. What ends a settlement is a compound event in which
generation falls and demand shifts because both respond to the same weather, and
exchanging bounds once destroys that correlation by construction. I overruled it,
and the recommendation reversed at `d8760fc`.

That is the limitation worth reporting. Not an obviously wrong answer, which a
check catches, but a defensible answer to a subtly different question, which
survives review precisely because it looks rigorous. The safeguard was not a
better prompt or a better tool. It was domain judgement about what the model is
for.

One number in the artifact is assumed rather than measured, the demand response
to a storm, because no published figure for it exists. It sits on the page as a
control rather than in the code as a constant, and at zero it converges the two
designs and refutes the recommendation. An argument resting on an unmeasured
number belongs in the reader's hands.

## Where it was kept out

No language model runs inside the artifact. The model behind the sliders is
arithmetic and returns the same answer every time from the same settings. Its
thirty-two constants each carry a tag, stated or assumed, and a source, twelve
stated against twenty assumed, and a test refuses any constant that reaches the
page without both. A partner who dislikes a result has to be able to find the
number responsible and argue with it, which is not possible once a probabilistic
step sits in the evidence path.

The step before this one is where a model belongs. Reading a partner's real
documentation and proposing a draft declaration for a person to correct is a
suggestion pipeline with a human in the loop, which is a different thing
entirely.
