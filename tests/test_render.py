"""The generated page must open from disk with no network. That is testable.

The self-contained requirement is the one property of the output worth a test:
it is easy to break by adding a font or a CDN script, and the break only shows
up on the machine that is offline.
"""

import unittest


class TestGeneratedPage(unittest.TestCase):
    @unittest.skip("pending render.py: no src/href pointing at http(s) or //")
    def test_page_has_no_external_references(self):
        raise NotImplementedError

    @unittest.skip("pending render.py: same inputs produce a byte-identical page")
    def test_render_is_deterministic(self):
        raise NotImplementedError


if __name__ == "__main__":
    unittest.main()
