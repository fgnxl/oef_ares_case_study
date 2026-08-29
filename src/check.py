"""The checker. Runs rules over the model and returns findings, it does not print.

Separated from build.py so the rules are testable without touching the
filesystem, and separated from render.py so a finding is a value rather than a
paragraph of HTML.

A finding carries a severity, the contract or field it concerns, and a sentence
a human can act on. Severity decides the exit code, not the wording.

Expected contents:
    Finding       -- severity, subject, message
    run(partners) -- apply every rule, return the findings in a stable order
    the rules themselves, one function each, each independently testable
"""

from __future__ import annotations
