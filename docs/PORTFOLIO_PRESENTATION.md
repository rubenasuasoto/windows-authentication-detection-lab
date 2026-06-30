# Portfolio presentation guide

Use this page as a concise speaking guide for GitHub, LinkedIn or interviews.
It explains what the project proves without overstating operational coverage.

## One-minute summary

This lab builds and validates five Sigma detections for Windows authentication
anomalies. It uses only synthetic JSON events, documentation IP ranges and
fictional users. The value is not just the rules: it shows a repeatable
detection-engineering workflow with validation cases, tuning notes, backend
conversion, an interactive local demo, reports and safety checks.

## What to show first

1. `reports/latest/demo.html`: a guided local mini-SOC walkthrough over
   synthetic scenarios.
2. `rules/`: five readable Sigma detections with ATT&CK mapping and tuning
   notes.
3. `tests/fixtures/scenarios.json`: positive, negative, boundary and tuning
   cases.
4. `reports/latest/report.en.html`: the generated validation matrix.
5. `docs/ALERT_NARRATIVES.md`: examples of analyst-facing alert summaries.
6. `.github/workflows/validate.yml`: CI that runs linting, tests, conversion,
   reporting, secret scanning and dependency audit.

## Interview talking points

- I separated detection intent from validation evidence so each rule has a
  clear expected outcome.
- I documented backend limitations instead of hiding them. Two correlation
  rules produce reviewed compatibility SPL because the installed Splunk backend
  does not convert `temporal_ordered` correlations natively.
- I treated false positives as tuning cases. The matrix keeps them visible
  instead of pretending every scenario is a perfect alert.
- I wrote analyst-facing narratives so the detections can be explained as
  observable facts, impact and next steps.
- I added a local mini-SOC demo so reviewers can select a scenario, inspect
  synthetic Windows events and see why the rule alerts or stays quiet.
- I kept the lab safe for publication: no EVTX files, credentials, binaries,
  memory access, production paths or offensive simulations.

## Resume bullets

- Built a defensive Windows authentication detection lab with five Sigma rules,
  synthetic validation fixtures, a local mini-SOC demo, Splunk conversion and
  bilingual reporting.
- Validated detection logic with positive, negative, boundary and tuning cases,
  documenting backend limitations and false-positive handling.
- Added CI quality gates for tests, linting, secret scanning, dependency audit,
  report freshness and repository safety.

## What this project does not claim

- It is not a production SIEM deployment.
- It does not measure organization-specific precision or recall.
- It does not include real logs, credentials, malware samples or offensive
  procedures.
- It keeps Sigma rule status as `test` until validation in an authorized
  environment is completed.
