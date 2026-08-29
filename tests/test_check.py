"""Rules the checker must enforce, written down before the checker exists.

Each skipped test names one rule. Unskip as check.py implements it. A skipped
test is a visible commitment; a missing test is not.
"""

import unittest


class TestContractRules(unittest.TestCase):
    @unittest.skip("pending check.py: mismatched units between a producer and a consumer")
    def test_unit_mismatch_is_a_blocking_finding(self):
        raise NotImplementedError

    @unittest.skip("pending check.py: a consumer requires a field no producer publishes")
    def test_unmet_requirement_is_a_blocking_finding(self):
        raise NotImplementedError

    @unittest.skip("pending check.py: a field the parser inferred rather than read")
    def test_inferred_field_is_reported_but_not_blocking(self):
        raise NotImplementedError

    @unittest.skip("pending check.py: findings order must be stable across runs")
    def test_findings_are_deterministically_ordered(self):
        raise NotImplementedError


if __name__ == "__main__":
    unittest.main()
