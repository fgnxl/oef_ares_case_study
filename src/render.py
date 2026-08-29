"""Renders the model and the findings into one self-contained HTML file.

Self-contained is a hard requirement, not a preference: the page has to open
from disk on a laptop with no network and no server. CSS and JavaScript are
inlined into template.html. No CDN, no fetch, no build step, no framework.

Interactivity is limited to what a reader needs to follow the argument:
selecting a partner or a contract and seeing what depends on it. That is
achievable in a few dozen lines of vanilla JavaScript in the template.

Expected contents:
    page(partners, findings) -> str   -- substitute into template.html
    small helpers that turn model objects into the JSON blob the page embeds
"""

from __future__ import annotations
