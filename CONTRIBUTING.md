# Contributing

Contributions must preserve the lab-only, defensive scope.

1. Use synthetic events and reserved documentation IP addresses.
2. Do not add binaries, EVTX files, credentials, tokens or production logs.
3. Add positive, negative and boundary fixtures for rule changes.
4. Run `uv run authlab all` and `uv run pytest` before opening a pull request.
5. Explain expected false positives and tuning trade-offs.

Rules are portable detection content, not production-ready guarantees. A rule
must not be promoted from `test` without evidence from an authorized target
environment.

