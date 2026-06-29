# AUTH-002 Failed Logons Across Multiple Accounts

## Intent

Detect one source failing authentication against several distinct accounts in a
short window. This is the pack's clearest password-spraying-oriented signal.

## Triage questions

- How many distinct users were touched by the same source?
- Are the targeted users related by department, role or naming pattern?
- Is the source a VPN, proxy, gateway or shared jump system?
- Did any of the users later authenticate successfully?
- Has this source produced similar activity before?

## Fields to review

- `EventID`
- `TargetUserName`
- `IpAddress`
- `Computer`
- `Timestamp`

## Common false positives

- Shared gateways where many users appear behind one source.
- Authorized identity testing.
- Broken applications trying multiple stored identities.
- Helpdesk workflows during account recovery windows.

## Escalation guidance

Escalate when the source is not expected for authentication traffic, touches
unrelated accounts, or repeats across multiple systems. Correlate with account
lockouts and successful logons after failure bursts.

## Tuning notes

Do not suppress a shared gateway by source alone unless other context is
available. Add owner, time window and expected user population whenever an
exception is approved.
