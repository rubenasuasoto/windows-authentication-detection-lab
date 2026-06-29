from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES_DIR = ROOT / "rules"
FIXTURES_PATH = ROOT / "tests" / "fixtures" / "scenarios.json"
ARTIFACTS_DIR = ROOT / "artifacts"
REPORTS_DIR = ROOT / "reports" / "latest"
MANIFEST_PATH = RULES_DIR / "manifest.json"


def ensure_output_directories() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
