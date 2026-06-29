from __future__ import annotations

import ipaddress
import re
from pathlib import Path

from .paths import ROOT

FORBIDDEN_EXTENSIONS = {".exe", ".dll", ".evtx", ".dmp", ".bin", ".pfx", ".p12"}
FORBIDDEN_NAMES = {".env", "storage_state.json", "credentials.json", "secrets.json"}
FORBIDDEN_TEXT = ("c:\\users\\",)
SKIP_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
TEXT_EXTENSIONS = {".md", ".py", ".toml", ".json", ".yml", ".yaml", ".txt", ".html", ".csv"}
IP_PATTERN = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")


def _allowed_ip(value: str) -> bool:
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return False
    documentation_ranges = (
        ipaddress.ip_network("192.0.2.0/24"),
        ipaddress.ip_network("198.51.100.0/24"),
        ipaddress.ip_network("203.0.113.0/24"),
    )
    return address.is_loopback or any(address in network for network in documentation_ranges)


def audit_repository(root: Path = ROOT) -> list[str]:
    findings: list[str] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in SKIP_PARTS for part in relative.parts):
            continue
        if not path.is_file():
            continue
        if path.name.lower() in FORBIDDEN_NAMES:
            findings.append(f"forbidden file name: {relative}")
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
            findings.append(f"forbidden binary or sensitive extension: {relative}")
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"text file is not UTF-8: {relative}")
            continue
        lowered = text.lower()
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in lowered:
                findings.append(
                    f"private or unrelated project reference in {relative}: {forbidden}"
                )
        for candidate in IP_PATTERN.findall(text):
            if not _allowed_ip(candidate):
                findings.append(f"non-documentation IPv4 address in {relative}: {candidate}")
    return sorted(set(findings))
