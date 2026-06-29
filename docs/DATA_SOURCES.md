# Data sources

The first pack uses the Windows Security event log only.

| Event ID | Purpose in this lab | Required fields |
|---|---|---|
| 4624 | Successful logon | TargetUserName, IpAddress, LogonType, TargetLogonId |
| 4625 | Failed logon | TargetUserName, IpAddress, Computer |
| 4672 | Special privileges assigned | SubjectUserName, SubjectLogonId, Computer |
| 4740 | Account locked out | TargetUserName, CallerComputerName, Computer |

Field availability varies by Windows version, audit policy and collection
pipeline. Missing fields must be handled explicitly during deployment. The
fixtures model a normalized subset and are not copied from a real endpoint.

