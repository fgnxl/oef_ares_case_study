"""Readers for the four partner declarations, one per format.

The point of the case study lives here: the four partners describe the same
class of thing in four incompatible registers (a spec sheet, a README
paragraph, a clause-numbered requirements list, a JSON schema), and each needs
its own reader to reach the common model. The readers are the only code that
knows about file formats. Everything downstream sees model.py types.

Each reader records provenance: which file, and whether a field was stated
outright or inferred by the reader. What was inferred is exactly what the
checker cannot take on trust, and exactly what the page should surface.

Expected contents:
    load_all(data_dir)   -- dispatch on filename, return a list of Partner
    one reader per format, each returning the same type
"""

from __future__ import annotations
