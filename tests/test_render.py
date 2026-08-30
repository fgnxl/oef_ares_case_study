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
import toy  # noqa: E402

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


class TestToyModel(unittest.TestCase):
    """The coupled toy model, and the provenance every one of its numbers carries.

    The section exists to be argued with. A reader who disagrees with a number
    has to be able to see that it was assumed and by whom, so a constant that
    reaches the page without a tag and a source is the one defect worth a test.
    """

    @classmethod
    def setUpClass(cls):
        cls.partners = parse.load_all(ROOT / "data")
        cls.findings = check.run(cls.partners)
        cls.html = render.page(cls.partners, cls.findings)
        start = cls.html.index('<section class="toy">')
        cls.section = cls.html[start:cls.html.index("</section>", start)]

    def test_the_section_slice_is_real(self):
        """Every test below reads this slice, so an empty one would pass them."""
        self.assertGreater(len(self.section), 4000)

    def test_every_constant_carries_a_tag_and_a_source(self):
        """The whole point of the section. No number arrives unattributed."""
        entries = toy.payload()["entries"]
        self.assertTrue(entries)
        for e in entries:
            with self.subTest(key=e["key"]):
                self.assertIn(e["tag"], ("stated", "assumed"))
                self.assertTrue(e["source"].strip(), "empty source")
                self.assertTrue(e["label"].strip(), "empty label")
                self.assertIsNotNone(e["value"])

    def test_a_bad_tag_is_rejected_at_construction(self):
        """The tag is checked where it is set, not where it is rendered."""
        with self.assertRaises(ValueError):
            toy.Const("X", "x", 1, "u", "guessed", "somewhere", "g")
        with self.assertRaises(ValueError):
            toy.Const("X", "x", 1, "u", "assumed", "   ", "g")

    def test_the_toy_section_reaches_the_page(self):
        self.assertIn("Would this settlement survive the storm", self.html)
        self.assertIn('<section class="toy">', self.html)
        self.assertIn("Loose, bounds exchanged once", self.section)
        self.assertIn("Tight, iterated on one dust state", self.section)
        for ident in ("sev", "up", "shed", "env", "verdict", "ceiling",
                      "loose-spark", "tight-spark", "loose-surv", "tight-surv"):
            with self.subTest(id=ident):
                self.assertIn(f'id="{ident}"', self.section)

    def test_every_constant_is_rendered_with_its_provenance(self):
        """Rendered, not merely embedded. A reader sees the tag on the page."""
        for e in toy.payload()["entries"]:
            with self.subTest(key=e["key"]):
                self.assertIn(render._e(e["label"]), self.section)
                self.assertIn(render._e(e["source"]), self.section)
        stated, assumed = toy.counts()
        self.assertEqual(len(toy.CONSTANTS), stated + assumed)
        self.assertGreaterEqual(
            self.section.count('<span class="tag assumed">'), assumed)

    def test_the_page_carries_the_toy_constants(self):
        self.assertIn('<script type="application/json" id="toy">', self.html)
        self.assertIn('"PER_CAP_KW"', self.html)
        self.assertIn('"tag": "assumed"', self.html)

    def test_the_shape_is_a_sol_of_multipliers_with_mean_one(self):
        """A shape whose mean drifts silently rescales the whole settlement."""
        self.assertEqual(24, len(toy.SHAPE))
        self.assertAlmostEqual(1.0, sum(toy.SHAPE) / 24, places=9)
        self.assertAlmostEqual(0.75, min(toy.SHAPE))
        self.assertAlmostEqual(1.35, max(toy.SHAPE))

    def test_the_toy_section_cites_no_clause_identifier(self):
        """The declarations in data/ are ours. Quoting a clause number back at

        a reader would present this repository's own worldbuilding as a
        partner's requirement. The values are read and used. The identifiers
        stay out of the prose.
        """
        forbidden = re.compile(
            r"OUT-\d|IN-\d|DEL-\d|SOL-ARES|MRL-ARES|THI-|HLX-|"
            r"clause\s+\d|\bMeridian\b", re.IGNORECASE)
        self.assertEqual([], forbidden.findall(self.section))

    def test_the_storage_figure_sits_under_the_toy_section(self):
        """The figure answers the question the model raises, so it follows it."""
        toy_at = self.html.index('<section class="toy">')
        fig_at = self.html.index("What an unowned load costs")
        boundary_at = self.html.index("<h2>The boundary</h2>")
        self.assertLess(toy_at, fig_at)
        self.assertLess(fig_at, boundary_at)

    def test_the_toy_section_is_first(self):
        """It is placed above everything the page rendered before it."""
        self.assertLess(self.html.index('<section class="toy">'),
                        self.html.index('<div class="counts">'))


if __name__ == "__main__":
    unittest.main()
