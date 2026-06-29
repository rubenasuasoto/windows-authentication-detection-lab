from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from .oracle import evaluate_cases
from .paths import ARTIFACTS_DIR, ensure_output_directories
from .rules import validate_rule_pack


def run_validation() -> dict[str, Any]:
    ensure_output_directories()
    rule_checks = validate_rule_pack()
    case_results = evaluate_cases()
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "rules": [
            {
                "key": check.key,
                "file": check.file,
                "title": check.title,
                "ok": check.ok,
                "errors": list(check.errors),
                "document_count": check.document_count,
            }
            for check in rule_checks
        ],
        "cases": case_results,
        "summary": {
            "rules_total": len([check for check in rule_checks if check.key != "PACK"]),
            "rules_valid": len(
                [check for check in rule_checks if check.key != "PACK" and check.ok]
            ),
            "cases_total": len(case_results),
            "cases_passed": sum(result["status"] == "pass" for result in case_results),
            "cases_tuning": sum(result["disposition"] == "tune" for result in case_results),
        },
    }
    payload["ok"] = all(check.ok for check in rule_checks) and all(
        result["status"] == "pass" for result in case_results
    )
    (ARTIFACTS_DIR / "validation.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return payload
