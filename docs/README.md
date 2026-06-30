# Windows Authentication Detection Lab

This documentation is the reviewer-facing guide for a defensive, synthetic
Windows authentication detection lab. It is designed to be published through
GitBook while the source of truth stays in this GitHub repository.

> Synthetic lab only. No production logs, credentials, malware, offensive
> simulations or host-changing automation are included.

## Start Here

- Open the public mini-SOC demo:
  https://rubenasuasoto.github.io/windows-authentication-detection-lab/reports/latest/demo.html
- Or open the local mini-SOC demo with `uv run authlab demo --open`.
- Review the five detections in [Detection catalog](DETECTION_CATALOG.md).
- Walk through analyst response steps in [Playbooks](playbooks/README.md).
- Check validation results in [Validation](VALIDATION.md).
- Use [Portfolio presentation](PORTFOLIO_PRESENTATION.md) for a short reviewer
  walkthrough.

## Reviewer Flow

1. Open the demo and select `AUTH-003-POS`.
2. Compare expected and observed results for the synthetic event sequence.
3. Open the linked playbook and explain what an analyst would check next.
4. Open the validation documentation to show pass/fail evidence and limitations.
5. Close by stating that the lab is synthetic and not a production SIEM.

## Detection Coverage

| ID | Focus | Analyst entry point |
|---|---|---|
| AUTH-001 | Failed logon burst from one source | [Playbook](playbooks/AUTH-001_failed_logon_burst.md) |
| AUTH-002 | Failed logons across multiple accounts | [Playbook](playbooks/AUTH-002_multiple_accounts.md) |
| AUTH-003 | Successful logon after repeated failures | [Playbook](playbooks/AUTH-003_success_after_failures.md) |
| AUTH-004 | Account lockout burst | [Playbook](playbooks/AUTH-004_account_lockout_burst.md) |
| AUTH-005 | Remote logon followed by special privileges | [Playbook](playbooks/AUTH-005_privileged_remote_logon.md) |

## Public Demo Status

The GitHub Pages demo is live and should be the first stop for external
reviewers:

https://rubenasuasoto.github.io/windows-authentication-detection-lab/reports/latest/demo.html

GitBook is intended for polished documentation and playbook review. It does not
replace the local demo, validation commands or CI evidence.
