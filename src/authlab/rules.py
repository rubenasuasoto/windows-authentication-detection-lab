from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .paths import MANIFEST_PATH, RULES_DIR


@dataclass(frozen=True)
class RuleCheck:
    key: str
    file: str
    title: str
    ok: bool
    errors: tuple[str, ...]
    document_count: int


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_rule_documents(path: Path) -> list[dict[str, Any]]:
    return [
        document
        for document in yaml.safe_load_all(path.read_text(encoding="utf-8"))
        if document
    ]


def _valid_uuid(value: object) -> bool:
    try:
        uuid.UUID(str(value))
    except (ValueError, TypeError, AttributeError):
        return False
    return True


def _pysigma_check(path: Path) -> str | None:
    try:
        from sigma.collection import SigmaCollection

        SigmaCollection.load_ruleset([path])
    except Exception as exc:  # pySigma exceptions vary by parser version.
        return f"pySigma rejected the rule set: {exc}"
    return None


def validate_rule_pack() -> list[RuleCheck]:
    manifest = load_manifest()
    detections = manifest.get("detections", [])
    checks: list[RuleCheck] = []
    primary_ids: set[str] = set()

    for detection in detections:
        path = RULES_DIR / detection["file"]
        errors: list[str] = []
        documents: list[dict[str, Any]] = []
        for field in ("risk", "severity_reason", "triage_priority"):
            if not detection.get(field):
                errors.append(f"missing manifest field: {field}")
        if detection.get("risk") not in {"low", "medium", "high"}:
            errors.append("manifest risk must be low, medium or high")
        if detection.get("triage_priority") not in {"P1", "P2", "P3", "P4"}:
            errors.append("manifest triage_priority must be P1, P2, P3 or P4")
        if not path.is_file():
            errors.append("rule file is missing")
        else:
            try:
                documents = load_rule_documents(path)
            except yaml.YAMLError as exc:
                errors.append(f"invalid YAML: {exc}")

        primary = documents[0] if documents else {}
        required = (
            "title",
            "id",
            "status",
            "description",
            "author",
            "date",
            "falsepositives",
            "level",
        )
        for field in required:
            if not primary.get(field):
                errors.append(f"missing primary field: {field}")
        if primary.get("status") != "test":
            errors.append("primary status must remain 'test'")
        if not _valid_uuid(primary.get("id")):
            errors.append("primary id is not a UUID")
        elif str(primary["id"]) in primary_ids:
            errors.append("primary id is duplicated")
        else:
            primary_ids.add(str(primary.get("id")))
        if "correlation" not in primary:
            errors.append("primary document must be a Sigma correlation")
        if primary.get("title") != detection.get("title"):
            errors.append("manifest title and rule title differ")
        if path.is_file() and not errors:
            pysigma_error = _pysigma_check(path)
            if pysigma_error:
                errors.append(pysigma_error)

        checks.append(
            RuleCheck(
                key=detection["key"],
                file=detection["file"],
                title=detection["title"],
                ok=not errors,
                errors=tuple(errors),
                document_count=len(documents),
            )
        )

    rule_files = {path.name for path in RULES_DIR.glob("*.yml")}
    manifest_files = {item["file"] for item in detections}
    if len(detections) != 5 or rule_files != manifest_files:
        checks.append(
            RuleCheck(
                key="PACK",
                file="rules/",
                title="Exactly five primary detections",
                ok=False,
                errors=(
                    "manifest and rule directory must contain exactly the same five rule files",
                ),
                document_count=0,
            )
        )
    return checks
