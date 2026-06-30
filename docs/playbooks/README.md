# Playbooks

These playbooks translate each synthetic detection into a short analyst workflow.
They are written for technical review and local lab validation, not for direct
production operation.

> Synthetic lab only. No production logs, credentials, malware, offensive
> simulations or host-changing actions are included.

## Playbook Index

| ID | Detection | Risk | Priority | Playbook |
|---|---|---|---|---|
| AUTH-001 | Failed logon burst from one source | Medium | P3 | [Open](AUTH-001_failed_logon_burst.md) |
| AUTH-002 | Failed logons across multiple accounts | Medium | P2 | [Open](AUTH-002_multiple_accounts.md) |
| AUTH-003 | Successful logon after repeated failures | High | P1 | [Open](AUTH-003_success_after_failures.md) |
| AUTH-004 | Account lockout burst | Medium | P3 | [Open](AUTH-004_account_lockout_burst.md) |
| AUTH-005 | Remote logon followed by special privileges | High | P1 | [Open](AUTH-005_privileged_remote_logon.md) |

## How To Read Them

1. Start with the trigger and expected fields.
2. Check ownership, business context and known administrative paths.
3. Compare the event sequence with the synthetic scenario shown in the demo.
4. Decide whether the case is suspicious, benign, or a tuning candidate.
5. Record the evidence that would be required before escalation.

Each playbook should be treated as a defensive investigation guide. It does not
include exploitation steps, host-changing commands or instructions for activity
outside an authorized lab.
