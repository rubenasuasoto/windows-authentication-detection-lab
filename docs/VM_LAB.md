# Optional isolated Windows VM lab

The synthetic test suite is the reproducible baseline. A virtual machine is a
separate validation phase for confirming field names, audit-policy assumptions
and expected alert timing with authorized Windows telemetry.

## Safety boundaries

- Use disposable evaluation VMs with no personal or production data.
- Prefer an internal virtual switch; do not bridge the lab to a work network.
- Take a clean snapshot before collecting events and restore it after a run.
- Generate only ordinary authentication outcomes through Windows interfaces.
- Do not run credential-access tools, memory inspection or offensive payloads.
- Never commit EVTX files. Export only the minimum normalized JSON fields after
  anonymization and keep raw logs outside the repository.

## Proposed phases

### VM-A: standalone Windows client

Validates events 4624, 4625 and 4672 with local fictional accounts. Enable the
relevant Advanced Audit Policy categories, record the audit configuration and
capture expected event fields. This phase can validate AUTH-001, AUTH-002,
AUTH-003 and parts of AUTH-005 without a domain controller.

### VM-B: isolated mini-domain

Adds a Windows Server evaluation VM as a lab-only domain controller and a
client VM. This phase exists specifically to validate account lockout event
4740 and domain-oriented field mappings. It should be attempted only after
VM-A is stable because it increases setup and maintenance significantly.

## Evidence contract

For each run, record the VM snapshot name, Windows build, audit policy, event
IDs observed, expected rule, observed result and a short tuning decision. Raw
logs remain private. Sanitized evidence must use fictional identities and RFC
5737 documentation addresses.

## Local platform decision

The development computer supports Windows Pro, but no supported hypervisor is
currently enabled or installed. Hyper-V is the preferred future option because
it is native to Windows Pro. Enabling Windows features and creating virtual
switches are explicit system changes and are intentionally outside the initial
repository build.

Run `uv run authlab vm-check` to refresh the read-only readiness artifact in
`artifacts/vm-readiness.json`. Use `VM_EVIDENCE_TEMPLATE.json` as the public
contract for sanitized validation notes.

Before enabling a hypervisor or creating a VM, complete
[`VM_READINESS_CHECKLIST.md`](VM_READINESS_CHECKLIST.md). The checklist keeps
the VM phase explicit, reversible and separate from this repository's normal
test pipeline.
