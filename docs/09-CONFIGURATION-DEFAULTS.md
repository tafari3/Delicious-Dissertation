# Initial Configuration Defaults

## 1. Purpose

This document removes implementation ambiguity for Phase 1 onward. Values here are safe initial defaults for the dissertation laboratories and local scanner. They remain configurable, but AntiGravity should implement these as the starting contract unless a reviewed change updates them.

## 2. Local service ports

Use these initial ports unless they conflict with the VM and a documented change is required:

```text
Scanner web/API:                 127.0.0.1:8000
Citizen Records / FastAPI:       127.0.0.1:8101
Public Health / Express:         127.0.0.1:8102
Permit & Licensing / Spring:     127.0.0.1:8103
OWASP ZAP local control:         Docker-internal/default unless explicitly exposed
```

Labs should bind to loopback when run directly on the host. Docker Compose may use an isolated bridge internally while publishing only required lab ports to loopback.

## 3. Default scan profile — Safe Read-Only

```yaml
profile: safe-read-only
requests_per_second: 5
max_concurrency: 4
max_total_requests: 500
request_timeout_seconds: 10
connect_timeout_seconds: 5
max_redirects: 3
follow_cross_host_redirects: false
allow_https_to_http_downgrade: false
max_response_capture_bytes: 262144
max_evidence_excerpt_bytes: 16384
mutation_tests: false
resource_control_tests: false
```

These are ceilings, not performance targets. Rules should use fewer requests whenever possible.

## 4. Controlled Lab Full profile

```yaml
profile: controlled-lab-full
requests_per_second: 5
max_concurrency: 4
max_total_requests: 1000
request_timeout_seconds: 10
connect_timeout_seconds: 5
max_redirects: 3
follow_cross_host_redirects: false
allow_https_to_http_downgrade: false
max_response_capture_bytes: 262144
max_evidence_excerpt_bytes: 16384
mutation_tests: true
resource_control_tests: true
resource_requests_per_second: 1
resource_max_total_requests: 20
```

This profile is valid only when the target is explicitly classified as a controlled dissertation laboratory or another specifically authorised disposable test environment.

## 5. Rule budgets

Initial guidance:

```text
read-only differential authorisation rule: <= 6 requests per operation/fixture case
controlled mutation rule:                 <= 8 requests including verification/cleanup
configuration/header rule:                <= 3 requests per operation/target check
inventory check:                          no unnecessary live probing
resource-control rule:                    <= 20 requests total per bounded case
```

If a rule cannot reach a reliable conclusion within its defined budget, return `INCONCLUSIVE` rather than silently increasing traffic.

## 6. Retry policy

Default:

- zero retries for normal deterministic scanner requests;
- at most one retry for a clearly transient transport failure on an idempotent operation;
- no automatic retry for mutation tests;
- no retry when a safety/scope check fails;
- retry attempts consume the request budget.

## 7. Redirect policy

Default:

- same scheme + host + port only;
- maximum 3 redirects;
- every redirect target revalidated before following;
- HTTPS-to-HTTP downgrade denied;
- cross-host redirects blocked;
- blocked redirect becomes a structured observation/error, not an automatic follow.

## 8. Evidence defaults

- canonical persisted evidence format: structured JSON;
- maximum captured response material in memory: 256 KiB per response before truncation handling;
- maximum persisted evidence excerpt: 16 KiB;
- redact before persistence;
- binary bodies: metadata only unless a future explicit rule requires otherwise;
- known runtime secrets replaced with `[REDACTED]`;
- no credential hashes stored as substitutes.

## 9. Scan result defaults

Severity values:

```text
critical | high | medium | low | info
```

Confidence values:

```text
high | medium | low
```

Rule execution states:

```text
NOT_APPLICABLE
PASS_OBSERVED
CONFIRMED
SUSPECTED
INFORMATIONAL
INCONCLUSIVE
ERROR
```

## 10. Database/runtime paths

Recommended local defaults:

```text
.data/scanner.db
.data/imports/
.data/runtime/
reports/
evaluation/outputs/runtime/
```

These should be Git-ignored. Version-controlled sanitised research datasets belong in a separate clearly named evaluation artefact path only after review.

## 11. Identity secret references

Initial supported runtime secret sources:

```text
env
file
```

Example metadata only:

```yaml
label: citizen-a
auth_type: bearer
secret_source: env
secret_ref: LAB_CITIZEN_RECORDS_CITIZEN_A_TOKEN
```

The resolved value must not be returned through the web API, rendered in templates, written to logs, persisted in SQLite or exported to reports.

## 12. Laboratory modes

Each lab must expose deterministic mode metadata:

```text
vulnerable
corrected
```

The evaluation runner must verify expected lab ID/version/mode/fixture version before running. Mutation-enabled scans must refuse an unexpected or unknown mode.

## 13. Deterministic lab ports and IDs

```text
citizen-records-fastapi    -> http://127.0.0.1:8101
public-health-express      -> http://127.0.0.1:8102
permit-licensing-spring    -> http://127.0.0.1:8103
```

These IDs are evaluation metadata only; the scanner remains independent of target language/framework.

## 14. Evaluation repetition default

For final key experiments, start with **5 repeated runs per lab per mode per selected final profile**, unless methodology review chooses another value before final collection. Record every run; do not discard an inconvenient run without a documented validity reason.

This is a stability/reproducibility default, not a claim of statistical sufficiency.

## 15. ZAP baseline default

Use OWASP ZAP as a general-purpose baseline against the same reset laboratory state and scope. Record ZAP version/container identifier and configuration with each baseline dataset.

Comparison must distinguish `EQUIVALENTLY_TESTABLE`, `PARTIALLY_TESTABLE` and `NOT_EQUIVALENTLY_TESTABLE` cases rather than forcing equivalence where ZAP does not implement the same controlled multi-identity semantics.

## 16. ZCHPC deployment default

There is no required ZCHPC runtime configuration. Local/VM/container execution is canonical and sufficient for completion.

If explicit permission/resources are later granted, add a separate authorised deployment profile for the student's own isolated lab without changing scanner safety defaults or targeting ZCHPC production services.

## 17. Configuration change rule

If implementation reveals that a default is impractical, change the documented default in the same reviewed PR and explain why. Never silently implement a different ceiling, lab identity or safety policy than this file.
