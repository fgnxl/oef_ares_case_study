"""The four partner declarations are an input contract of the build.

parse.py dispatches on these filenames, so a rename or a deletion breaks the
page silently rather than loudly. This test is the loud part.
"""

import unittest
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# One per format. The formats differing is the point of the case study, so the
# set is asserted explicitly rather than globbed.
EXPECTED_DECLARATIONS = {
    "solis_spec_sheet.md",
    "tharsis_readme.md",
    "meridian_requirements.txt",
    "helix_schema.json",
}


class TestPartnerDeclarations(unittest.TestCase):
    def test_all_four_declarations_are_present(self):
        found = {p.name for p in DATA_DIR.iterdir() if p.is_file()}
        self.assertEqual(EXPECTED_DECLARATIONS, found & EXPECTED_DECLARATIONS)

    def test_no_declaration_is_empty(self):
        for name in sorted(EXPECTED_DECLARATIONS):
            with self.subTest(declaration=name):
                self.assertGreater((DATA_DIR / name).stat().st_size, 0)

    def test_the_four_formats_are_actually_different(self):
        suffixes = {Path(name).suffix for name in EXPECTED_DECLARATIONS}
        self.assertGreaterEqual(len(suffixes), 3)


if __name__ == "__main__":
    unittest.main()
