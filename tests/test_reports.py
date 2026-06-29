import csv
import unittest

from authlab.paths import REPORTS_DIR
from authlab.report import build_reports
from authlab.validation import run_validation


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        run_validation()
        # Conversion is exercised by the integration command and CI. A minimal
        # deterministic conversion summary is enough to unit-test rendering.
        from authlab.paths import ARTIFACTS_DIR

        (ARTIFACTS_DIR / "conversion.json").write_text(
            "[" + ",".join(
                f'{{"rule":"auth_{index:03d}.yml","backend":"splunk","ok":true,"output":"artifacts/splunk/auth_{index:03d}.spl","message":"converted"}}'
                for index in range(1, 6)
            ) + "]\n",
            encoding="utf-8",
        )
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


if __name__ == "__main__":
    unittest.main()

