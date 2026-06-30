# VM readiness checklist

Use this checklist before moving from synthetic fixtures to an isolated Windows
validation VM. It is intentionally conservative: no repository command enables
Windows features, creates networks or collects raw logs.

## Host readiness

- [ ] Run `uv run authlab vm-check` and save the generated readiness summary.
- [ ] Run `uv run authlab vm-plan` and confirm VM-A/VM-B scope is still
      appropriate.
- [ ] Choose one reviewed hypervisor. Hyper-V is preferred on Windows Pro when
      available.
- [ ] Confirm the VM network will be isolated or internal-only.
- [ ] Confirm there is enough disk space for snapshots.
- [ ] Document who owns the lab and when it should be deleted.

## VM baseline

- [ ] Use a disposable Windows evaluation VM with no personal data.
- [ ] Create fictional local users only.
- [ ] Take a clean snapshot before collecting telemetry.
- [ ] Record Windows edition, build number and audit policy.
- [ ] Keep raw EVTX exports outside the repository.

## Detection validation scope

- [ ] VM-A validates 4624, 4625 and 4672 with local fictional accounts.
- [ ] VM-A can cover AUTH-001, AUTH-002, AUTH-003 and part of AUTH-005.
- [ ] VM-B is optional and exists only if domain lockout event 4740 needs field
      validation.
- [ ] No offensive tools, credential dumping tools, memory inspection or malware
      samples are used.

## Evidence sanitization

- [ ] Normalize only the fields needed by the rules.
- [ ] Replace hostnames, users and IP addresses with fictional values.
- [ ] Use RFC 5737 documentation IP ranges or loopback only.
- [ ] Store public evidence using `docs/VM_EVIDENCE_TEMPLATE.json`.
- [ ] Do not commit `.evtx`, screenshots with private data, tokens, credentials,
      memory dumps or binaries.

## Exit criteria

- [ ] Each tested rule has expected, observed and pass/tune outcome recorded.
- [ ] Any mismatch becomes either a documented tuning note or a rule update.
- [ ] Synthetic fixtures still pass after any rule change.
- [ ] Reports are regenerated with `uv run authlab all`.
