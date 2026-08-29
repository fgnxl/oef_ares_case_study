"""The contract model. Plain dataclasses, no behaviour beyond validation of shape.

This is the vocabulary the rest of the artifact shares: what a partner is, what
an interface they publish or consume looks like, and what it means for two of
them to agree. Everything upstream (parse.py) produces these; everything
downstream (check.py, render.py) consumes them and nothing else.

Deliberately: no ORM, no schema library, no inheritance hierarchy. Four
partners and a handful of fields do not need one.

Expected contents:
    Partner      -- a named organisation and the declarations it publishes
    Interface    -- one published or consumed boundary: name, direction, fields
    Field        -- name, type, unit, required, and whether it was stated or inferred
    Contract     -- a matched pair: one partner's output against another's input
"""

from __future__ import annotations
