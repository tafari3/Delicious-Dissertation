# Initial Configuration Defaults

## 1. Purpose

Safe initial defaults for implementation. Signed/approved operational limits always override these toward the more restrictive value.

## 2. Local development ports

```text
Scanner web/API:                        127.0.0.1:8000
Government Permit/Service lab:         127.0.0.1:8101
Lab database:                           internal/local only; no public host port by default
OWASP ZAP control:                      internal/default unless explicitly required
```

Lab ID: `government-permit-service-fastapi`.

## 3. `safe-read-only`

```yaml
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

## 4. `controlled-lab-full`

```yaml
requests_per_second: 5
max_concurrency: 4
max_total_requests: 1000
request_timeout_seconds: 10
connect_timeout_seconds: 5
max_redirects: 3
mutation_tests: true
resource_control_tests: true
resource_requests_per_second: 1
resource_max_total_requests: 20
```

Valid only for the disposable synthetic lab or another explicitly controlled disposable target.

## 5. `authorised-zchpc`

Initial engineering ceiling before applying any stricter signed-scope limit:

```yaml
requests_per_second: 2
max_concurrency: 2
max_total_requests: 200
request_timeout_seconds: 10
connect_timeout_seconds: 5
max_redirects: 2
follow_cross_host_redirects: false
allow_https_to_http_downgrade: false
mutation_tests: false
resource_control_tests: false
require_authorisation_reference: true
require_exact_address_scope: true
```

These are not a claim that the signed authorisation permits this much traffic. Runtime configuration must use the minimum of repository safety ceilings and the actual approved limits. If the signed scope is narrower or unclear, preflight blocks.

## 6. Rule budgets

```text
read-only differential authorisation: <= 6 requests per case
controlled lab mutation:              <= 8 requests incl. verification/cleanup
configuration/header check:           <= 3 requests per check
resource-control case:                <= 20 requests total, lab/explicit-authorisation only
```

If proof cannot be reached safely within budget, return `INCONCLUSIVE` rather than increasing traffic.

## 7. Retry/redirect defaults

- zero retries for normal deterministic requests;
- at most one retry for clearly transient idempotent transport failure;
- no automatic mutation retry;
- no retry after safety/scope failure;
- every retry/redirect hop consumes budget;
- cross-authority redirect blocked by default;
- credentials never forwarded to unvalidated authority.

## 8. Evidence/report defaults

- redact before persistence;
- canonical evidence: structured JSON;
- max response capture: 256 KiB;
- max persisted excerpt: 16 KiB;
- binary bodies metadata-only unless a specific safe rule needs otherwise;
- runtime-known secrets -> `[REDACTED]`;
- report formats: HTML, PDF, JSON, CSV;
- ZCHPC operational reports default to restricted/confidential handling until explicitly sanitised for research publication.

## 9. Result states

`NOT_APPLICABLE`, `PASS_OBSERVED`, `CONFIRMED`, `SUSPECTED`, `INFORMATIONAL`, `INCONCLUSIVE`, `ERROR`.

Severity: `critical | high | medium | low | info`.

Confidence: `high | medium | low`.

## 10. Runtime paths

```text
.data/scanner.db
.data/imports/
.data/runtime/
reports/
evaluation/outputs/runtime/
.local/zchpc/           # local/ignored operational configuration only
```

All runtime and operational-sensitive paths are Git-ignored.

## 11. Repetition and ZAP

The exact controlled-lab repeat count is frozen before final data collection. Every run is retained with validity metadata. Do not claim statistical significance solely from a small repetition count.

Use a pinned/documented ZAP version/configuration against the same controlled lab state. Record equivalently/partially/not-equivalently testable status.

## 12. Change rule

If implementation reveals a default is impractical, update this document in the same reviewed change. Never silently weaken a hard safety ceiling or operational authorisation boundary.
