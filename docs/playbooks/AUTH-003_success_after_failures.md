# AUTH-003 Successful Logon After Repeated Failures

## Intent

Raise confidence when repeated failures are followed by a successful logon for
the same user, source and host. The sequence is more interesting than isolated
failed or successful events.

## Triage questions

- Did the same account and source produce both the failures and the success?
- Was there a recent password reset, account unlock or helpdesk interaction?
- Is the logon type consistent with normal behavior for the user?
- Did the session access unusual systems after the successful logon?
- Is this a one-off user mistake or a recurring pattern?

## Fields to review

- `EventID`
- `TargetUserName`
- `IpAddress`
- `Computer`
- `LogonType`
- `TargetLogonId`
- `Timestamp`

## Common false positives

- Users mistyping a password and then succeeding.
- Password changes not synchronized across devices.
- Helpdesk-assisted account recovery.
- Training or onboarding activity.

## Escalation guidance

Escalate when the source is unusual, the user is privileged, or the successful
session is followed by sensitive access. Use this alert as a pivot into session
review rather than as standalone proof of compromise.

## Tuning notes

The fixture `AUTH-003-TUNE` intentionally remains an alert. Tune with support
ticket context or known training windows, not with broad suppression of the
sequence.
