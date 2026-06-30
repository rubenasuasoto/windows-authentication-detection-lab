from __future__ import annotations

import csv
import hashlib
import html
import json
from io import StringIO
from pathlib import Path
from typing import Any

from .paths import ARTIFACTS_DIR, MANIFEST_PATH, REPORTS_DIR, ensure_output_directories
from .rules import load_manifest


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _fingerprint() -> str:
    digest = hashlib.sha256()
    for path in sorted(MANIFEST_PATH.parent.glob("*")):
        if path.is_file():
            digest.update(path.name.encode())
            digest.update(path.read_text(encoding="utf-8").encode("utf-8"))
    return digest.hexdigest()[:12]


def _matrix_csv(cases: list[dict[str, Any]]) -> str:
    output = StringIO(newline="")
    fields = [
        "case_id",
        "rule_id",
        "category",
        "expected",
        "observed",
        "status",
        "disposition",
        "matched_event_count",
        "matched_fields",
        "note",
    ]
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for case in cases:
        row = dict(case)
        row["matched_fields"] = ";".join(case["matched_fields"])
        writer.writerow({field: row[field] for field in fields})
    return output.getvalue()


def _markdown(
    language: str,
    manifest: dict[str, Any],
    validation: dict[str, Any],
    conversions: list[dict[str, Any]],
    fingerprint: str,
) -> str:
    spanish = language == "es"
    title = "Informe de validación" if spanish else "Validation report"
    intro = (
        "Laboratorio defensivo con eventos sintéticos. Este informe no acredita rendimiento en producción."
        if spanish
        else "Defensive lab using synthetic events. This report does not claim production performance."
    )
    summary = validation["summary"]
    lines = [
        f"# {title}",
        "",
        intro,
        "",
        f"**Pack fingerprint:** `{fingerprint}`",
        "",
        "## Resumen" if spanish else "## Summary",
        "",
        f"- {'Reglas válidas' if spanish else 'Valid rules'}: {summary['rules_valid']}/{summary['rules_total']}",
        f"- {'Casos superados' if spanish else 'Passing cases'}: {summary['cases_passed']}/{summary['cases_total']}",
        f"- {'Casos marcados para ajuste' if spanish else 'Cases marked for tuning'}: {summary['cases_tuning']}",
        f"- {'Conversiones SPL correctas' if spanish else 'Successful SPL conversions'}: {sum(item['ok'] for item in conversions)}/{len(conversions)}",
        "",
        "## Detecciones" if spanish else "## Detections",
        "",
        "| ID | Title | Risk | Priority | Events | Threshold | ATT&CK |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in manifest["detections"]:
        lines.append(
            f"| {item['key']} | {item['title']} | {item['risk']} | "
            f"{item['triage_priority']} | {', '.join(map(str, item['event_ids']))} | "
            f"{item['threshold']} | {', '.join(item['attack']) or 'Operational'} |"
        )
    lines.extend(
        [
            "",
            "## Matriz de validación" if spanish else "## Validation matrix",
            "",
            "| Case | Rule | Category | Expected | Observed | Result | Disposition |",
            "|---|---|---|---:|---:|---|---|",
        ]
    )
    for case in validation["cases"]:
        lines.append(
            f"| {case['case_id']} | {case['rule_id']} | {case['category']} | "
            f"{str(case['expected']).lower()} | {str(case['observed']).lower()} | "
            f"{case['status']} | {case['disposition']} |"
        )
    lines.extend(
        [
            "",
            "## Compatibilidad del backend" if spanish else "## Backend compatibility",
            "",
            *[
                f"- **{item['rule']}**: {item.get('mode', 'native')}"
                for item in conversions
            ],
            "",
            "## Notas de ajuste" if spanish else "## Tuning notes",
            "",
        ]
    )
    for item in manifest["detections"]:
        lines.append(
            f"- **{item['key']}** ({item['risk']}/{item['triage_priority']}): "
            f"{item['severity_reason']} Tuning: {item['tuning']}"
        )
    lines.extend(
        [
            "",
            "## Limitaciones" if spanish else "## Limitations",
            "",
            (
                "El runner es un oráculo educativo y no un SIEM. Las consultas generadas requieren revisión y pruebas autorizadas."
                if spanish
                else "The runner is an educational oracle, not a SIEM. Generated queries require review and authorized testing."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def _html_report(
    language: str,
    manifest: dict[str, Any],
    validation: dict[str, Any],
    conversions: list[dict[str, Any]],
    fingerprint: str,
) -> str:
    spanish = language == "es"
    summary = validation["summary"]
    labels = {
        "title": "Laboratorio de detección de autenticación" if spanish else "Authentication Detection Lab",
        "subtitle": "Ingeniería de detección reproducible con telemetría sintética de Windows" if spanish else "Reproducible detection engineering with synthetic Windows telemetry",
        "rules": "Reglas válidas" if spanish else "Valid rules",
        "cases": "Pruebas superadas" if spanish else "Passing tests",
        "tuning": "Casos para tuning" if spanish else "Tuning cases",
        "spl": "Conversiones SPL" if spanish else "SPL conversions",
        "pack": "Pack de detección" if spanish else "Detection pack",
        "matrix": "Matriz de validación" if spanish else "Validation matrix",
        "limitations": "Alcance y limitaciones" if spanish else "Scope and limitations",
    }
    detection_cards = "".join(
        f"""
        <article class="detection">
          <div class="detection-head"><span>{html.escape(item['key'])}</span><strong>{html.escape(item['title'])}</strong></div>
          <p>{html.escape(item['threshold'])}</p>
          <div class="chips"><span>{html.escape(item['risk'])}</span><span>{html.escape(item['triage_priority'])}</span><span>Events {', '.join(map(str, item['event_ids']))}</span><span>{html.escape(', '.join(item['attack']) or 'Operational')}</span></div>
          <small>{html.escape(item['severity_reason'])} Tuning: {html.escape(item['tuning'])}</small>
        </article>
        """
        for item in manifest["detections"]
    )
    rows = "".join(
        f"""
        <tr>
          <td><strong>{html.escape(case['case_id'])}</strong><small>{html.escape(case['note'])}</small></td>
          <td>{html.escape(case['rule_id'])}</td>
          <td>{html.escape(case['category'])}</td>
          <td>{str(case['expected']).lower()}</td>
          <td>{str(case['observed']).lower()}</td>
          <td><span class="status {html.escape(case['status'])}">{html.escape(case['status'])}</span></td>
          <td><span class="status {html.escape(case['disposition'])}">{html.escape(case['disposition'])}</span></td>
        </tr>
        """
        for case in validation["cases"]
    )
    language_link = "report.en.html" if spanish else "report.es.html"
    language_label = "English" if spanish else "Español"
    compatibility_count = sum(item.get("mode") == "compatibility" for item in conversions)
    limitation = (
        f"El runner usa eventos sintéticos y no sustituye a un SIEM. "
        f"{compatibility_count} correlaciones usan SPL de compatibilidad revisado."
        if spanish
        else f"The runner uses synthetic events and does not replace a SIEM. "
        f"{compatibility_count} correlations use reviewed compatibility SPL."
    )
    return f"""<!doctype html>
<html lang="{language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{labels['title']}</title>
  <style>
    :root {{ --bg:#0d1513; --panel:#16211e; --panel2:#101916; --ink:#eef8f4; --muted:#a8bab2; --line:#344740; --green:#65d6a7; --blue:#78b7ff; --amber:#ffd27a; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; overflow-x:hidden; background:var(--bg); color:var(--ink); font:15px/1.5 "Segoe UI",Arial,sans-serif; }}
    header {{ border-bottom:1px solid var(--line); padding:30px max(24px,calc((100vw - 1180px)/2)); background:var(--panel2); }}
    header div {{ display:flex; align-items:flex-start; justify-content:space-between; gap:20px; }}
    h1 {{ margin:0; font-size:30px; letter-spacing:0; }} h2 {{ margin:0 0 14px; font-size:18px; }}
    p {{ color:var(--muted); }} a {{ color:var(--green); }}
    main {{ min-width:0; max-width:1180px; margin:0 auto; padding:24px; display:grid; gap:18px; }}
    section {{ min-width:0; border:1px solid var(--line); background:var(--panel); border-radius:8px; padding:18px; }}
    .fingerprint {{ font:12px Consolas,monospace; color:var(--muted); }}
    .metrics {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; }}
    .metric {{ border:1px solid var(--line); background:var(--panel2); border-radius:7px; padding:14px; }}
    .metric strong {{ display:block; font-size:26px; color:var(--green); }} .metric span {{ color:var(--muted); }}
    .detections {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }}
    .detection {{ border:1px solid var(--line); background:var(--panel2); border-radius:7px; padding:14px; }}
    .detection-head {{ display:flex; gap:10px; align-items:center; }} .detection-head span {{ color:var(--blue); font:12px Consolas,monospace; }}
    .detection p {{ margin:8px 0; }} .detection small {{ display:block; color:var(--muted); margin-top:10px; }}
    .chips {{ display:flex; flex-wrap:wrap; gap:6px; }} .chips span {{ border:1px solid var(--line); padding:3px 7px; border-radius:999px; font-size:12px; color:var(--muted); }}
    .table-wrap {{ min-width:0; max-width:100%; overflow:auto; }} table {{ width:100%; border-collapse:collapse; min-width:850px; }} th,td {{ padding:10px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }} th {{ color:var(--muted); font-size:12px; }} td small {{ display:block; color:var(--muted); max-width:320px; }}
    .status {{ display:inline-block; padding:3px 7px; border-radius:999px; background:#26352f; }} .pass,.keep {{ color:var(--green); }} .fail {{ color:#ff9c91; }} .tune {{ color:var(--amber); }}
    .notice {{ border-left:3px solid var(--amber); padding-left:12px; color:var(--muted); }}
    @media (max-width:760px) {{ .metrics,.detections {{ grid-template-columns:minmax(0,1fr); }} h1 {{ font-size:24px; }} header div {{ display:block; }} header p {{ overflow-wrap:anywhere; }} }}
  </style>
</head>
<body>
  <header><div><div><h1>{labels['title']}</h1><p>{labels['subtitle']}</p><span class="fingerprint">pack {fingerprint}</span></div><a href="{language_link}">{language_label}</a></div></header>
  <main>
    <section class="metrics">
      <div class="metric"><strong>{summary['rules_valid']}/{summary['rules_total']}</strong><span>{labels['rules']}</span></div>
      <div class="metric"><strong>{summary['cases_passed']}/{summary['cases_total']}</strong><span>{labels['cases']}</span></div>
      <div class="metric"><strong>{summary['cases_tuning']}</strong><span>{labels['tuning']}</span></div>
      <div class="metric"><strong>{sum(item['ok'] for item in conversions)}/{len(conversions)}</strong><span>{labels['spl']}</span></div>
    </section>
    <section><h2>{labels['pack']}</h2><div class="detections">{detection_cards}</div></section>
    <section><h2>{labels['matrix']}</h2><div class="table-wrap"><table><thead><tr><th>Case</th><th>Rule</th><th>Category</th><th>Expected</th><th>Observed</th><th>Result</th><th>Decision</th></tr></thead><tbody>{rows}</tbody></table></div></section>
    <section><h2>{labels['limitations']}</h2><p class="notice">{limitation}</p></section>
  </main>
</body>
</html>
"""


def build_reports() -> list[Path]:
    ensure_output_directories()
    validation = _load_json(ARTIFACTS_DIR / "validation.json")
    conversions = _load_json(ARTIFACTS_DIR / "conversion.json")
    manifest = load_manifest()
    fingerprint = _fingerprint()
    outputs: list[Path] = []
    for language in ("en", "es"):
        markdown_path = REPORTS_DIR / f"report.{language}.md"
        html_path = REPORTS_DIR / f"report.{language}.html"
        markdown_path.write_text(
            _markdown(language, manifest, validation, conversions, fingerprint), encoding="utf-8"
        )
        html_path.write_text(
            _html_report(language, manifest, validation, conversions, fingerprint), encoding="utf-8"
        )
        outputs.extend((markdown_path, html_path))
    matrix_path = REPORTS_DIR / "validation-matrix.csv"
    matrix_path.write_text(_matrix_csv(validation["cases"]), encoding="utf-8")
    outputs.append(matrix_path)
    return outputs
