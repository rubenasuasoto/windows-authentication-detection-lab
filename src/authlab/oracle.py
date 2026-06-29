from __future__ import annotations

import json
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .paths import FIXTURES_PATH

Event = dict[str, Any]
Observation = tuple[bool, list[str], int]


def _timestamp(event: Event) -> datetime:
    return datetime.fromisoformat(str(event["Timestamp"]).replace("Z", "+00:00"))


def _events(case: dict[str, Any], event_id: int) -> list[Event]:
    return sorted(
        (event for event in case["events"] if int(event.get("EventID", 0)) == event_id),
        key=_timestamp,
    )


def _valid_source(event: Event) -> bool:
    return str(event.get("IpAddress", "")) not in {"", "-", "127.0.0.1", "::1"}


def _grouped_window(
    events: list[Event],
    key: Callable[[Event], tuple[object, ...]],
    minutes: int,
    qualifies: Callable[[list[Event]], bool],
) -> list[Event]:
    for index, first in enumerate(events):
        end = _timestamp(first) + timedelta(minutes=minutes)
        grouped = [
            event
            for event in events[index:]
            if _timestamp(event) <= end and key(event) == key(first)
        ]
        if qualifies(grouped):
            return grouped
    return []


def _auth_001(case: dict[str, Any]) -> Observation:
    events = [event for event in _events(case, 4625) if _valid_source(event)]
    matched = _grouped_window(
        events,
        lambda event: (event.get("IpAddress"), event.get("Computer")),
        5,
        lambda group: len(group) >= 5,
    )
    return bool(matched), ["EventID", "IpAddress", "Computer"], len(matched)


def _auth_002(case: dict[str, Any]) -> Observation:
    events = [event for event in _events(case, 4625) if _valid_source(event)]
    matched = _grouped_window(
        events,
        lambda event: (event.get("IpAddress"), event.get("Computer")),
        10,
        lambda group: len({event.get("TargetUserName") for event in group}) >= 4,
    )
    return bool(matched), ["EventID", "TargetUserName", "IpAddress", "Computer"], len(matched)


def _auth_003(case: dict[str, Any]) -> Observation:
    failures = _events(case, 4625)
    for success in _events(case, 4624):
        success_time = _timestamp(success)
        start = success_time - timedelta(minutes=10)
        matched = [
            event
            for event in failures
            if start <= _timestamp(event) <= success_time
            and event.get("TargetUserName") == success.get("TargetUserName")
            and event.get("IpAddress") == success.get("IpAddress")
            and event.get("Computer") == success.get("Computer")
        ]
        if len(matched) >= 3:
            return True, ["EventID", "TargetUserName", "IpAddress", "Computer"], len(matched) + 1
    return False, ["EventID", "TargetUserName", "IpAddress", "Computer"], 0


def _auth_004(case: dict[str, Any]) -> Observation:
    events = [
        event
        for event in _events(case, 4740)
        if not str(event.get("TargetUserName", "")).endswith("$")
    ]
    matched = _grouped_window(
        events,
        lambda event: (event.get("CallerComputerName"), event.get("Computer")),
        15,
        lambda group: len(group) >= 3,
    )
    return bool(matched), ["EventID", "CallerComputerName", "Computer"], len(matched)


def _auth_005(case: dict[str, Any]) -> Observation:
    privileged = _events(case, 4672)
    for logon in _events(case, 4624):
        if int(logon.get("LogonType", 0)) not in {3, 10}:
            continue
        start = _timestamp(logon)
        end = start + timedelta(minutes=2)
        matches = [
            event
            for event in privileged
            if start <= _timestamp(event) <= end
            and event.get("SubjectLogonId") == logon.get("TargetLogonId")
            and event.get("Computer") == logon.get("Computer")
        ]
        if matches:
            return True, ["EventID", "LogonType", "TargetLogonId", "SubjectLogonId", "Computer"], 2
    return False, ["EventID", "LogonType", "TargetLogonId", "SubjectLogonId", "Computer"], 0


EVALUATORS: dict[str, Callable[[dict[str, Any]], Observation]] = {
    "AUTH-001": _auth_001,
    "AUTH-002": _auth_002,
    "AUTH-003": _auth_003,
    "AUTH-004": _auth_004,
    "AUTH-005": _auth_005,
}


def load_cases(path: Path = FIXTURES_PATH) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["cases"]


def evaluate_cases(path: Path = FIXTURES_PATH) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for case in load_cases(path):
        observed, fields, event_count = EVALUATORS[case["rule_id"]](case)
        expected = bool(case["expected_alert"])
        results.append(
            {
                "case_id": case["case_id"],
                "rule_id": case["rule_id"],
                "category": case["category"],
                "expected": expected,
                "observed": observed,
                "status": "pass" if expected == observed else "fail",
                "disposition": case.get("disposition", "keep"),
                "matched_fields": fields,
                "matched_event_count": event_count,
                "note": case["note"],
            }
        )
    return results

