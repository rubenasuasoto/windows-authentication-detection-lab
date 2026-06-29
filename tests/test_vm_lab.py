import json
import unittest
from unittest.mock import patch

from authlab.paths import ARTIFACTS_DIR, ROOT
from authlab.vm_lab import build_readiness, inspect_vm_readiness, write_vm_readiness


class VMReadinessTests(unittest.TestCase):
    def test_hyper_v_is_preferred_when_available(self) -> None:
        readiness = build_readiness(
            "Windows",
            "Windows Pro",
            True,
            {"hyper_v": True, "virtualbox": True, "vmware": False},
        )
        self.assertTrue(readiness.ready)
        self.assertEqual(readiness.preferred_provider, "hyper_v")
        self.assertFalse(readiness.changes_applied)

    def test_missing_provider_requires_explicit_system_decision(self) -> None:
        readiness = build_readiness(
            "Windows",
            "Windows Pro",
            False,
            {"hyper_v": False, "virtualbox": False, "vmware": False},
        )
        self.assertFalse(readiness.ready)
        self.assertIn("explicit approval", readiness.next_step)

    def test_readiness_artifact_records_no_changes(self) -> None:
        readiness = build_readiness(
            "Windows",
            "Windows Pro",
            False,
            {"hyper_v": False, "virtualbox": False, "vmware": False},
        )
        payload = write_vm_readiness(readiness)
        self.assertTrue(payload["safety"]["read_only"])
        self.assertFalse(payload["safety"]["virtual_machines_created"])
        saved = json.loads((ARTIFACTS_DIR / "vm-readiness.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["preferred_provider"], None)

    @patch("authlab.vm_lab.shutil.which")
    @patch("authlab.vm_lab._powershell_value")
    @patch("authlab.vm_lab.platform.system", return_value="Windows")
    def test_powershell_false_is_not_treated_as_available(
        self,
        _system_mock,
        powershell_mock,
        which_mock,
    ) -> None:
        which_mock.return_value = None
        powershell_mock.side_effect = ["Windows 10 Pro", "False", "False"]
        readiness = inspect_vm_readiness()
        self.assertFalse(readiness.providers["hyper_v"])
        self.assertFalse(readiness.hypervisor_present)

    def test_public_evidence_template_forbids_raw_logs(self) -> None:
        template = json.loads(
            (ROOT / "docs" / "VM_EVIDENCE_TEMPLATE.json").read_text(encoding="utf-8")
        )
        self.assertFalse(template["evidence"]["raw_logs_committed"])
        self.assertTrue(template["evidence"]["identities_fictional"])


if __name__ == "__main__":
    unittest.main()
