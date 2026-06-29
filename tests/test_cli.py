import io
import json
import unittest
from contextlib import redirect_stdout

from authlab.cli import main


class CliTests(unittest.TestCase):
    def _run_cli(self, *args: str) -> tuple[int, str]:
        stream = io.StringIO()
        with redirect_stdout(stream):
            exit_code = main(list(args))
        return exit_code, stream.getvalue()

    def test_validate_command_returns_summary(self) -> None:
        exit_code, output = self._run_cli("validate")

        self.assertEqual(exit_code, 0)
        summary = json.loads(output)
        self.assertEqual(summary["rules_total"], 5)
        self.assertEqual(summary["rules_valid"], 5)
        self.assertEqual(summary["cases_total"], 17)
        self.assertEqual(summary["cases_passed"], 17)

    def test_convert_command_reports_all_rules(self) -> None:
        exit_code, output = self._run_cli("convert", "--backend", "splunk")

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.count("OK"), 5)
        self.assertIn("compatibility", output)

    def test_report_command_generates_bilingual_outputs(self) -> None:
        exit_code, output = self._run_cli("report")

        self.assertEqual(exit_code, 0)
        self.assertIn("report.en.html", output)
        self.assertIn("report.es.html", output)

    def test_vm_check_is_read_only_and_successful(self) -> None:
        exit_code, output = self._run_cli("vm-check")

        self.assertEqual(exit_code, 0)
        summary = json.loads(output)
        self.assertFalse(summary["changes_applied"])
        self.assertIn("providers", summary)

    def test_all_command_runs_public_pipeline(self) -> None:
        exit_code, output = self._run_cli("all")

        self.assertEqual(exit_code, 0)
        self.assertIn("Repository audit: OK", output)
        self.assertIn("Generated", output)


if __name__ == "__main__":
    unittest.main()
