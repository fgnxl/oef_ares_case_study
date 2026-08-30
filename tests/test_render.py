"""The page is the coupled toy model and nothing else. That is testable.

Two properties are worth a test above all others. The page must open from disk
with no network, which is easy to break by adding a font or a CDN script and
only breaks on the machine that is offline. And it must render byte-identically
from identical inputs, or its diff is unreadable.

The rest of these tests hold the page to being one thing. The checker still
runs, it is still a gate, and none of what it produces reaches the page, so the
tests that once asserted a provenance panel per declaration and every finding on
the page now assert the opposite property: the model is checked on the command
line and the page carries only the toy.
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

# Headings and hooks of the sections the page used to carry. A page that grows
# one of them back has stopped being one thing.
_REMOVED = (
    "The boundary",
    "The six weeks",
    "Where a finding comes from",
    "What an unowned load costs",
    'id="findings"',
    'class="chip',
    'class="detail"',
    'class="counts"',
    'id="model"',
    "blocking findings",
)


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

    def test_the_page_has_a_top_that_stands_alone(self):
        """A reader landing cold has to know what the two columns are.

        The title, the heading and the lede are the whole of the framing, so
        each has to be on the page and the lede has to name both models and say
        what each one does.
        """
        self.assertIn(f"<title>{render.TITLE}</title>", self.html)
        self.assertIn(f"<h1>{render._e(render.HEADING)}</h1>", self.html)
        self.assertIn(render._e(render.LEDE), self.html)
        for name in ("Solis", "Tharsis"):
            with self.subTest(partner=name):
                self.assertIn(name, render.LEDE)
        self.assertLess(self.html.index("<h1>"), self.html.index('class="dials"'))

    def test_the_widget_is_the_only_section(self):
        """One section element, and it is the toy model."""
        self.assertEqual(1, self.html.count("<section"))
        self.assertIn('<section class="toy">', self.html)

    def test_no_removed_section_survives_anywhere_on_the_page(self):
        """Deleting a section means its markup and its prose both go."""
        for needle in _REMOVED:
            with self.subTest(removed=needle):
                self.assertNotIn(needle, self.html)

    def test_the_checker_still_runs_and_stays_off_the_page(self):
        """The gate is real and its output is not rendered.

        The page no longer reports findings, which is only defensible while the
        findings are still produced and still block. Both halves are asserted
        here, because dropping the section would otherwise be indistinguishable
        from dropping the check.
        """
        self.assertTrue(self.findings)
        self.assertTrue(check.blocking(self.findings))
        for f in self.findings[:20]:
            with self.subTest(rule=f.rule, subject=f.subject):
                self.assertNotIn(f.message, self.html)
                self.assertNotIn(f.subject, self.html)

    def test_the_page_carries_the_toy_data_and_no_contract_model(self):
        """The embedded JSON is what makes the page readable without the repo."""
        self.assertIn('<script type="application/json" id="toy">', self.html)
        self.assertIn('"PER_CAP_KW"', self.html)
        self.assertNotIn('"declarations"', self.html)


    def test_the_opening_sets_the_scene_before_the_controls(self):
        """A reader who knows nothing has to be able to start at the top.

        The settlement, then the hazard, then why the model exists, then the
        partners, and all of it above the first slider.
        """
        paras = render._opening()
        self.assertGreaterEqual(len(paras), 3)
        self.assertLessEqual(len(paras), 4)
        for para in paras:
            with self.subTest(para=para[:40]):
                self.assertIn(render._e(para), self.html)
        joined = " ".join(paras)
        for token in ("1,000", "residents", "120", "dust", "Solis", "Tharsis"):
            with self.subTest(token=token):
                self.assertIn(token, joined)
        self.assertLess(self.html.index(render._e(paras[0])),
                        self.html.index('class="dials"'))

    def test_the_reference_list_is_present_and_non_empty(self):
        """The values came from somewhere and the page has to say where."""
        self.assertIn('<div class="refs">', self.html)
        self.assertGreaterEqual(render.reference_count(), 10)
        self.assertEqual(render.reference_count(), self.html.count("<li><b>"))
        self.assertIn("fictional", self.html)
        self.assertLess(self.html.index('class="dials"'),
                        self.html.index('<div class="refs">'))


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

    def test_the_controls_and_both_columns_reach_the_page(self):
        for ident in ("sev", "up", "shed", "env", "verdict", "ceiling",
                      "loose-spark", "tight-spark", "loose-surv", "tight-surv",
                      "loose-pv", "tight-pv", "loose-h2", "tight-h2"):
            with self.subTest(id=ident):
                self.assertIn(f'id="{ident}"', self.section)

    def test_each_column_names_its_regime_in_plain_words(self):
        """A column heading has to be readable before the argument is read.

        Both name a partner and say what it does, rather than naming a term
        from an argument the reader has not reached yet.
        """
        self.assertIn("Loose: Solis picks a capacity and stops", self.section)
        self.assertIn("Tight: Solis revises against Tharsis running the storm",
                      self.section)

    def test_each_column_separates_what_is_built_from_what_happens_to_it(self):
        """The capacities are the design. The survival number is the outcome."""
        self.assertEqual(2, self.section.count("What gets built"))
        self.assertEqual(2, self.section.count("What the storm does to it"))

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

    def test_the_shape_is_a_sol_of_multipliers_with_mean_one(self):
        """A shape whose mean drifts silently rescales the whole settlement."""
        self.assertEqual(24, len(toy.SHAPE))
        self.assertAlmostEqual(1.0, sum(toy.SHAPE) / 24, places=9)
        self.assertAlmostEqual(0.75, min(toy.SHAPE))
        self.assertAlmostEqual(1.35, max(toy.SHAPE))

    def test_the_page_cites_no_clause_identifier(self):
        """The declarations in data/ are ours. Quoting a clause number back at

        a reader would present this repository's own worldbuilding as a
        partner's requirement. The values are read and used. The identifiers
        stay out of the prose. The whole rendered section is scanned now, not
        one part of it, because the section is the whole page.
        """
        forbidden = re.compile(
            r"OUT-\d|IN-\d|DEL-\d|SOL-ARES|MRL-ARES|THI-|HLX-|"
            r"clause\s+\d|\bMeridian\b", re.IGNORECASE)
        self.assertEqual([], forbidden.findall(self.section))

    def test_the_storage_figure_is_supporting_material_inside_the_widget(self):
        """It is the mass under the store the two columns disagree about.

        Inside the section, below the verdict, and above the constants table,
        so it reads as part of the model rather than as a topic of its own.
        """
        self.assertIn("What the store above weighs", self.section)
        self.assertLess(self.section.index('id="verdict"'),
                        self.section.index("What the store above weighs"))
        self.assertLess(self.section.index("What the store above weighs"),
                        self.section.index('table class="consts"'))
        self.assertIn('src="data:image/png;base64,', self.section)


if __name__ == "__main__":
    unittest.main()
