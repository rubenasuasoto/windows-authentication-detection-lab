import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

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

    def test_demo_command_generates_local_html(self) -> None:
        exit_code, output = self._run_cli("demo")

        self.assertEqual(exit_code, 0)
        self.assertIn("demo.html", output)

    def test_demo_open_command_uses_local_browser(self) -> None:
        with patch("authlab.cli.webbrowser.open") as open_mock:
            exit_code, output = self._run_cli("demo", "--open")

        self.assertEqual(exit_code, 0)
        self.assertIn("demo.html", output)
        open_mock.assert_called_once()

    def test_vm_check_is_read_only_and_successful(self) -> None:
        exit_code, output = self._run_cli("vm-check")

        self.assertEqual(exit_code, 0)
        summary = json.loads(output)
        self.assertFalse(summary["changes_applied"])
        self.assertIn("providers", summary)

    def test_vm_plan_prints_phases_without_host_changes(self) -> None:
        exit_code, output = self._run_cli("vm-plan")

        self.assertEqual(exit_code, 0)
        self.assertIn("VM-A", output)
        self.assertIn("VM-B", output)
        self.assertIn("no Windows features, networks or VMs are changed", output)

    def test_list_rules_outputs_detection_ids_and_playbooks(self) -> None:
        exit_code, output = self._run_cli("list-rules")

        self.assertEqual(exit_code, 0)
        self.assertIn("AUTH-001", output)
        self.assertIn("AUTH-005", output)
        self.assertIn("docs/playbooks/", output)
        self.assertIn("priority:", output)

    def test_explain_outputs_one_detection(self) -> None:
        exit_code, output = self._run_cli("explain", "AUTH-003")

        self.assertEqual(exit_code, 0)
        self.assertIn("Successful Logon After Repeated Failures", output)
        self.assertIn("Required fields", output)
        self.assertIn("Triage priority", output)
        self.assertIn("Playbook", output)

    def test_explain_unknown_detection_fails_cleanly(self) -> None:
        exit_code, output = self._run_cli("explain", "AUTH-999")

        self.assertEqual(exit_code, 1)
        self.assertIn("Unknown detection id", output)

    def test_playbook_command_prints_one_playbook(self) -> None:
        exit_code, output = self._run_cli("playbook", "AUTH-001")

        self.assertEqual(exit_code, 0)
        self.assertIn("# AUTH-001 Failed Logon Burst From One Source", output)
        self.assertIn("Triage questions", output)

    def test_narrative_command_prints_one_narrative(self) -> None:
        exit_code, output = self._run_cli("narrative", "AUTH-001")

        self.assertEqual(exit_code, 0)
        self.assertIn("## AUTH-001 Failed Logon Burst From One Source", output)
        self.assertIn("What happened", output)
        self.assertNotIn("## AUTH-002", output)

    def test_all_command_runs_public_pipeline(self) -> None:
        exit_code, output = self._run_cli("all")

        self.assertEqual(exit_code, 0)
        self.assertIn("Repository audit: OK", output)
        self.assertIn("Generated", output)


if __name__ == "__main__":
    unittest.main()
