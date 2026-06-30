import unittest

from authlab.demo import GITBOOK_BASE_URL, SCOPE_NOTICE, build_demo
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

    def test_demo_does_not_load_external_resources(self) -> None:
        forbidden = (
            "<script src",
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
        external_urls = [
            value
            for value in self.html.split('"')
            if value.startswith(("https://", "http://"))
        ]
        self.assertTrue(external_urls)
        for url in external_urls:
            with self.subTest(url=url):
                self.assertTrue(url.startswith(GITBOOK_BASE_URL))

    def test_demo_links_playbooks_and_report(self) -> None:
        self.assertIn("<a", self.html)
        for playbook in (
            "https://2dam-7.gitbook.io/window-auth/playbooks/auth-001_failed_logon_burst",
            "https://2dam-7.gitbook.io/window-auth/playbooks/auth-002_multiple_accounts",
            "https://2dam-7.gitbook.io/window-auth/playbooks/auth-003_success_after_failures",
            "https://2dam-7.gitbook.io/window-auth/playbooks/auth-004_account_lockout_burst",
            "https://2dam-7.gitbook.io/window-auth/playbooks/auth-005_privileged_remote_logon",
        ):
            with self.subTest(playbook=playbook):
                self.assertIn(playbook, self.html)
        self.assertIn("Open AUTH-003 playbook in GitBook", self.html)

    def test_demo_exposes_guided_soc_controls(self) -> None:
        for expected in (
            "ruleSelect",
            "caseSelect",
            "For reviewers: 3-minute guided path",
            "Previous case",
            "Next case",
            "Event timeline",
            "Analyst narrative",
            "Matched fields",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.html)


if __name__ == "__main__":
    unittest.main()
