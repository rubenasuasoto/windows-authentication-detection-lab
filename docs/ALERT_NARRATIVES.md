# Alert narratives

These examples show how to turn each detection into a concise analyst note.
They use fictional entities and documentation IP ranges only. Treat them as
communication examples, not as claims about real activity.

## AUTH-001 Failed Logon Burst From One Source

**What happened:** One source generated five failed Windows logons against the
same computer within five minutes.

**Why it matters:** Repeated failures from one source can indicate password
guessing, a broken authentication dependency or a noisy approved scanner.

**What to check next:** Confirm source ownership, affected user count, target
host role, maintenance windows and any later successful logon from the same
source.

**Decision example:** Keep as an alert unless the source is an approved and
documented scanner with a narrow owner-approved exception.

## AUTH-002 Failed Logons Across Multiple Accounts

**What happened:** One source failed authentication against four distinct users
within ten minutes.

**Why it matters:** A single source touching multiple accounts is consistent
with password spraying behavior, especially when the accounts are unrelated.

**What to check next:** Review whether the source is a gateway, proxy, VPN or
identity-testing host. Check whether any targeted account later authenticated
successfully.

**Decision example:** Escalate when the source is not expected for
authentication traffic or when affected users span unrelated groups.

## AUTH-003 Successful Logon After Repeated Failures

**What happened:** A user had three failed logons followed by a successful
logon from the same source within ten minutes.

**Why it matters:** The ordered sequence is more interesting than isolated
failure events because it may show credential guessing followed by a valid
authentication.

**What to check next:** Look for helpdesk activity, password resets, user
mistakes, unusual source systems and sensitive actions after the successful
session.

**Decision example:** Keep visible as a higher-confidence authentication
sequence, then tune only with support or training context.

## AUTH-004 Account Lockout Burst

**What happened:** Three account lockouts were associated with the same caller
computer in fifteen minutes.

**Why it matters:** Lockout bursts can be caused by brute-force pressure, stale
credentials, scheduled tasks or broken services.

**What to check next:** Determine whether affected accounts are human users or
machine accounts. Review recent password rotations, application deployments
and caller ownership.

**Decision example:** Investigate operational root cause first. Escalate when
human accounts are affected from an unknown caller or combined with failed
logon bursts.

## AUTH-005 Remote Logon Followed By Special Privileges

**What happened:** A remote or network logon was followed by special privileges
on the same logon identifier within two minutes.

**Why it matters:** Privileged remote sessions deserve review because they can
represent legitimate administration or misuse of valid accounts.

**What to check next:** Confirm user role, source host, destination host,
approved change window and whether the path matches normal administration.

**Decision example:** Keep as a reviewable privileged-session alert. Tune only
when both jump-host context and administrative purpose are documented.

## Writing style

- Use cautious language: "is consistent with", "may indicate" and "requires
  review" are safer than attribution claims.
- Separate observable facts from interpretation.
- Mention the fields that drove the alert.
- Record a decision: keep, tune, escalate or gather more evidence.
- Do not include production names, private IP ranges, screenshots or raw logs in
  public notes.
