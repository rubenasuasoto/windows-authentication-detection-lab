# Architecture

The project separates portable detection content from lab validation:

```text
rules/             Five primary Sigma detections
tests/fixtures/    Synthetic scenario definitions
src/authlab/       CLI, fixture oracle, audit and report generation
artifacts/         Disposable conversion and validation output
reports/latest/    Public, reproducible validation report
```

`pySigma` parses the Sigma documents and `sigma-cli` performs backend
conversion through the explicit `splunk_windows` processing pipeline. The
local oracle evaluates only the documented synthetic fixture contract. It
deliberately does not claim full Sigma or SIEM semantics.

The report consumes machine-readable validation results. This keeps the
reviewer narrative traceable to repeatable tests instead of manually written
success claims.
