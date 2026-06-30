from __future__ import annotations

import json
import platform
import shutil
import subprocess
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any

from .paths import ARTIFACTS_DIR, ensure_output_directories


@dataclass(frozen=True)
class VMReadiness:
    platform: str
    windows_edition: str
    hypervisor_present: bool
    providers: dict[str, bool]
    preferred_provider: str | None
    ready: bool
    next_step: str
    changes_applied: bool = False


def _powershell_value(script: str) -> str:
    executable = shutil.which("powershell")
    if not executable:
        return ""
    result = subprocess.run(
        [executable, "-NoProfile", "-NonInteractive", "-Command", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=15,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def build_readiness(
    system: str,
    windows_edition: str,
    hypervisor_present: bool,
    providers: dict[str, bool],
) -> VMReadiness:
    preferred = next(
        (provider for provider in ("hyper_v", "virtualbox", "vmware") if providers.get(provider)),
        None,
    )
    if system != "Windows":
        next_step = "Run this readiness check on the Windows host intended for the isolated lab."
    elif preferred:
        next_step = (
            f"Review the {preferred} network and snapshot plan before creating any virtual machine."
        )
    else:
        next_step = (
            "Choose and enable a reviewed hypervisor only after explicit approval; Hyper-V is "
            "preferred on compatible Windows Pro hosts."
        )
    return VMReadiness(
        platform=system,
        windows_edition=windows_edition,
        hypervisor_present=hypervisor_present,
        providers=providers,
        preferred_provider=preferred,
        ready=system == "Windows" and preferred is not None,
        next_step=next_step,
    )


def inspect_vm_readiness() -> VMReadiness:
    system = platform.system()
    edition = ""
    hypervisor_present = False
    providers = {
        "hyper_v": False,
        "virtualbox": shutil.which("VBoxManage") is not None,
        "vmware": shutil.which("vmrun") is not None,
    }
    if system == "Windows":
        edition = _powershell_value("(Get-CimInstance Win32_OperatingSystem).Caption")
        hypervisor_value = _powershell_value(
            "(Get-CimInstance Win32_ComputerSystem).HypervisorPresent"
        )
        hypervisor_present = hypervisor_value.lower() == "true"
        hyper_v_value = _powershell_value(
            "[bool](Get-Command Get-VM -ErrorAction SilentlyContinue)"
        )
        providers["hyper_v"] = hyper_v_value.lower() == "true"
    return build_readiness(system, edition, hypervisor_present, providers)


def write_vm_readiness(readiness: VMReadiness | None = None) -> dict[str, Any]:
    ensure_output_directories()
    current = readiness or inspect_vm_readiness()
    payload: dict[str, Any] = {
        "schema_version": 1,
        "checked_at": datetime.now(UTC).isoformat(),
        **asdict(current),
        "safety": {
            "read_only": True,
            "network_changes": False,
            "software_installed": False,
            "virtual_machines_created": False,
        },
    }
    (ARTIFACTS_DIR / "vm-readiness.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return payload


def format_vm_plan() -> str:
    return "\n".join(
        [
            "Optional isolated VM validation plan",
            "",
            "Scope",
            "- Read-only planning command; no Windows features, networks or VMs are changed.",
            "- Use disposable Windows evaluation systems with fictional identities only.",
            "- Keep raw EVTX exports and screenshots with private data out of the repository.",
            "",
            "VM-A: local authentication telemetry",
            "- Purpose: validate 4624, 4625 and 4672 field behavior with local accounts.",
            "- Candidate detections: AUTH-001, AUTH-002, AUTH-003 and part of AUTH-005.",
            "- Evidence to record: Windows edition/build, audit policy, normalized events, "
            "rule result, pass/tune decision.",
            "- Public evidence format: docs/VM_EVIDENCE_TEMPLATE.json with fictional users, "
            "hosts and documentation IP ranges.",
            "",
            "VM-B: optional domain lockout telemetry",
            "- Purpose: validate 4740 lockout fields only when a domain-style lab is approved.",
            "- Candidate detections: AUTH-004.",
            "- Evidence to record: caller computer field, affected account type, normalized "
            "lockout events, pass/tune decision.",
            "- Skip VM-B unless it can remain isolated and disposable.",
            "",
            "Exit criteria",
            "- Synthetic fixtures still pass with uv run authlab all.",
            "- Every tested rule has expected, observed and disposition recorded.",
            "- Any mismatch becomes a tuning note or a reviewed rule update.",
            "- No offensive tools, credential dumping tools, malware samples or production "
            "data are used.",
        ]
    )
