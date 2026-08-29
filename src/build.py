"""Entry point. Reads data/, builds the contract model, checks it, writes the page.

Run from the repository root:

    make                  # or: python3 src/build.py
    make check            # or: python3 src/build.py --check-only

The pipeline is deliberately linear and has one shape:

    data/*  ->  parse.py  ->  model.py  ->  check.py  ->  render.py  ->  out/*.html

Nothing here talks to a network or a server. The page it writes opens from disk.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DEFAULT_OUT = ROOT / "out" / "ares_interface_map.html"


def main(argv: list[str] | None = None) -> int:
    """Run the pipeline. Returns a process exit code: 0 clean, 1 on violations."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate the contracts and report, without writing the page",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"output path for the generated page (default: {DEFAULT_OUT.relative_to(ROOT)})",
    )
    args = parser.parse_args(argv)

    # TODO(build): declarations = parse.load_all(DATA_DIR)
    # TODO(build): findings = check.run(declarations)
    # TODO(build): report findings to stdout, one line each
    # TODO(build): if args.check_only: return 1 if any blocking findings else 0
    # TODO(build): args.out.parent.mkdir(parents=True, exist_ok=True)
    # TODO(build): args.out.write_text(render.page(declarations, findings), encoding="utf-8")
    raise NotImplementedError("pipeline not yet wired; see TODO(build) above")


if __name__ == "__main__":
    sys.exit(main())
