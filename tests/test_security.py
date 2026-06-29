import unittest

from authlab.audit import audit_repository
from authlab.paths import ROOT


class SecurityAuditTests(unittest.TestCase):
    def test_repository_passes_defensive_content_audit(self) -> None:
        self.assertEqual(audit_repository(), [])

    def test_auditor_rejects_sensitive_extensions(self) -> None:
        test_root = ROOT / ".audit-test"
        test_root.mkdir(exist_ok=True)
        unsafe = test_root / "sample.evtx"
        try:
            unsafe.write_bytes(b"synthetic")
            findings = audit_repository(test_root)
            self.assertTrue(any("forbidden" in finding for finding in findings))
        finally:
            unsafe.unlink(missing_ok=True)
            test_root.rmdir()

    def test_fixture_file_contains_no_real_user_paths(self) -> None:
        fixture = (ROOT / "tests" / "fixtures" / "scenarios.json").read_text(encoding="utf-8")
        self.assertNotIn("C:\\Users\\", fixture)


if __name__ == "__main__":
    unittest.main()
