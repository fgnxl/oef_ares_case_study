"""Readers for the four partner declarations, one per format.

The point of the case study lives here: the four partners describe the same
class of thing in four incompatible registers, and each needs its own reader to
reach the common model. The readers are the only code that knows about file
formats. Everything downstream sees model.py types.

Which partner writes in which register is a choice, and it is the brief's:

    Solis     spec sheet        tabular, units in the header, no prose. Looks
                               machine-readable, so its ambiguities are the
                               easiest of the four to miss.
    Tharsis   README paragraph  the interface stated in passing, in a section
                               about something else, cadence implied.
    Meridian  requirements      precise about obligation, vague about payload.
                               Meridian is complied with, not coupled to.
    Helix     JSON schema       fully specified types carrying no units, no
                               cadence and no semantics. The partner whose job
                               is translation declares no meaning.

Each reader records provenance: which file, and whether a field was stated
outright or inferred by the reader. What was inferred is exactly what the
checker cannot take on trust, and exactly what the page should surface.

Expected contents:
    load_all(data_dir):  dispatch on filename, return a list of Partner
    one reader per format, each returning the same type
"""

from __future__ import annotations
