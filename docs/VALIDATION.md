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

The pinned pySigma Splunk backend converts `event_count` and `value_count`
natively but does not currently convert `temporal_ordered`. For AUTH-003 and
AUTH-005 the lab emits separately marked, reviewed compatibility SPL based on
the same fields and time windows. These queries are evidence for review, not a
claim of production deployment.
