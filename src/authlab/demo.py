from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from .explain import format_narrative, playbook_path
from .oracle import evaluate_cases, load_cases
from .paths import REPORTS_DIR, ensure_output_directories
from .rules import load_manifest

SCOPE_NOTICE = (
    "Synthetic lab only. No production logs, credentials, malware, offensive "
    "simulations or host-changing actions."
)


def _narrative_parts(rule_id: str) -> dict[str, str]:
    labels = {
        "**What happened:**": "what_happened",
        "**Why it matters:**": "why_it_matters",
        "**What to check next:**": "what_to_check_next",
        "**Decision example:**": "decision_example",
    }
    parts = {value: "" for value in labels.values()}
    current: str | None = None
    for raw_line in format_narrative(rule_id).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        matched_label = next((label for label in labels if line.startswith(label)), None)
        if matched_label:
            current = labels[matched_label]
            parts[current] = line.removeprefix(matched_label).strip()
        elif current:
            parts[current] = f"{parts[current]} {line}".strip()
    return parts


def _relative_from_demo(path: str) -> str:
    return f"../../{path}"


def _demo_payload() -> dict[str, Any]:
    manifest = load_manifest()
    result_by_case = {result["case_id"]: result for result in evaluate_cases()}
    detections = {}
    for detection in manifest["detections"]:
        rule_id = detection["key"]
        detections[rule_id] = {
            "key": rule_id,
            "title": detection["title"],
            "events": detection["event_ids"],
            "attack": detection["attack"],
            "threshold": detection["threshold"],
            "risk": detection["risk"],
            "triage_priority": detection["triage_priority"],
            "severity_reason": detection["severity_reason"],
            "tuning": detection["tuning"],
            "playbook": playbook_path(rule_id),
            "playbook_href": _relative_from_demo(playbook_path(rule_id)),
            "narrative": _narrative_parts(rule_id),
        }

    cases = []
    for case in load_cases():
        result = result_by_case[case["case_id"]]
        cases.append(
            {
                "case_id": case["case_id"],
                "rule_id": case["rule_id"],
                "category": case["category"],
                "expected": result["expected"],
                "observed": result["observed"],
                "status": result["status"],
                "disposition": result["disposition"],
                "matched_fields": result["matched_fields"],
                "matched_event_count": result["matched_event_count"],
                "note": result["note"],
                "events": sorted(case["events"], key=lambda event: str(event["Timestamp"])),
            }
        )

    summary = {
        "rules": len(detections),
        "cases": len(cases),
        "expected_alerts": sum(1 for case in cases if case["expected"]),
        "tuning_cases": sum(1 for case in cases if case["disposition"] == "tune"),
        "passing_cases": sum(1 for case in cases if case["status"] == "pass"),
    }
    summary["pass_rate"] = round(summary["passing_cases"] / summary["cases"] * 100)
    return {
        "scope_notice": SCOPE_NOTICE,
        "summary": summary,
        "detections": detections,
        "cases": cases,
    }


def _json_script(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def _html(payload: dict[str, Any]) -> str:
    data = _json_script(payload)
    title = "Authentication Detection Mini-SOC"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg:#111417; --panel:#1b2026; --panel2:#242a31; --ink:#f3f6f8;
      --muted:#aab4bf; --line:#3a434d; --accent:#52c7b8; --blue:#8bbcff;
      --amber:#f5c56f; --red:#ff8f86; --green:#79d69e; --violet:#b9a4ff;
    }}
    * {{ box-sizing:border-box; }}
    body {{
      margin:0; background:var(--bg); color:var(--ink);
      font:14px/1.45 "Segoe UI",Arial,sans-serif;
    }}
    header {{
      padding:26px max(20px,calc((100vw - 1220px)/2)); border-bottom:1px solid var(--line);
      background:#171b20;
    }}
    h1 {{ margin:0 0 6px; font-size:28px; letter-spacing:0; }}
    h2 {{ margin:0 0 12px; font-size:17px; letter-spacing:0; }}
    h3 {{ margin:0 0 8px; font-size:14px; letter-spacing:0; color:var(--muted); }}
    p {{ margin:0; color:var(--muted); }}
    code {{ color:var(--blue); }}
    main {{ max-width:1220px; margin:0 auto; padding:18px; display:grid; gap:14px; }}
    section {{ min-width:0; border:1px solid var(--line); background:var(--panel); border-radius:8px; padding:16px; }}
    a {{ color:var(--blue); text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
    button {{
      color:var(--ink); background:#101316; border:1px solid var(--line); border-radius:6px;
      padding:9px 11px; font:inherit; cursor:pointer;
    }}
    button:hover {{ border-color:var(--accent); }}
    .notice {{ margin-top:12px; color:#ffe7b0; border-left:3px solid var(--amber); padding-left:10px; }}
    .reviewer-path {{
      margin-top:12px; display:flex; flex-wrap:wrap; gap:8px; align-items:center;
      color:var(--muted);
    }}
    .reviewer-path strong {{ color:var(--ink); }}
    .metrics {{ display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:10px; }}
    .metric {{ background:var(--panel2); border:1px solid var(--line); border-radius:7px; padding:12px; min-height:76px; }}
    .metric strong {{ display:block; font-size:24px; color:var(--accent); }}
    .metric span {{ color:var(--muted); }}
    .controls {{ display:grid; grid-template-columns:1fr 1.4fr; gap:12px; align-items:end; }}
    label {{ display:block; color:var(--muted); font-size:12px; margin-bottom:5px; }}
    select {{
      width:100%; color:var(--ink); background:#101316; border:1px solid var(--line);
      border-radius:6px; padding:10px; font:inherit;
    }}
    .grid {{ display:grid; grid-template-columns:0.8fr 1.2fr; gap:14px; align-items:start; }}
    .stack {{ display:grid; gap:14px; }}
    .chips {{ display:flex; flex-wrap:wrap; gap:6px; margin-top:10px; }}
    .chip {{ border:1px solid var(--line); border-radius:999px; padding:4px 8px; color:var(--muted); background:#15191e; }}
    .chip.high,.chip.P1,.chip.fail {{ color:var(--red); }}
    .chip.medium,.chip.P2,.chip.P3,.chip.tune {{ color:var(--amber); }}
    .chip.pass,.chip.keep {{ color:var(--green); }}
    .kv {{ display:grid; grid-template-columns:130px 1fr; gap:8px; margin-top:10px; }}
    .kv span:nth-child(odd) {{ color:var(--muted); }}
    .table-wrap {{ overflow:auto; max-width:100%; }}
    table {{ width:100%; min-width:780px; border-collapse:collapse; }}
    th,td {{ border-bottom:1px solid var(--line); padding:9px; text-align:left; vertical-align:top; }}
    th {{ color:var(--muted); font-size:12px; }}
    td {{ font-family:Consolas,"Courier New",monospace; font-size:12px; }}
    .narrative {{ display:grid; gap:10px; }}
    .narrative div {{ border-left:2px solid var(--violet); padding-left:10px; }}
    .narrative strong {{ display:block; margin-bottom:2px; }}
    .route {{ color:var(--blue); overflow-wrap:anywhere; }}
    .actions {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }}
    @media (max-width:860px) {{
      .metrics,.controls,.grid {{ grid-template-columns:minmax(0,1fr); }}
      h1 {{ font-size:23px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(title)}</h1>
    <p>Guided, local-only walkthrough for synthetic Windows authentication detections.</p>
    <p class="notice">{html.escape(SCOPE_NOTICE)}</p>
    <div class="reviewer-path">
      <strong>For reviewers: 3-minute guided path</strong>
      <span>Start with AUTH-003-POS, inspect the matched fields, open the playbook, then compare with the validation report.</span>
    </div>
  </header>
  <main>
    <section class="metrics" aria-label="Demo metrics">
      <div class="metric"><strong id="rulesMetric"></strong><span>Detections</span></div>
      <div class="metric"><strong id="casesMetric"></strong><span>Synthetic cases</span></div>
      <div class="metric"><strong id="alertsMetric"></strong><span>Expected alerts</span></div>
      <div class="metric"><strong id="tuneMetric"></strong><span>Tuning cases</span></div>
      <div class="metric"><strong id="passMetric"></strong><span>Pass rate</span></div>
    </section>
    <section class="controls" aria-label="Scenario controls">
      <div>
        <label for="ruleSelect">Detection</label>
        <select id="ruleSelect"></select>
      </div>
      <div>
        <label for="caseSelect">Scenario</label>
        <select id="caseSelect"></select>
      </div>
    </section>
    <div class="grid">
      <section>
        <h2 id="caseTitle"></h2>
        <p id="caseNote"></p>
        <div class="chips" id="caseChips"></div>
        <div class="kv">
          <span>Threshold</span><span id="threshold"></span>
          <span>Severity reason</span><span id="severity"></span>
          <span>Matched fields</span><span id="fields"></span>
          <span>Playbook</span><a class="route" id="playbook" href="#"></a>
        </div>
        <div class="actions">
          <button type="button" id="previousCase">Previous case</button>
          <button type="button" id="nextCase">Next case</button>
          <a class="route" href="report.en.html">Open validation report</a>
          <a class="route" href="../../README.md">Open README</a>
        </div>
      </section>
      <section>
        <h2>Analyst narrative</h2>
        <div class="narrative" id="narrative"></div>
      </section>
    </div>
    <section>
      <h2>Event timeline</h2>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Timestamp</th><th>EventID</th><th>User</th><th>Source</th>
              <th>Computer</th><th>Logon</th><th>Fields</th>
            </tr>
          </thead>
          <tbody id="eventsBody"></tbody>
        </table>
      </div>
    </section>
  </main>
  <script id="demo-data" type="application/json">{data}</script>
  <script>
    const data = JSON.parse(document.getElementById('demo-data').textContent);
    const els = {{
      rulesMetric: document.getElementById('rulesMetric'),
      casesMetric: document.getElementById('casesMetric'),
      alertsMetric: document.getElementById('alertsMetric'),
      tuneMetric: document.getElementById('tuneMetric'),
      passMetric: document.getElementById('passMetric'),
      ruleSelect: document.getElementById('ruleSelect'),
      caseSelect: document.getElementById('caseSelect'),
      caseTitle: document.getElementById('caseTitle'),
      caseNote: document.getElementById('caseNote'),
      caseChips: document.getElementById('caseChips'),
      threshold: document.getElementById('threshold'),
      severity: document.getElementById('severity'),
      fields: document.getElementById('fields'),
      playbook: document.getElementById('playbook'),
      previousCase: document.getElementById('previousCase'),
      nextCase: document.getElementById('nextCase'),
      narrative: document.getElementById('narrative'),
      eventsBody: document.getElementById('eventsBody')
    }};

    function text(value) {{
      return value === undefined || value === null || value === '' ? '-' : String(value);
    }}

    function setText(node, value) {{
      node.textContent = text(value);
    }}

    function chip(value) {{
      const span = document.createElement('span');
      span.className = 'chip ' + text(value).replace(/[^a-zA-Z0-9_-]/g, '');
      span.textContent = text(value);
      return span;
    }}

    function eventUser(event) {{
      return event.TargetUserName || event.SubjectUserName || '-';
    }}

    function eventSource(event) {{
      return event.IpAddress || event.CallerComputerName || '-';
    }}

    function eventLogon(event) {{
      return event.TargetLogonId || event.SubjectLogonId || event.LogonType || '-';
    }}

    function renderRuleOptions() {{
      Object.values(data.detections).forEach((detection) => {{
        const option = document.createElement('option');
        option.value = detection.key;
        option.textContent = detection.key + ' - ' + detection.title;
        els.ruleSelect.appendChild(option);
      }});
    }}

    function renderCaseOptions() {{
      const ruleId = els.ruleSelect.value;
      els.caseSelect.replaceChildren();
      data.cases.filter((item) => item.rule_id === ruleId).forEach((item) => {{
        const option = document.createElement('option');
        option.value = item.case_id;
        option.textContent = item.case_id + ' | ' + item.category;
        els.caseSelect.appendChild(option);
      }});
    }}

    function selectedCaseIndex() {{
      return data.cases.findIndex((item) => item.case_id === els.caseSelect.value);
    }}

    function selectCaseByIndex(index) {{
      const total = data.cases.length;
      const normalized = (index + total) % total;
      const selected = data.cases[normalized];
      els.ruleSelect.value = selected.rule_id;
      renderCaseOptions();
      els.caseSelect.value = selected.case_id;
      renderCase();
    }}

    function renderNarrative(detection) {{
      const labels = [
        ['What happened', detection.narrative.what_happened],
        ['Why it matters', detection.narrative.why_it_matters],
        ['What to check next', detection.narrative.what_to_check_next],
        ['Decision example', detection.narrative.decision_example]
      ];
      els.narrative.replaceChildren();
      labels.forEach(([label, value]) => {{
        const block = document.createElement('div');
        const strong = document.createElement('strong');
        const p = document.createElement('p');
        strong.textContent = label;
        p.textContent = value;
        block.append(strong, p);
        els.narrative.appendChild(block);
      }});
    }}

    function renderEvents(events) {{
      els.eventsBody.replaceChildren();
      events.forEach((event) => {{
        const row = document.createElement('tr');
        const extra = Object.keys(event)
          .filter((key) => !['Timestamp','EventID','TargetUserName','SubjectUserName','IpAddress','CallerComputerName','Computer','TargetLogonId','SubjectLogonId','LogonType'].includes(key))
          .map((key) => key + '=' + text(event[key]))
          .join('; ');
        [event.Timestamp, event.EventID, eventUser(event), eventSource(event), event.Computer, eventLogon(event), extra || '-'].forEach((value) => {{
          const cell = document.createElement('td');
          cell.textContent = text(value);
          row.appendChild(cell);
        }});
        els.eventsBody.appendChild(row);
      }});
    }}

    function renderCase() {{
      const selected = data.cases.find((item) => item.case_id === els.caseSelect.value);
      const detection = data.detections[selected.rule_id];
      setText(els.caseTitle, selected.case_id + ' - ' + detection.title);
      setText(els.caseNote, selected.note);
      els.caseChips.replaceChildren(
        chip(selected.category),
        chip('expected: ' + selected.expected),
        chip('observed: ' + selected.observed),
        chip(selected.status),
        chip(selected.disposition),
        chip(detection.risk),
        chip(detection.triage_priority)
      );
      setText(els.threshold, detection.threshold);
      setText(els.severity, detection.severity_reason);
      setText(els.fields, selected.matched_fields.join(', '));
      setText(els.playbook, detection.playbook);
      els.playbook.href = detection.playbook_href;
      renderNarrative(detection);
      renderEvents(selected.events);
    }}

    els.rulesMetric.textContent = data.summary.rules;
    els.casesMetric.textContent = data.summary.cases;
    els.alertsMetric.textContent = data.summary.expected_alerts;
    els.tuneMetric.textContent = data.summary.tuning_cases;
    els.passMetric.textContent = data.summary.pass_rate + '%';
    renderRuleOptions();
    els.ruleSelect.value = 'AUTH-003';
    renderCaseOptions();
    els.caseSelect.value = 'AUTH-003-POS';
    renderCase();
    els.ruleSelect.addEventListener('change', () => {{
      renderCaseOptions();
      renderCase();
    }});
    els.caseSelect.addEventListener('change', renderCase);
    els.previousCase.addEventListener('click', () => selectCaseByIndex(selectedCaseIndex() - 1));
    els.nextCase.addEventListener('click', () => selectCaseByIndex(selectedCaseIndex() + 1));
  </script>
</body>
</html>
"""


def build_demo() -> Path:
    ensure_output_directories()
    output = REPORTS_DIR / "demo.html"
    output.write_text(_html(_demo_payload()), encoding="utf-8")
    return output
