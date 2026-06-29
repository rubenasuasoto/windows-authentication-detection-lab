import csv
import unittest

from authlab.convert import convert_rules
from authlab.paths import REPORTS_DIR
from authlab.report import build_reports
from authlab.validation import run_validation


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        run_validation()
        convert_rules("splunk")
        build_reports()

    def test_bilingual_reports_are_generated(self) -> None:
        for language in ("en", "es"):
            self.assertTrue((REPORTS_DIR / f"report.{language}.html").is_file())
            self.assertTrue((REPORTS_DIR / f"report.{language}.md").is_file())

    def test_matrix_contains_every_case(self) -> None:
        with (REPORTS_DIR / "validation-matrix.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 17)
        self.assertTrue(all(row["status"] == "pass" for row in rows))

    def test_html_has_no_external_assets(self) -> None:
        report = (REPORTS_DIR / "report.en.html").read_text(encoding="utf-8")
        self.assertNotIn("<script", report.lower())
        self.assertNotIn("https://", report.lower())

    def test_report_shows_reviewed_compatibility_queries(self) -> None:
        report = (REPORTS_DIR / "report.en.md").read_text(encoding="utf-8")
        self.assertIn("auth_003_success_after_failures.yml**: compatibility", report)
        self.assertIn("auth_005_privileged_remote_logon.yml**: compatibility", report)
        html = (REPORTS_DIR / "report.en.html").read_text(encoding="utf-8")
        self.assertIn("2 correlations use reviewed compatibility SPL", html)


if __name__ == "__main__":
    unittest.main()
