import json
import unittest

from authlab.paths import MANIFEST_PATH, RULES_DIR
from authlab.rules import load_rule_documents, validate_rule_pack


class RulePackTests(unittest.TestCase):
    def test_pack_contains_exactly_five_primary_detections(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["detections"]), 5)
        self.assertEqual(
            {item["file"] for item in manifest["detections"]},
            {path.name for path in RULES_DIR.glob("*.yml")},
        )

    def test_primary_ids_are_unique_and_rules_are_valid(self) -> None:
        checks = validate_rule_pack()
        failures = [check for check in checks if not check.ok]
        self.assertEqual(failures, [], failures)

    def test_manifest_includes_triage_metadata(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        allowed_risk = {"low", "medium", "high"}
        allowed_priority = {"P1", "P2", "P3", "P4"}

        for detection in manifest["detections"]:
            with self.subTest(key=detection["key"]):
                self.assertIn(detection["risk"], allowed_risk)
                self.assertIn(detection["triage_priority"], allowed_priority)
                self.assertGreater(len(detection["severity_reason"]), 40)

    def test_every_primary_document_is_a_test_correlation(self) -> None:
        for path in RULES_DIR.glob("*.yml"):
            primary = load_rule_documents(path)[0]
            self.assertEqual(primary["status"], "test")
            self.assertIn("correlation", primary)
            self.assertTrue(primary["falsepositives"])


if __name__ == "__main__":
    unittest.main()
