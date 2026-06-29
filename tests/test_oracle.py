import unittest

from authlab.oracle import evaluate_cases, load_cases


class OracleTests(unittest.TestCase):
    def test_every_synthetic_case_matches_its_expectation(self) -> None:
        failures = [result for result in evaluate_cases() if result["status"] != "pass"]
        self.assertEqual(failures, [], failures)

    def test_every_rule_has_positive_negative_and_boundary_cases(self) -> None:
        categories: dict[str, set[str]] = {}
        for case in load_cases():
            categories.setdefault(case["rule_id"], set()).add(case["category"])
        self.assertEqual(set(categories), {f"AUTH-{number:03d}" for number in range(1, 6)})
        for rule_categories in categories.values():
            self.assertTrue({"positive", "negative", "boundary"}.issubset(rule_categories))

    def test_tuning_cases_are_visible_alerts(self) -> None:
        tuning = [result for result in evaluate_cases() if result["disposition"] == "tune"]
        self.assertGreaterEqual(len(tuning), 2)
        self.assertTrue(all(result["expected"] and result["observed"] for result in tuning))


if __name__ == "__main__":
    unittest.main()

