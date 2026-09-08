# Safety and Security Model

## 1. Purpose

This document defines the non-negotiable safety controls for the dissertation scanner. The scanner is a defensive research artefact. Its design must prevent accidental scope escape, uncontrolled request generation, secret leakage and escalation beyond proof-of-condition.

## 2. Safety invariants

A scan may execute only when all of the following are true:

1. the target is explicitly allow-listed;
2. the effective scheme, host, port and base path match registered scope;
3. the actual connection destination remains within approved address policy;
4. redirect behaviour cannot escape authorised scope;
5. a scan profile with explicit request ceilings is selected;
6. required controlled identities are configured for selected rules;
7. secrets are available through approved runtime secret sources;
8. the target passes reachability and safety preflight;
9. the selected rule plan fits within global, rule and resource budgets.

Failure of any hard invariant produces a blocking preflight result, not a warning-only state.

## 3. Scope model

Canonical scope dimensions:

```text
scheme + host + port + base-path policy + approved destination-address policy
```

Rules:

- wildcard Internet-scale targets are forbidden;
- DNS names and actual connection destinations are validated according to the locked network policy;
- redirects are evaluated as new target candidates before following;
- cross-host redirects are denied by default;
- HTTPS-to-HTTP downgrade is denied by default;
- URL userinfo is rejected;
- non-HTTP(S) target schemes are rejected;
- every target request passes through the shared executor and scope validator;
- imported OpenAPI/Postman server metadata never expands operator-approved scope.

No rule module may bypass these checks.

## 4. Scan profiles

### Safe Read-Only

Default profile. Permits only requests that do not intentionally alter application state. Resource-control checks are disabled unless separately enabled.

### Controlled Lab Full

Permitted only for project-owned disposable laboratory targets or another explicitly authorised disposable test environment. Allows narrowly defined mutation checks against seeded disposable fixtures and bounded resource-control observations.

### Custom

A custom profile may reduce or explicitly enumerate capabilities but may never disable hard scope, redaction or request-budget controls.

No profile may silently enable unrestricted fuzzing, arbitrary scripting or unbounded traffic.

## 5. Request budgets

Every scan defines:

- maximum requests per second;
- maximum total requests;
- maximum concurrent requests;
- per-request timeout;
- maximum redirect count;
- maximum captured response size;
- resource-control sub-budget;
- optional lower per-rule request budget.

Budget reservation/enforcement is atomic before scheduling/transmission. Retries and redirect hops consume the relevant budget.

Budget exhaustion is recorded as `STOPPED` or `INCONCLUSIVE` according to context, never as a pass.

## 6. Mutation policy

Write tests are allowed only when:

- target is a controlled lab or specifically authorised disposable test environment;
- operation is explicitly marked mutation-safe;
- test uses a known disposable synthetic fixture;
- mutation is minimal and reversible;
- reset/cleanup is available;
- rule stops after first sufficient proof.

Prefer reversible field changes or disposable objects. If cleanup/reset fails, stop further mutation tests against the affected fixture/environment until canonical state is restored.

## 7. Proof-of-condition rule

The scanner demonstrates whether a defined weakness is present; it does not maximise impact.

Once rule-specific proof is observed, stop. Do not:

- enumerate additional affected users/records;
- extract unnecessary records;
- persist unauthorised access;
- escalate privileges beyond the controlled proof case;
- chain weaknesses for broader compromise;
- create service disruption.

## 8. Prohibited capabilities

The implementation must not add:

- credential stuffing or password spraying;
- brute-force authentication testing;
- unrestricted or destructive fuzzing;
- high-volume denial-of-service, stress or saturation testing;
- exploit libraries intended for compromise;
- malware, persistence or post-exploitation behaviour;
- arbitrary user-supplied attack scripts;
- scanning outside explicit scope.

A future feature request conflicting with these constraints requires an explicit reviewed academic/project-scope decision before implementation.

## 9. Secrets

Approved initial sources:

- environment variables;
- ignored local `.env` files for laboratories/development;
- bounded local secret files with restrictive permissions.

Secrets must never be committed to Git or persisted in:

- database evidence;
- reports;
- structured logs;
- exception text;
- test snapshots;
- screenshots;
- evaluation datasets.

The runtime secret registry should provide exact known secret values to the redaction layer before persistence/export.

## 10. Evidence redaction boundary

Raw responses may exist transiently in memory for rule evaluation. Persistence happens only after redaction and minimisation.

Required redactions include:

- Authorization and Proxy-Authorization headers;
- cookies and Set-Cookie values;
- API-key headers;
- password/token/secret/session fields;
- exact known runtime secret values wherever observed.

Tests must prove redaction occurs before database writes and report generation.

## 11. Logging

Logs are operational telemetry, not packet capture.

Allowed examples:

- scan ID;
- rule ID;
- method and normalised path;
- status code;
- duration;
- request counters;
- state transitions;
- sanitised/redacted exception summaries.

Do not log request/response bodies by default. Target-controlled terminal/control text must be sanitised before operator-facing display.

## 12. Laboratory isolation

The canonical dissertation labs are:

- `citizen-records-fastapi`;
- `public-health-express`;
- `permit-licensing-spring`.

They run locally through Docker Compose on loopback-published ports or a controlled local bridge and use synthetic data only.

Evaluation tooling verifies expected lab ID/version/mode/fixture version before mutation-enabled execution.

Canonical vulnerable labs:

- publish only to loopback;
- do not run privileged;
- do not use host networking;
- do not mount the Docker socket;
- avoid unnecessary host mounts;
- have no production service dependency.

## 13. ZCHPC boundary

ZCHPC is optional hosting context for an isolated copy of the student's own laboratory only when formal permission/resources exist.

The dissertation does not scan ZCHPC production applications, management plane, hypervisor, network fabric, unrelated tenants or production government systems.

The full project must remain completable on student-controlled VM/container infrastructure without ZCHPC access.

## 14. Preflight decision model

Preflight produces:

```text
PASS      requirement satisfied
WARN      non-blocking limitation affecting coverage
BLOCK     scan must not start
```

Examples of `BLOCK`:

- target not allow-listed;
- destination/scope unsafe;
- redirect scope unsafe;
- missing request ceilings;
- mutation profile selected for non-disposable target;
- required identity secret unavailable;
- selected rules exceed configured hard policy.

Warnings never downgrade hard failures.

## 15. Emergency stop

The scan engine supports cooperative cancellation. A stop prevents new requests from being scheduled and records the reason.

Automatic safety-stop conditions include:

- request budget exhausted;
- repeated target instability beyond conservative threshold;
- redirect/destination scope violation;
- unexpected target identity/version/mode change in lab evaluation;
- unrecoverable redaction/persistence safety failure;
- cleanup/reset failure that makes further controlled writes unsafe.

## 16. Security testing of the scanner itself

Automated tests must cover:

- scope validation and redirect escape prevention;
- destination/DNS edge cases;
- URL parsing edge cases;
- atomic rate/request-budget enforcement;
- identity-session isolation;
- secret redaction;
- evidence minimisation;
- prevention of direct target HTTP clients in rule modules where feasible;
- safe malformed OpenAPI/Postman handling;
- report/dashboard injection controls;
- database/report output containing no known fixture secrets.

The full adversarial acceptance catalogue is `docs/11-RED-TEAM-ATTACK-MATRIX.md` and the locked design responses are in `docs/12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md`.

## 17. Research-integrity boundary

Ground-truth manifests are evaluation inputs only. Ordinary scanner detector packages must not read/import them.

Ground truth, matching logic, metric formulas and state-treatment rules are frozen before final data collection. Failed or inconvenient runs are retained with explicit validity reasons.

## 18. Ethical operating statement

No real Zimbabwean government, ZCHPC production or other third-party system is an evaluation dependency. The dissertation can be completed entirely against controlled synthetic e-government laboratories.

Any future real-system test requires written authorisation, an agreed scope, the same bounded safety model and any required university approval before execution.
