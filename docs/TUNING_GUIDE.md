# Tuning guide

This guide explains how to tune the detections without hiding the behavior the
lab is designed to catch. Treat every exclusion as an owned decision with
evidence, an expiry or review date, and a named business reason.

## Tuning principles

- Start with measurement. Review alert volume, source systems, affected users
  and time windows before changing logic.
- Prefer narrow exceptions over broad suppressions.
- Keep positive scenarios working after each tuning change.
- Document why an exception exists, who approved it and when it should be
  reviewed.
- Keep environment-specific values out of this public repository.

## Safe exception patterns

| Pattern | Safer use | Risky use |
|---|---|---|
| Approved scanner source | Exclude one documented source for AUTH-001 after confirming ownership | Excluding an entire subnet |
| Identity platform host | Add a host-specific exception with service ticket evidence | Suppressing all failed logons from identity infrastructure |
| Training or helpdesk workflow | Lower severity or route to a different queue for known training windows | Ignoring successful logon after failures for all users |
| Machine account noise | Exclude account names ending in `$` for lockout analysis | Suppressing lockouts from unmanaged callers |
| Jump host activity | Require known jump host plus approved admin group context | Excluding all privileged remote logons |

## Rule-by-rule notes

### AUTH-001 Failed Logon Burst From One Source

Review whether the source is a scanner, identity gateway or misconfigured
application. If it is authorized, tune by exact source and owner. Do not reduce
the threshold globally until several days of baseline evidence show that the
current threshold is too noisy.

### AUTH-002 Failed Logons Across Multiple Accounts

This is the password-spraying-oriented rule. Tune shared gateways carefully:
source-only exclusions can hide meaningful spraying. Prefer adding context such
as approved system owner, expected maintenance window or known test tenant.

### AUTH-003 Successful Logon After Repeated Failures

The fixture `AUTH-003-TUNE` represents a user who eventually succeeds after
mistakes. Keep the alert visible, then tune with helpdesk context, password
reset evidence or training windows. Avoid suppressing all interactive mistakes
because the sequence itself is still valuable.

### AUTH-004 Account Lockout Burst

Machine account lockouts are common operational noise and are excluded in the
fixture contract. Human account lockouts from a repeated caller should remain
visible until stale services, scheduled tasks and mapped drives are checked.

### AUTH-005 Remote Logon Followed By Special Privileges

The fixture `AUTH-005-TUNE` models approved jump-host administration. Good
tuning should require both the jump host and an approved administrative context.
Do not suppress all event 4672 activity or all remote logon types.

## Before and after checklist

Before tuning:

- Capture the rule ID, source, user, host, timestamp range and matched fields.
- Confirm whether the case is expected administrative activity.
- Check whether the alert maps to an existing support ticket or change window.

After tuning:

- Re-run `uv run authlab validate`.
- Confirm positive, negative and boundary fixtures still pass.
- Add or update a `tune` fixture if the scenario is useful for technical review.
- Update `reports/latest/` with `uv run authlab report`.

## Public repository boundary

Do not commit production exclusions, internal hostnames, real usernames, real
IP ranges, screenshots with private data or raw SIEM exports. Keep this guide
as a reusable method, not a record of a real organization.
