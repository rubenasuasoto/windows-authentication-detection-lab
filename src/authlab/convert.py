from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any

from .paths import ARTIFACTS_DIR, RULES_DIR, ensure_output_directories

SPLUNK_COMPATIBILITY = {
    "auth_003_success_after_failures": """index=* sourcetype=\"WinEventLog:Security\" (EventCode=4625 OR EventCode=4624)
| sort 0 TargetUserName IpAddress Computer _time
| streamstats time_window=10m count(eval(EventCode=4625)) AS failures latest(eval(if(EventCode=4625,_time,null()))) AS last_failure BY TargetUserName IpAddress Computer
| where EventCode=4624 AND failures>=3 AND last_failure<=_time
| table _time Computer TargetUserName IpAddress failures""",
    "auth_005_privileged_remote_logon": """index=* sourcetype=\"WinEventLog:Security\" (EventCode=4624 OR EventCode=4672)
| eval CorrelationLogonId=coalesce(TargetLogonId,SubjectLogonId)
| sort 0 Computer CorrelationLogonId _time
| streamstats time_window=2m latest(eval(if(EventCode=4624 AND (LogonType=3 OR LogonType=10),_time,null()))) AS remote_logon_time latest(eval(if(EventCode=4624,TargetUserName,null()))) AS remote_user BY Computer CorrelationLogonId
| where EventCode=4672 AND isnotnull(remote_logon_time) AND remote_logon_time<=_time
| table _time Computer CorrelationLogonId remote_user SubjectUserName""",
}


def convert_rules(backend: str = "splunk") -> list[dict[str, Any]]:
    if backend != "splunk":
        raise ValueError("The first release supports only the reviewed Splunk backend.")
    ensure_output_directories()
    executable = shutil.which("sigma")
    if not executable:
        raise RuntimeError("sigma-cli is not available. Run 'uv sync --extra dev'.")

    output_dir = ARTIFACTS_DIR / backend
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    for rule_path in sorted(RULES_DIR.glob("*.yml")):
        process = subprocess.run(
            [
                executable,
                "convert",
                "-t",
                backend,
                "-p",
                "splunk_windows",
                str(rule_path),
            ],
            cwd=RULES_DIR.parent,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        query = process.stdout.strip()
        mode = "native"
        message = process.stderr.strip() or ("converted" if query else "no query generated")
        if (
            process.returncode != 0
            and "temporal_ordered" in message
            and rule_path.stem in SPLUNK_COMPATIBILITY
        ):
            query = SPLUNK_COMPATIBILITY[rule_path.stem]
            mode = "compatibility"
            message = (
                "Reviewed SPL compatibility query: installed pySigma Splunk backend "
                "does not support temporal_ordered correlations."
            )
        output_path = output_dir / f"{rule_path.stem}.spl"
        ok = bool(query) and (process.returncode == 0 or mode == "compatibility")
        if ok:
            output_path.write_text(query + "\n", encoding="utf-8")
        elif output_path.exists():
            output_path.unlink()
        results.append(
            {
                "rule": rule_path.name,
                "backend": backend,
                "ok": ok,
                "mode": mode,
                "output": str(output_path.relative_to(RULES_DIR.parent)) if query else "",
                "message": message,
            }
        )
    (ARTIFACTS_DIR / "conversion.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return results
