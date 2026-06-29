from __future__ import annotations

import argparse
import json

from .audit import audit_repository
from .convert import convert_rules
from .report import build_reports
from .validation import run_validation


def _audit() -> bool:
    findings = audit_repository()
    if findings:
        print("Repository audit failed:")
        for finding in findings:
            print(f"- {finding}")
        return False
    print("Repository audit: OK")
    return True


def _validate() -> bool:
    payload = run_validation()
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return bool(payload["ok"])


def _convert(backend: str) -> bool:
    results = convert_rules(backend)
    for result in results:
        status = "OK" if result["ok"] else "UNSUPPORTED"
        print(f"{status} ({result['mode']}) {result['rule']}: {result['message']}")
    return all(result["ok"] for result in results)


def _report() -> bool:
    outputs = build_reports()
    for output in outputs:
        print(f"Generated {output}")
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safe Windows authentication detection lab")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("audit", help="reject private or unsafe repository artifacts")
    subparsers.add_parser("validate", help="validate Sigma rules and synthetic fixtures")
    convert_parser = subparsers.add_parser("convert", help="convert rules to a reviewed backend")
    convert_parser.add_argument("--backend", default="splunk", choices=("splunk",))
    subparsers.add_parser("report", help="build bilingual portfolio reports")
    subparsers.add_parser("all", help="run audit, validation, conversion and reports")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "audit":
        return 0 if _audit() else 1
    if args.command == "validate":
        return 0 if _validate() else 1
    if args.command == "convert":
        return 0 if _convert(args.backend) else 1
    if args.command == "report":
        return 0 if _report() else 1

    audit_ok = _audit()
    validation_ok = _validate()
    conversion_ok = _convert("splunk")
    report_ok = _report()
    return 0 if all((audit_ok, validation_ok, conversion_ok, report_ok)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
