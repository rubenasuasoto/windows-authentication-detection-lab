from __future__ import annotations

from typing import Any

from .paths import ROOT
from .rules import load_manifest

NARRATIVES_PATH = "docs/ALERT_NARRATIVES.md"

PLAYBOOKS = {
    "AUTH-001": "docs/playbooks/AUTH-001_failed_logon_burst.md",
    "AUTH-002": "docs/playbooks/AUTH-002_multiple_accounts.md",
    "AUTH-003": "docs/playbooks/AUTH-003_success_after_failures.md",
    "AUTH-004": "docs/playbooks/AUTH-004_account_lockout_burst.md",
    "AUTH-005": "docs/playbooks/AUTH-005_privileged_remote_logon.md",
}


def detections() -> list[dict[str, Any]]:
    return list(load_manifest()["detections"])


def find_detection(rule_id: str) -> dict[str, Any]:
    normalized = rule_id.strip().upper()
    for detection in detections():
        if detection["key"] == normalized:
            return detection
    raise KeyError(f"Unknown detection id: {rule_id}")


def playbook_path(rule_id: str) -> str:
    return PLAYBOOKS[find_detection(rule_id)["key"]]


def playbook_exists(rule_id: str) -> bool:
    return (ROOT / playbook_path(rule_id)).is_file()


def format_playbook(rule_id: str) -> str:
    path = ROOT / playbook_path(rule_id)
    if not path.is_file():
        raise FileNotFoundError(f"Missing playbook for {rule_id}: {path}")
    return path.read_text(encoding="utf-8").strip()


def format_narrative(rule_id: str) -> str:
    detection = find_detection(rule_id)
    text = (ROOT / NARRATIVES_PATH).read_text(encoding="utf-8")
    marker = f"## {detection['key']} "
    start = text.find(marker)
    if start == -1:
        raise KeyError(f"Missing narrative for detection id: {rule_id}")
    next_start = text.find("\n## ", start + len(marker))
    section = text[start:] if next_start == -1 else text[start:next_start]
    return section.strip()


def format_rule_list() -> str:
    lines = ["Detection pack: Windows Authentication Anomalies", ""]
    for detection in detections():
        attacks = ", ".join(detection["attack"]) or "Operational anomaly"
        events = ", ".join(str(item) for item in detection["event_ids"])
        lines.append(f"{detection['key']}  {detection['title']}")
        lines.append(f"  events: {events} | attack: {attacks}")
        lines.append(
            f"  risk: {detection['risk']} | priority: {detection['triage_priority']}"
        )
        lines.append(f"  playbook: {playbook_path(detection['key'])}")
    return "\n".join(lines)


def format_detection(rule_id: str) -> str:
    detection = find_detection(rule_id)
    attacks = ", ".join(detection["attack"]) or "Operational anomaly"
    events = ", ".join(str(item) for item in detection["event_ids"])
    fields = ", ".join(detection["required_fields"])
    playbook = playbook_path(detection["key"])
    exists = "yes" if playbook_exists(detection["key"]) else "missing"
    return "\n".join(
        [
            f"{detection['key']} - {detection['title']}",
            "",
            f"Rule file: rules/{detection['file']}",
            f"Events: {events}",
            f"Required fields: {fields}",
            f"Threshold: {detection['threshold']}",
            f"ATT&CK: {attacks}",
            f"Risk: {detection['risk']}",
            f"Triage priority: {detection['triage_priority']}",
            f"Severity reason: {detection['severity_reason']}",
            f"Tuning: {detection['tuning']}",
            f"Playbook: {playbook} ({exists})",
            f"Narrative: {NARRATIVES_PATH}",
        ]
    )
