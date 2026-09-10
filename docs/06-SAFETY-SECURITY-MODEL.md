# Safety and Security Model

## 1. Purpose

The scanner is a defensive research artefact. Safety controls prevent scope escape, uncontrolled traffic, secret leakage, destructive testing and invalid operational claims.

## 2. Universal preflight invariants

A scan can start only when:

- target is explicitly allow-listed;
- scheme/host/port/base path and actual destination match approved policy;
- redirects cannot escape scope;
- a profile with hard request/rate/concurrency limits is selected;
- required controlled identities are configured;
- runtime secrets are available through approved sources;
- rule plan fits global/rule/resource budgets;
- redaction/evidence store is healthy.

Hard failures block execution.

## 3. Profiles

### `safe-read-only`

Default non-destructive profile.

### `controlled-lab-full`

Only for `government-permit-service-fastapi` or another explicitly disposable research target. Permits narrowly defined mutation cases and deterministic cleanup/reset.

### `authorised-zchpc`

P10 only. Requires non-secret authorisation reference, exact operational allow-list and stricter ceilings. Non-destructive by default. Lab mutation permissions do not carry over.

## 4. Request budgets

Every scan has maximum requests/second, concurrency, total requests, timeout, redirects, capture size and a stricter resource-test sub-budget. Retries/redirect hops consume budget. Exhaustion stops or makes the affected result inconclusive; never a pass.

## 5. Proof-of-condition

Once sufficient evidence exists, stop the test. Do not enumerate extra records, maximise impact, chain weaknesses, persist access or create disruption.

## 6. Prohibited capabilities

No credential stuffing, password spraying, brute-force authentication, destructive/unrestricted fuzzing, DoS/stress/saturation, exploit framework, malware/persistence, VM escape, lateral movement or scanning outside explicit scope.

## 7. Controlled lab isolation

The lab uses only synthetic users/data and has deterministic vulnerable/corrected states. Mutation rules require disposable fixtures and successful cleanup/reset. Lab direct tests, not scanner output, establish ground truth.

## 8. ZCHPC operational boundary

Signed project authorisation exists, but this does not mean unrestricted permission. P10 must use only the exact assets, interfaces, identities, traffic levels and time windows represented by the approved scope.

Do not deliberately introduce operational vulnerabilities. Do not access unrelated tenants/assets. Any action not clearly covered by the local representation of the signed scope is blocked pending explicit scope clarification.

Operational evidence receives stronger minimisation/confidentiality treatment than synthetic lab evidence.

## 9. Secrets/logging

Never persist or log resolved passwords, bearer tokens, cookies, API keys or sensitive response material. Logs use structured sanitised summaries rather than raw request/response dumps.

## 10. Emergency stop

Cancellation blocks new scheduling. Automatic safety stops include scope/destination violation, budget exhaustion, repeated target instability, redaction/persistence failure, unexpected lab identity/mode change and lab cleanup/reset failure.

## 11. Research integrity

Ground truth is evaluation-only. Freeze ground truth, matcher, formulas/state treatment, final lab profile and ZAP configuration before controlled final collection. Retain failed/inconvenient runs with validity reasons.

Operational ZCHPC results remain a separate dataset and are not used to manufacture quantitative accuracy metrics without defensible ground truth.
