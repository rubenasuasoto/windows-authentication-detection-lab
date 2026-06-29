# Security policy

## Defensive scope

This repository is a defensive detection-engineering lab. It contains only
synthetic Windows authentication events, Sigma rules, validation code and
generated reports. It does not contain credentials, malware, executable
samples, memory dumps, real event logs or instructions for gaining access to
systems.

The fixtures use fictional identities and documentation-only IP ranges. Do not
replace them with production data in a public fork.

## Reporting a problem

Please report suspected secrets, unsafe artifacts or security defects through
GitHub's private security advisory feature. Do not include real credentials or
private logs in a report.

## Supported version

The latest version on the default branch is supported. The rules remain at
Sigma status `test` until they are validated against an authorized SIEM and an
organization-specific baseline.

