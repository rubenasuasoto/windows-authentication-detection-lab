# Validation and tuning

Each detection has positive, negative and boundary scenarios. Selected cases
also represent expected administrative noise and are marked `tune` rather than
being hidden.

The generated matrix records:

- expected and observed alert state;
- pass or fail;
- matched fields and event count;
- scenario category;
- tuning disposition and analyst note.

## Interpretation

Synthetic fixtures prove that the documented logic behaves consistently. They
do not estimate production precision or recall. Organization-specific service
accounts, management hosts, network ranges and maintenance windows should be
measured before exclusions are approved.

Sigma correlations are not supported equally by every backend. Failed
conversion is reported as a visible compatibility result, never silently
treated as a successful deployment artifact.

