# Validation report

Defensive lab using synthetic events. This report does not claim production performance.

**Pack fingerprint:** `22bc77ef0e20`

## Summary

- Valid rules: 5/5
- Passing cases: 17/17
- Cases marked for tuning: 2
- Successful SPL conversions: 5/5

## Detections

| ID | Title | Risk | Priority | Events | Threshold | ATT&CK |
|---|---|---|---|---|---|---|
| AUTH-001 | Failed Logon Burst From One Source | medium | P3 | 4625 | 5 events in 5 minutes per source and computer | T1110.001 |
| AUTH-002 | Failed Logons Across Multiple Accounts | medium | P2 | 4625 | 4 distinct users in 10 minutes per source and computer | T1110.003 |
| AUTH-003 | Successful Logon After Repeated Failures | high | P1 | 4625, 4624 | 3 failures followed by success in 10 minutes for the same user and source | T1078 |
| AUTH-004 | Account Lockout Burst | medium | P3 | 4740 | 3 lockouts in 15 minutes per caller and computer | Operational |
| AUTH-005 | Remote Logon Followed By Special Privileges | high | P1 | 4624, 4672 | Remote or network logon followed by privileges in 2 minutes for the same logon ID | T1078 |

## Validation matrix

| Case | Rule | Category | Expected | Observed | Result | Disposition |
|---|---|---|---:|---:|---|---|
| AUTH-001-POS | AUTH-001 | positive | true | true | pass | keep |
| AUTH-001-NEG | AUTH-001 | negative | false | false | pass | keep |
| AUTH-001-BOUNDARY | AUTH-001 | boundary | false | false | pass | keep |
| AUTH-002-POS | AUTH-002 | positive | true | true | pass | keep |
| AUTH-002-NEG | AUTH-002 | negative | false | false | pass | keep |
| AUTH-002-BOUNDARY | AUTH-002 | boundary | false | false | pass | keep |
| AUTH-003-POS | AUTH-003 | positive | true | true | pass | keep |
| AUTH-003-NEG | AUTH-003 | negative | false | false | pass | keep |
| AUTH-003-BOUNDARY | AUTH-003 | boundary | false | false | pass | keep |
| AUTH-003-TUNE | AUTH-003 | false_positive | true | true | pass | tune |
| AUTH-004-POS | AUTH-004 | positive | true | true | pass | keep |
| AUTH-004-NEG | AUTH-004 | negative | false | false | pass | keep |
| AUTH-004-BOUNDARY | AUTH-004 | boundary | false | false | pass | keep |
| AUTH-005-POS | AUTH-005 | positive | true | true | pass | keep |
| AUTH-005-NEG | AUTH-005 | negative | false | false | pass | keep |
| AUTH-005-BOUNDARY | AUTH-005 | boundary | false | false | pass | keep |
| AUTH-005-TUNE | AUTH-005 | false_positive | true | true | pass | tune |

## Backend compatibility

- **auth_001_failed_logon_burst.yml**: native
- **auth_002_multiple_accounts.yml**: native
- **auth_003_success_after_failures.yml**: compatibility
- **auth_004_account_lockout_burst.yml**: native
- **auth_005_privileged_remote_logon.yml**: compatibility

## Tuning notes

- **AUTH-001** (medium/P3): Repeated failures from one source are useful early signal but need ownership and scanner context before escalation. Tuning: Baseline trusted scanners and identity infrastructure before adding exclusions.
- **AUTH-002** (medium/P2): Failures across several accounts increase concern, especially when the source is not an approved gateway or test system. Tuning: Review shared gateways and authorized identity-testing systems.
- **AUTH-003** (high/P1): A success after repeated failures is a higher-confidence sequence that should be reviewed before broad tuning. Tuning: Compare with password resets, user mistakes and approved support activity.
- **AUTH-004** (medium/P3): Lockout bursts can be operational noise or abuse pressure, so ownership and affected account type drive severity. Tuning: Treat as an operational anomaly; investigate stale services and machine accounts first.
- **AUTH-005** (high/P1): Privileged remote sessions have higher impact and should be matched against approved administration paths. Tuning: Baseline approved administration paths, jump hosts and service identities.

## Limitations

The runner is an educational oracle, not a SIEM. Generated queries require review and authorized testing.
