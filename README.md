# Windows Authentication Detection Lab

[Versión en español](README.es.md)

A safe, reproducible detection-engineering portfolio project built around five
Sigma detections for Windows authentication anomalies. The lab validates rule
structure, exercises synthetic scenarios, converts supported rules to Splunk
SPL, and publishes a bilingual validation report.

> Lab-only and defensive. No real credentials, production logs, malware,
> binaries, memory access or offensive simulations are included.

## What this demonstrates

- Sigma rule and correlation design.
- Positive, negative, boundary and tuning-oriented tests.
- Transparent handling of false positives and backend limitations.
- Reproducible validation and reporting through CI.
- ATT&CK-aligned detection reasoning without unsafe activity.

## Detection pack

| ID | Detection | Windows events | Focus |
|---|---|---|---|
| AUTH-001 | Failed logon burst from one source | 4625 | Password guessing |
| AUTH-002 | Failed logons across multiple accounts | 4625 | Password spraying |
| AUTH-003 | Successful logon after repeated failures | 4625, 4624 | Authentication sequence |
| AUTH-004 | Account lockout burst | 4740 | Operational anomaly |
| AUTH-005 | Remote logon followed by special privileges | 4624, 4672 | Privileged session |

## Quick start

Requirements: Python 3.12 and [uv](https://docs.astral.sh/uv/).

```powershell
uv sync --extra dev
uv run authlab all
uv run pytest
```

Open `reports/latest/report.en.html` after the run. Generated Splunk queries and
machine-readable evidence are written to `artifacts/`, which is intentionally
ignored by Git.

## Commands

```text
authlab validate                 Validate rules and execute safe fixtures
authlab convert --backend splunk Convert supported rules to Splunk SPL
authlab report                   Build English and Spanish reports
authlab audit                    Reject unsafe or private artifacts
authlab all                      Run audit, validation, conversion and reports
```

## Important limitation

The fixture runner is an educational test oracle, not a SIEM. Correlation
support differs between Sigma backends. Conversion output must be reviewed and
tested in an authorized target environment before operational use.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Data sources](docs/DATA_SOURCES.md)
- [Validation and tuning](docs/VALIDATION.md)
- [Security policy](SECURITY.md)

Licensed under the [MIT License](LICENSE).

