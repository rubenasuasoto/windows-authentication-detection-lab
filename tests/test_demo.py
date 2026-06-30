import unittest

from authlab.demo import SCOPE_NOTICE, build_demo
from authlab.paths import REPORTS_DIR


class DemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.demo_path = build_demo()
        cls.html = cls.demo_path.read_text(encoding="utf-8")
        cls.lower_html = cls.html.lower()

    def test_demo_is_generated_under_reports_latest(self) -> None:
        self.assertEqual(self.demo_path, REPORTS_DIR / "demo.html")
        self.assertTrue(self.demo_path.is_file())

    def test_demo_contains_detection_ids_and_case_categories(self) -> None:
        for rule_id in ("AUTH-001", "AUTH-002", "AUTH-003", "AUTH-004", "AUTH-005"):
            with self.subTest(rule_id=rule_id):
                self.assertIn(rule_id, self.html)
        for category in ("positive", "negative", "boundary", "false_positive", "tune"):
            with self.subTest(category=category):
                self.assertIn(category, self.html)

    def test_demo_keeps_defensive_scope_visible(self) -> None:
        self.assertIn(SCOPE_NOTICE, self.html)
        self.assertIn("Synthetic lab only", self.html)
        self.assertIn("No production logs", self.html)

    def test_demo_is_self_contained_and_local_only(self) -> None:
        forbidden = (
            "<script src",
            "https://",
            "http://",
            "<form",
            'type="file"',
            "fetch(",
            "xmlhttprequest",
            "sendbeacon",
        )
        for marker in forbidden:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, self.lower_html)

    def test_demo_exposes_guided_soc_controls(self) -> None:
        for expected in (
            "ruleSelect",
            "caseSelect",
            "Event timeline",
            "Analyst narrative",
            "Matched fields",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.html)


if __name__ == "__main__":
    unittest.main()
