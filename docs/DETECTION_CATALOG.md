# Detection catalog

This catalog summarizes the five primary detections in the lab. The rules stay
in Sigma status `test` until they are validated in an authorized environment
with local baselines.

| ID | Rule | Events | Window and threshold | ATT&CK | Playbook |
|---|---|---|---|---|---|
| AUTH-001 | Failed Logon Burst From One Source | 4625 | 5 events in 5 minutes per source and computer | T1110.001 | [Triage](playbooks/AUTH-001_failed_logon_burst.md) |
| AUTH-002 | Failed Logons Across Multiple Accounts | 4625 | 4 distinct users in 10 minutes per source and computer | T1110.003 | [Triage](playbooks/AUTH-002_multiple_accounts.md) |
| AUTH-003 | Successful Logon After Repeated Failures | 4625, 4624 | 3 failures followed by success in 10 minutes for the same user and source | T1078 | [Triage](playbooks/AUTH-003_success_after_failures.md) |
| AUTH-004 | Account Lockout Burst | 4740 | 3 lockouts in 15 minutes per caller and computer | Operational anomaly | [Triage](playbooks/AUTH-004_account_lockout_burst.md) |
| AUTH-005 | Remote Logon Followed By Special Privileges | 4624, 4672 | Remote or network logon followed by privileges in 2 minutes for the same logon ID | T1078 | [Triage](playbooks/AUTH-005_privileged_remote_logon.md) |

## Analyst notes

### AUTH-001 Failed Logon Burst From One Source

Detects repeated failed authentication attempts from one source. It is useful
as a first-pass password guessing signal, but should be tuned around known
identity scanners, vulnerability scanners and noisy management systems.

### AUTH-002 Failed Logons Across Multiple Accounts

Looks for one source touching several user accounts in a short window. This is
the clearest password spraying story in the pack. Review shared gateways and
approved identity-testing systems before adding exclusions.

### AUTH-003 Successful Logon After Repeated Failures

Raises the severity when repeated failures are followed by a success for the
same user and source. It is intentionally framed as an authentication sequence,
not proof of compromise. Password resets, user mistakes and support activity
are expected tuning candidates.

### AUTH-004 Account Lockout Burst

Treats account lockouts as an operational anomaly compatible with brute-force
pressure, stale services or misconfigured scheduled tasks. The rule avoids
attribution claims and should drive investigation rather than automatic
escalation.

### AUTH-005 Remote Logon Followed By Special Privileges

Correlates remote or network logon activity with special privileges on the same
logon identifier. Baseline jump hosts, service identities and approved admin
paths before considering the rule production-ready.

## Deployment cautions

- The fixture runner is an educational oracle, not a SIEM.
- Correlation support varies by backend; review generated SPL before use.
- Keep the rules readable and explainable for analysts.
- Do not publish real logs, credentials, EVTX files or organization-specific
  exclusions in this repository.
