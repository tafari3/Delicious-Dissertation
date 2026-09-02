# Safety and Security Model

## 1. Purpose

This document defines the non-negotiable safety controls for the dissertation scanner. The scanner is a defensive research artefact. Its design must prevent accidental scope escape, uncontrolled request generation, secret leakage and escalation beyond proof-of-condition.

## 2. Safety invariants

A scan may execute only when all of the following are true:

1. the target is explicitly allow-listed;
2. the effective scheme, host, port and base path match the registered scope;
3. redirect behaviour cannot escape authorised scope;
4. a scan profile with explicit request ceilings is selected;
5. required controlled identities are configured for selected rules;
6. secrets are available through approved runtime secret sources;
7. the target passes reachability and safety preflight;
8. the selected rule plan fits within global and rule-specific budgets.

Failure of any invariant must produce a blocking preflight result, not a warning-only state.

## 3. Scope model

The canonical scope key is:

```text
scheme + host + port + base-path prefix
```

Rules:

- wildcard Internet-scale targets are forbidden;
- DNS names are revalidated at request time where practical;
- redirects are evaluated as new target candidates before following;
- cross-host redirects are denied by default;
- scheme downgrade from HTTPS to HTTP is denied by default;
- userinfo embedded in URLs is rejected;
- non-HTTP(S) schemes are rejected;
- every HTTP request must pass through the shared executor and scope validator.

No rule module may bypass these checks.

## 4. Scan profiles

### Safe Read-Only

Default profile. Permits only requests that do not intentionally alter application state. Resource-control checks are disabled unless separately enabled.

### Controlled Lab Full

Permitted only for project-owned disposable laboratory targets. Allows narrowly defined mutation checks against seeded disposable fixtures and bounded resource-control observations.

### Custom

A custom profile may only reduce or explicitly enumerate capabilities. It must never silently enable unrestricted fuzzing, arbitrary scripting or unbounded request rates.

## 5. Request budgets

Every scan must define:

- maximum requests per second;
- maximum total requests;
- maximum concurrent requests;
- per-request timeout;
- maximum redirect count;
- maximum captured response size;
- resource-control sub-budget;
- optional per-rule request budget.

The executor must stop further requests once a hard budget is reached. Budget exhaustion is recorded as `STOPPED` or `INCONCLUSIVE`, never as a pass.

## 6. Mutation policy

Write tests are allowed only when:

- the target is classified as a controlled lab or specifically authorised disposable test environment;
- the operation is explicitly marked mutation-safe;
- the test uses a known disposable fixture;
- the mutation is minimal and reversible;
- reset/cleanup is available;
- the rule stops after first sufficient proof.

Delete operations should be avoided unless required by a seeded laboratory case. Prefer reversible field changes or disposable objects.

## 7. Proof-of-condition rule

The scanner exists to demonstrate whether a defined weakness is present, not to maximise impact.

Once the rule-specific proof condition is observed, the rule must stop. It must not:

- enumerate additional victims;
- extract unnecessary records;
- persist unauthorised access;
- escalate privileges beyond the seeded proof case;
- chain vulnerabilities for broader compromise;
- create service disruption.

## 8. Prohibited capabilities

The implementation must not add:

- credential stuffing or password spraying;
- brute-force authentication testing;
- unrestricted or destructive fuzzing;
- high-volume denial-of-service or stress testing;
- exploit payload libraries intended for compromise;
- malware, persistence or post-exploitation behaviour;
- arbitrary user-supplied attack scripts;
- scanning of targets outside explicit scope.

If a future feature request conflicts with these constraints, it requires an explicit project-scope decision before implementation.

## 9. Secrets

Approved initial secret sources:

- environment variables;
- ignored local `.env` files for laboratories/development;
- local secret files with restrictive permissions.

Secrets must not be committed to Git.

Secrets must never be persisted in:

- database evidence;
- reports;
- structured logs;
- exception text;
- test snapshots;
- screenshots;
- evaluation datasets.

The runtime secret registry should provide known values to the redaction layer so accidental body/header echoes can be removed before persistence.

## 10. Evidence redaction boundary

Raw responses may exist transiently in memory for rule evaluation. Persistence happens only after redaction and minimisation.

Required redactions include:

- Authorization and Proxy-Authorization headers;
- cookies and Set-Cookie values;
- API-key headers;
- password/token/secret/session fields;
- known runtime secret values wherever observed.

Tests must verify that redaction occurs before database writes and report generation.

## 11. Logging

Logs are operational telemetry, not packet capture.

Allowed logging examples:

- scan ID;
- rule ID;
- method and normalised path;
- status code;
- duration;
- request counters;
- state transitions;
- redacted exception summaries.

Do not log request bodies or full response bodies by default.

## 12. Laboratory isolation

The three dissertation labs should run locally through Docker Compose on predictable loopback or dedicated local bridge endpoints. They must use synthetic data only.

Evaluation tooling must verify the expected lab identity/version before executing mutation-enabled profiles.

## 13. Preflight decision model

Preflight produces structured results:

```text
PASS      requirement satisfied
WARN      non-blocking limitation affecting coverage
BLOCK     scan must not start
```

Examples of `BLOCK`:

- target not allow-listed;
- redirect scope unsafe;
- missing request ceilings;
- mutation profile selected for non-lab target;
- required identity secret unavailable;
- selected rules exceed configured hard policy.

Warnings must never downgrade hard safety failures.

## 14. Emergency stop

The scan engine must support cooperative cancellation. A stop request prevents new requests from being scheduled and records the reason.

Automatic safety-stop conditions include:

- request budget exceeded;
- repeated target instability according to conservative threshold;
- redirect scope violation;
- unexpected target identity/version change in lab evaluation;
- unrecoverable redaction/persistence safety failure.

## 15. Security testing of the scanner itself

The scanner must have automated tests for:

- scope validation and redirect escape prevention;
- URL parsing edge cases;
- rate and request-budget enforcement;
- secret redaction;
- evidence minimisation;
- prevention of direct HTTP clients in rule modules where feasible through architecture/lint tests;
- safe handling of malformed OpenAPI/Postman input;
- database/report output containing no known fixture secrets.

## 16. Ethical operating statement

No real Zimbabwean fintech, government or other third-party system is an evaluation dependency. The dissertation can be completed entirely against controlled laboratories. Any future real-system test requires written authorisation and must remain within the same bounded safety model.