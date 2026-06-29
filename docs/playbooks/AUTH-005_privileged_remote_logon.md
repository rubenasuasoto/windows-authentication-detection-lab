# AUTH-005 Remote Logon Followed By Special Privileges

## Intent

Correlate remote or network logon activity with special privileges assigned to
the same logon identifier. This highlights sessions that deserve closer review,
especially for administrative users.

## Triage questions

- Which user received special privileges after the remote logon?
- Is the source a known jump host, admin workstation or service path?
- Is the destination expected for that user?
- Did the session occur during an approved change window?
- Are there related failed logons, lockouts or unusual host access?

## Fields to review

- `EventID`
- `LogonType`
- `TargetUserName`
- `SubjectUserName`
- `TargetLogonId`
- `SubjectLogonId`
- `Computer`
- `Timestamp`

## Common false positives

- Approved jump-host administration.
- Remote management by infrastructure teams.
- Service or automation accounts with documented privileges.
- Administrative maintenance windows.

## Escalation guidance

Escalate when the user, source, destination or time window is unexpected, or
when privileged remote logon follows suspicious authentication failures. Review
subsequent session activity in authorized telemetry before making conclusions.

## Tuning notes

The fixture `AUTH-005-TUNE` models approved jump-host activity. A good
exception should include both source context and approved administrative
purpose. Avoid suppressing all 4672 or all remote logons.
