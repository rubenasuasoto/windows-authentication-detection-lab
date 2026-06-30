import re
import unittest

from authlab.paths import ROOT

PUBLIC_DOCS = [
    ROOT / "README.md",
    ROOT / "README.es.md",
    ROOT / "SECURITY.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "SUMMARY.md",
    ROOT / "docs" / "ALERT_NARRATIVES.md",
    ROOT / "docs" / "ARCHITECTURE.md",
    ROOT / "docs" / "DATA_SOURCES.md",
    ROOT / "docs" / "DETECTION_CATALOG.md",
    ROOT / "docs" / "GITBOOK_SETUP.md",
    ROOT / "docs" / "TUNING_GUIDE.md",
    ROOT / "docs" / "VALIDATION.md",
    ROOT / "docs" / "VM_LAB.md",
    ROOT / "docs" / "VM_READINESS_CHECKLIST.md",
    ROOT / "docs" / "PORTFOLIO_PRESENTATION.md",
    ROOT / "docs" / "RELEASE_CHECKLIST.md",
    ROOT / "docs" / "playbooks" / "README.md",
]


class PublicDocumentationTests(unittest.TestCase):
    def test_public_docs_are_utf8_without_mojibake(self) -> None:
        bad_markers = ("Ã", "Â", "�")
        for path in PUBLIC_DOCS:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertFalse(any(marker in text for marker in bad_markers))

    def test_readme_links_point_to_existing_files(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme)
        local_links = [link for link in links if not link.startswith(("http://", "https://"))]

        self.assertIn("docs/DETECTION_CATALOG.md", local_links)
        self.assertIn("docs/PORTFOLIO_PRESENTATION.md", local_links)
        self.assertIn("docs/RELEASE_CHECKLIST.md", local_links)
        self.assertIn("docs/TUNING_GUIDE.md", local_links)
        self.assertIn("docs/GITBOOK_SETUP.md", local_links)
        for link in local_links:
            target = ROOT / link.split("#", 1)[0]
            with self.subTest(link=link):
                self.assertTrue(target.exists(), f"Broken README link: {link}")

    def test_detection_catalog_matches_manifest_identity(self) -> None:
        import json

        manifest = json.loads((ROOT / "rules" / "manifest.json").read_text(encoding="utf-8"))
        catalog = (ROOT / "docs" / "DETECTION_CATALOG.md").read_text(encoding="utf-8")

        for detection in manifest["detections"]:
            with self.subTest(key=detection["key"]):
                self.assertIn(detection["key"], catalog)
                self.assertIn(detection["title"], catalog)

    def test_each_detection_has_a_playbook(self) -> None:
        import json

        manifest = json.loads((ROOT / "rules" / "manifest.json").read_text(encoding="utf-8"))
        playbook_dir = ROOT / "docs" / "playbooks"
        playbooks = {path.name for path in playbook_dir.glob("AUTH-*.md")}

        self.assertEqual(len(playbooks), 5)
        for detection in manifest["detections"]:
            expected_prefix = detection["key"]
            with self.subTest(key=detection["key"]):
                self.assertTrue(
                    any(name.startswith(expected_prefix) for name in playbooks),
                    f"Missing playbook for {detection['key']}",
                )

    def test_gitbook_navigation_covers_playbooks(self) -> None:
        summary = (ROOT / "docs" / "SUMMARY.md").read_text(encoding="utf-8")
        setup = (ROOT / "docs" / "GITBOOK_SETUP.md").read_text(encoding="utf-8")
        config = (ROOT / ".gitbook.yaml").read_text(encoding="utf-8")

        self.assertIn("root: ./docs/", config)
        self.assertIn("readme: README.md", config)
        self.assertIn("summary: SUMMARY.md", config)
        self.assertIn("Branch: `main`", setup)
        self.assertIn("GitHub -> GitBook", setup)
        for detection_id in ("AUTH-001", "AUTH-002", "AUTH-003", "AUTH-004", "AUTH-005"):
            with self.subTest(detection_id=detection_id):
                self.assertIn(detection_id, summary)
                self.assertIn(detection_id, setup)

    def test_tuning_guide_covers_visible_tuning_cases(self) -> None:
        import json

        fixtures = json.loads(
            (ROOT / "tests" / "fixtures" / "scenarios.json").read_text(encoding="utf-8")
        )
        guide = (ROOT / "docs" / "TUNING_GUIDE.md").read_text(encoding="utf-8")
        tuning_cases = [
            item for item in fixtures["cases"] if item.get("disposition") == "tune"
        ]

        self.assertGreaterEqual(len(tuning_cases), 2)
        for case in tuning_cases:
            with self.subTest(case_id=case["case_id"]):
                self.assertIn(case["case_id"], guide)
                self.assertIn(case["rule_id"], guide)

    def test_portfolio_guide_keeps_defensive_scope_visible(self) -> None:
        text = (ROOT / "docs" / "PORTFOLIO_PRESENTATION.md").read_text(encoding="utf-8")

        self.assertIn("synthetic JSON events", text)
        self.assertIn("documentation IP ranges", text)
        self.assertIn("It is not a production SIEM deployment", text)
        self.assertIn("offensive simulations", text)

    def test_spanish_readme_links_portfolio_guide(self) -> None:
        text = (ROOT / "README.es.md").read_text(encoding="utf-8")

        self.assertIn("Presentación", text)
        self.assertIn("docs/PORTFOLIO_PRESENTATION.md", text)

    def test_readmes_explain_how_to_review_the_project(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        spanish = (ROOT / "README.es.md").read_text(encoding="utf-8")

        self.assertIn("How to review this project", english)
        self.assertIn("Cómo revisar este proyecto", spanish)
        for expected in ("rules/manifest.json", "tests/fixtures/scenarios.json", "authlab all"):
            with self.subTest(expected=expected):
                self.assertIn(expected, english)
                self.assertIn(expected, spanish)

    def test_readmes_list_review_commands(self) -> None:
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        spanish = (ROOT / "README.es.md").read_text(encoding="utf-8")

        for expected in (
            "authlab demo",
            "authlab vm-plan",
            "authlab playbook AUTH-001",
            "authlab narrative AUTH-001",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, english)
                self.assertIn(expected, spanish)

    def test_release_checklist_keeps_tagging_manual(self) -> None:
        text = (ROOT / "docs" / "RELEASE_CHECKLIST.md").read_text(encoding="utf-8")

        self.assertIn("git tag -a v0.1.0", text)
        self.assertIn("workflow badge", text)
        self.assertIn("synthetic data", text)

    def test_validation_doc_lists_splunk_outputs(self) -> None:
        text = (ROOT / "docs" / "VALIDATION.md").read_text(encoding="utf-8")

        self.assertIn("Splunk conversion outputs", text)
        self.assertIn("auth_003_success_after_failures.spl", text)
        self.assertIn("auth_005_privileged_remote_logon.spl", text)
        self.assertIn("reviewed compatibility", text)

    def test_alert_narratives_cover_every_detection(self) -> None:
        import json

        manifest = json.loads((ROOT / "rules" / "manifest.json").read_text(encoding="utf-8"))
        narratives = (ROOT / "docs" / "ALERT_NARRATIVES.md").read_text(encoding="utf-8")

        for detection in manifest["detections"]:
            with self.subTest(key=detection["key"]):
                self.assertIn(detection["key"], narratives)
                self.assertIn(detection["title"], narratives)
        for phrase in ("What happened", "Why it matters", "What to check next", "Decision"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, narratives)

    def test_portfolio_guide_mentions_alert_narratives(self) -> None:
        text = (ROOT / "docs" / "PORTFOLIO_PRESENTATION.md").read_text(encoding="utf-8")

        self.assertIn("docs/ALERT_NARRATIVES.md", text)
        self.assertIn("analyst-facing narratives", text)

    def test_portfolio_guide_mentions_local_demo(self) -> None:
        text = (ROOT / "docs" / "PORTFOLIO_PRESENTATION.md").read_text(encoding="utf-8")

        self.assertIn("reports/latest/demo.html", text)
        self.assertIn("local mini-SOC demo", text)
        self.assertIn("Three-minute reviewer path", text)

    def test_public_docs_explain_demo_access(self) -> None:
        expected = (
            "https://rubenasuasoto.github.io/windows-authentication-detection-lab/"
            "reports/latest/demo.html"
        )
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        spanish = (ROOT / "README.es.md").read_text(encoding="utf-8")
        release = (ROOT / "docs" / "RELEASE_CHECKLIST.md").read_text(encoding="utf-8")

        self.assertIn("uv run authlab demo --open", english)
        self.assertIn("uv run authlab demo --open", spanish)
        self.assertNotIn(expected, english)
        self.assertNotIn(expected, spanish)
        self.assertIn(expected, release)

    def test_vm_checklist_keeps_changes_explicit(self) -> None:
        text = (ROOT / "docs" / "VM_READINESS_CHECKLIST.md").read_text(encoding="utf-8")

        self.assertIn("uv run authlab vm-check", text)
        self.assertIn("uv run authlab vm-plan", text)
        self.assertIn("No offensive tools", text)
        self.assertIn("Do not commit `.evtx`", text)
        self.assertIn("internal-only", text)


if __name__ == "__main__":
    unittest.main()
