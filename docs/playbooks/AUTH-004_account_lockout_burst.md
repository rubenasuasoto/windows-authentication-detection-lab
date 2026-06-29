# AUTH-004 Account Lockout Burst

## Intent

Detect several account lockouts linked to the same caller and computer. This is
an operational anomaly compatible with brute-force pressure, stale credentials
or misconfigured services.

## Triage questions

- Which caller computer is associated with the lockouts?
- Are affected accounts human users or machine accounts?
- Did the lockouts begin after a password rotation or deployment?
- Is the caller a service host, application server or scheduled task system?
- Are there matching failed logons before the lockouts?

## Fields to review

- `EventID`
- `TargetUserName`
- `CallerComputerName`
- `Computer`
- `Timestamp`

## Common false positives

- Stale service credentials after password rotation.
- Scheduled tasks running with old credentials.
- Mapped drives or disconnected sessions.
- Machine accounts ending in `$`, which the lab treats separately.

## Escalation guidance

Escalate when human accounts are affected across unrelated systems, the caller
is unknown, or lockouts coincide with AUTH-001 or AUTH-002. Keep language
careful: lockouts show pressure or misconfiguration, not attribution by
themselves.

## Tuning notes

Machine account noise is a reasonable narrow exception. Do not suppress all
lockouts from a caller until the owner and root cause are documented.
