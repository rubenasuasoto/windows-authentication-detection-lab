# GitBook Setup

Use GitBook as a polished documentation layer for reviewers who want to read the
playbooks without browsing raw Markdown files in GitHub.

## Recommended Configuration

- Repository: `rubenasuasoto/windows-authentication-detection-lab`.
- Branch: `main`.
- Public URL: `https://2dam-7.gitbook.io/window-auth/`.
- GitBook sync direction for first import: `GitHub -> GitBook`.
- Content root: configured by `.gitbook.yaml` as `./docs/`.
- First page: `README.md`.
- Table of contents: `SUMMARY.md`.

The repository keeps `.gitbook.yaml` at the project root:

```yaml
root: ./docs/

structure:
  readme: README.md
  summary: SUMMARY.md
```

## Setup Steps

1. Create a GitBook space for the reviewer documentation.
2. Open the space configuration and enable GitHub Sync.
3. Install or authorize the GitBook GitHub app for this repository.
4. Select repository `rubenasuasoto/windows-authentication-detection-lab` and
   branch `main`.
5. Choose `GitHub -> GitBook` for the initial sync.
6. Confirm the sidebar uses `docs/SUMMARY.md`.
7. Confirm every `AUTH-*` playbook opens from the Playbooks section.
8. Publish the GitBook space only after the content renders correctly.

Expected playbook pages:

- `AUTH-001` failed logon burst.
- `AUTH-002` multiple accounts.
- `AUTH-003` success after failures.
- `AUTH-004` account lockout burst.
- `AUTH-005` privileged remote logon.

## Safety Checks

- Do not upload production logs, `.evtx` files, screenshots with private data,
  credentials, tokens, binaries or memory dumps.
- Keep GitBook connected to the repository docs instead of editing duplicate
  copies manually.
- Keep the synthetic lab notice visible in the overview and reviewer guide.
- Keep the public GitBook URL in `README.md` only while the space remains live
  and manually verified.

## Reviewer Path

1. Open GitBook at the Overview page.
2. Go to Playbooks.
3. Open `AUTH-003 Successful logon after repeated failures`.
4. Show the analyst checks, decision points and tuning notes.
5. Return to Validation to explain the synthetic evidence behind the playbook.
