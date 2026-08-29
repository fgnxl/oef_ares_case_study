# ARES integration: a contract-first recommendation

Candidate case study for the Energy Systems and AI Research Lead role, NEST
programme, Open Earth Foundation.

Prepared 29 August 2026. The commit history of this repository spans the work.

## The argument in one line

Tight bidirectional coupling is scientifically necessary, and a declared
interface contract is the precondition for building it rather than an
alternative to it.

## The deliverables

| Path | What it is |
|---|---|
| `deck/ares_board_deck.pptx` | The board deck, eight slides |
| `public/index.html` | The artifact, built. Opens from disk, no network |
| `docs/ai_use.md` | The AI-use disclosure |

## Running the artifact

    make          # read data/, check the contracts, write the page
    make check    # validate only, exit non-zero on any blocking finding
    make test     # 32 tests

Python 3.10 or later. No dependencies, no virtualenv, no build system.

The page is written to `out/` and copied to `public/index.html`, which is what
the static host serves. Committing a build artifact is normally wrong. Here the
page is the deliverable, the repository is the submission, and the host has no
Python, so both are written from one run to stop them drifting apart.

## The reasoning

| Path | What it is |
|---|---|
| `docs/findings.md` | The diagnosis: four objects on the boundary that no partner owns, and the six families of interface clause behind them |
| `docs/six_week_plan.md` | What the next six weeks do, with every action keyed to a gap, a meeting schedule, and where the slack is |
| `docs/decisions.md` | What was chosen, what it was chosen over, and leadership without direct control |
| `docs/assumptions.md` | Assumptions that materially shape the recommendation |
| `docs/partners.md` | Each partner read off the brief, every line marked stated, inferred or unknown |
| `docs/options.md` | Working notes. The option space, kept unedited so the choices can be checked against what they were chosen over |

## The inputs

`data/` holds four partner interface declarations, one per partner, each in a
different format: a spec sheet, a README, a clause-numbered requirements
document and a JSON schema. They are synthetic and were written for this
exercise. Each is a good example of its own genre and a poor interface contract,
which is the point.

Their numbers are grounded in background research that is not reproduced here,
because the brief states no Mars knowledge is required and a repository full of
planetary science would misread the exercise.
