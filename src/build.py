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

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check  # noqa: E402
import parse  # noqa: E402
import render  # noqa: E402

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

    partners = parse.load_all(DATA_DIR)
    findings = check.run(partners)

    for f in findings:
        print(f)

    blocking = check.blocking(findings)
    print(f"\n{len(findings)} finding(s), {len(blocking)} blocking, "
          f"across {sum(len(p.declarations) for p in partners)} declarations "
          f"from {len(partners)} partners.")

    if args.check_only:
        return 1 if blocking else 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render.page(partners, findings), encoding="utf-8")
    print(f"wrote {args.out.relative_to(ROOT)}")

    # The page is the deliverable and Vercel has no Python, so the built page is
    # committed rather than generated at deploy. Writing both from one run is
    # what keeps the served page and the local one from drifting.
    served = ROOT / "public" / "index.html"
    served.parent.mkdir(parents=True, exist_ok=True)
    served.write_text(args.out.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"wrote {served.relative_to(ROOT)}")

    # Writing the page succeeds even when the contract does not. The page exists
    # to show the findings, so failing to build it because there are findings
    # would be backwards. Use --check-only, or make check, to gate on them.
    return 0


if __name__ == "__main__":
    sys.exit(main())
