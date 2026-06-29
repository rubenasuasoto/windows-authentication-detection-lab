# AUTH-001 Failed Logon Burst From One Source

## Intent

Identify repeated failed Windows logons from one source against one computer.
This is a first-pass signal for password guessing or a broken authentication
dependency.

## Triage questions

- Which source IP and computer produced the failures?
- Did the failures affect one user or several users?
- Is the source an approved scanner, identity gateway or management host?
- Did the pattern happen during a known maintenance or testing window?
- Are there related successful logons from the same source after the burst?

## Fields to review

- `EventID`
- `IpAddress`
- `Computer`
- `TargetUserName`
- `Timestamp`

## Common false positives

- Vulnerability scanners that test authentication paths.
- Identity infrastructure retrying stale credentials.
- Applications with cached or expired service credentials.
- Users repeatedly mistyping passwords from the same workstation.

## Escalation guidance

Escalate when the source is unknown, external to the expected environment, or
continues to generate failures across several hosts. Combine with AUTH-003 or
AUTH-002 for stronger context before claiming a credential attack.

## Tuning notes

Prefer source-specific and owner-approved exceptions. Avoid lowering trust by
excluding entire subnets or all identity infrastructure without measurement.
