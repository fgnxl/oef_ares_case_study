"""Test package. Exists for one reason: to put src/ on the import path.

The modules under src/ are flat scripts rather than an installed package, so
there is nothing to pip install and nothing to activate. This runs once, before
any test module is imported, and is the only import plumbing in the repository.

    make test     # or: python3 -m unittest discover -t . -s tests
"""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
