# Release checklist v0.1.0

Use this checklist before publishing the first GitHub release. It keeps the
portfolio scope explicit and avoids claims beyond the synthetic lab.

## Final local validation

- [ ] Run `uv sync --extra dev --locked`.
- [ ] Run `uv run ruff check .`.
- [ ] Run `uv run pytest --cov=authlab --cov-report=term-missing`.
- [ ] Run `uv run authlab all`.
- [ ] Run `uv run authlab demo`.
- [ ] Confirm `git diff --exit-code -- reports/latest`.
- [ ] Run `uv run detect-secrets-hook --baseline .secrets.baseline $(git ls-files)`.
- [ ] Run `uv run pip-audit --skip-editable`.

## Portfolio safety review

- [ ] Confirm all examples use synthetic JSON events.
- [ ] Confirm `reports/latest/demo.html` is static and self-contained: no
      external assets, forms, uploads, `fetch(` or backend calls.
- [ ] Confirm the only external demo links are the public GitBook playbook URLs.
- [ ] Confirm GitHub Pages is configured to deploy from GitHub Actions and is
      currently published.
- [ ] Confirm the published demo opens:
      `https://rubenasuasoto.github.io/windows-authentication-detection-lab/reports/latest/demo.html`.
- [ ] Confirm playbook links work from the published demo.
- [ ] Confirm the GitBook space syncs from `main` using `docs/` as content
      root and renders `docs/SUMMARY.md`.
- [ ] Confirm all five `AUTH-*` playbooks open from GitBook.
- [ ] Confirm the public GitBook URL opens:
      `https://2dam-7.gitbook.io/window-auth/`.
- [ ] Confirm docs use fictional identities and documentation IP ranges only.
- [ ] Confirm no `.evtx`, screenshots with private data, credentials, tokens,
      binaries, memory dumps or production logs are committed.
- [ ] Confirm VM documentation remains optional, isolated and read-only from the
      repository command perspective.
- [ ] Confirm README and reports state that this is not a production SIEM
      deployment.

## GitHub release steps

- [ ] Push the repository to GitHub.
- [ ] Confirm the validation workflow passes on Linux and Windows.
- [ ] Confirm the GitHub Pages workflow publishes the static demo site.
- [ ] Confirm the public GitBook playbook documentation is published.
- [ ] Confirm the workflow badge is present in `README.md`.
- [ ] Create an annotated tag: `git tag -a v0.1.0 -m "v0.1.0"`.
- [ ] Push the tag: `git push origin v0.1.0`.
- [ ] Create a GitHub release from `v0.1.0`.

## Suggested release notes

```text
v0.1.0 - Windows Authentication Detection Lab

- Five lab-only Sigma correlations for Windows authentication anomalies.
- Synthetic fixture validation with positive, negative, boundary and tuning cases.
- Interactive local mini-SOC demo for guided scenario review.
- Reviewed Splunk conversion outputs for supported detections.
- Bilingual portfolio reports and analyst-facing playbooks.
- Read-only VM readiness and planning commands for optional isolated validation.

Scope: defensive portfolio lab using synthetic data. No production logs,
credentials, malware, offensive simulations or host-changing automation are
included.
```
