"""The generated page must open from disk with no network. That is testable.

The self-contained requirement is the one property of the output worth a test:
it is easy to break by adding a font or a CDN script, and the break only shows
up on the machine that is offline.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import check  # noqa: E402
import parse  # noqa: E402
import render  # noqa: E402

_EXTERNAL = re.compile(r"""(?:src|href)\s*=\s*["\'](https?:|//)""")


class TestGeneratedPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.partners = parse.load_all(ROOT / "data")
        cls.findings = check.run(cls.partners)
        cls.html = render.page(cls.partners, cls.findings)

    def test_page_has_no_external_references(self):
        """It must open from disk on a laptop with no network."""
        self.assertEqual([], _EXTERNAL.findall(self.html))

    def test_render_is_deterministic(self):
        """Same inputs, byte-identical page, or the diff is unreadable."""
        again = render.page(self.partners, check.run(self.partners))
        self.assertEqual(self.html, again)

    def test_every_finding_reaches_the_page(self):
        """Counted by severity class, which only findings rows carry.

        This test previously counted every row on the page, which passed until
        the provenance tables arrived and then failed for a reason that had
        nothing to do with findings going missing. A count is only a check if it
        counts the thing it names.
        """
        severities = sum(self.html.count(f'<tr class="{s}"')
                         for s in ("blocking", "reported", "advisory"))
        self.assertEqual(len(self.findings), severities)

    def test_every_declaration_has_a_provenance_panel(self):
        """The panel is where a finding stops being an assertion."""
        import parse
        from model import all_declarations
        n = len(all_declarations(parse.load_all(ROOT / "data")))
        self.assertEqual(n, self.html.count('class="detail"'))

    def test_the_page_carries_its_own_data(self):
        """The embedded JSON is what makes the page readable without the repo."""
        self.assertIn('<script type="application/json" id="model">', self.html)
        self.assertIn('"declarations"', self.html)


if __name__ == "__main__":
    unittest.main()
