# Scanner Architecture

## 1. Architectural objective

Build the smallest auditable architecture that supports safe, reproducible, specification-assisted black-box API security testing across different REST implementation stacks.

The scanner must remain target-language independent. All scanner decisions are made from HTTP behaviour, supplied API descriptions, configured identities, locally declared scope and observed response differentials.

## 2. Initial technology choices

These are engineering defaults for the dissertation implementation. They may be changed only when a concrete implementation reason is documented.

### Scanner/runtime

- **Python 3.12+**
- **httpx** for HTTP execution
- **Pydantic** for configuration and typed models
- **SQLAlchemy 2.x** for persistence
- **SQLite** as the default local database
- **FastAPI** for the local application/API surface
- **Typer** for the command-line interface
- **Jinja2 + HTMX or similarly lightweight server-rendered UI** for the minimal dashboard
- standard Python TLS/SSL facilities plus narrowly scoped supporting libraries where required
- pytest for unit/integration testing

The UI must not force a separate Node frontend build unless the simple server-rendered approach proves insufficient.

### Laboratory stacks

- Python / FastAPI
- Node.js / Express
- Java / Spring Boot

All labs run in Docker Compose for deterministic local evaluation.

## 3. Top-level component model

```text
+---------------------------+
| User                      |
| CLI / Local Web Dashboard |
+-------------+-------------+
              |
              v
+---------------------------+
| Project & Scan Service    |
+-------------+-------------+
              |
              v
+---------------------------+
| Safety / Scope Preflight  |
| allow-list, ceilings,     |
| profile, identity checks  |
+-------------+-------------+
              |
              v
+---------------------------+
| Inventory Builder         |
| OpenAPI / Postman / live  |
| observations              |
+-------------+-------------+
              |
              v
+---------------------------+
| Scan Planner              |
| builds deterministic      |
| rule execution plan       |
+-------------+-------------+
              |
              v
+---------------------------+
| Test Orchestrator         |
+-----+-----------+---------+
      |           |
      |           +----------------------------+
      v                                        v
+-------------+                     +-----------------------+
| Identity &  |                     | Rule Modules          |
| Session Mgr |                     | authz/auth/config/... |
+------+------+                     +-----------+-----------+
       \                                         /
        \                                       /
         +----------------+--------------------+
                          v
                 +------------------+
                 | HTTP Executor    |
                 | rate/timeout/etc |
                 +--------+---------+
                          |
                          v
                 +------------------+
                 | Target REST API  |
                 +------------------+

All observations
       |
       v
+---------------------------+
| Evidence Redaction Layer  |
+-------------+-------------+
              |
              v
+---------------------------+
| Finding Classifier        |
+-------------+-------------+
              |
              v
+---------------------------+
| SQLite Evidence Store     |
+-------------+-------------+
              |
              +-------------------------+
              |                         |
              v                         v
+-----------------------+     +-----------------------+
| Dashboard / Review    |     | Report Export        |
+-----------------------+     | JSON/CSV/HTML/PDF*   |
                              +-----------------------+

* PDF export is optional if HTML is sufficient for the dissertation; do not make PDF generation a core blocker.
```

## 4. Core domains

### 4.1 Project domain

A **Project** is the durable container for:

- target configuration;
- imported specifications;
- scope policy;
- controlled identities;
- scan profiles;
- scans and findings;
- evaluation metadata where relevant.

### 4.2 Target domain

A **Target** contains:

- scheme/host/base path;
- friendly name;
- target allow-list identity;
- expected environment classification (`lab`, `authorised-test`, etc.);
- optional specification association;
- safety constraints;
- optional written-authorisation reference metadata.

Never store secret authorisation documents in the repository.

### 4.3 Identity domain

An **Identity** represents a controlled test principal and must support:

- anonymous/no-auth context;
- user A;
- user B;
- low-privilege role;
- privileged/admin role;
- target-specific custom roles.

Credentials are runtime secrets, not persisted evidence. Persist only non-secret labels/metadata required for reproducibility.

### 4.4 Inventory domain

An **Endpoint Inventory** normalises operations into a common form:

- path template;
- method;
- parameters;
- request-body schema/fields;
- response schema hints;
- security requirements;
- source (`openapi`, `postman`, `observed`);
- documented/undocumented status;
- tags/operation identifier where available.

The scanner must tolerate incomplete specifications and record uncertainty rather than assuming the specification is ground truth.

### 4.5 Rule domain

Each security rule is a versioned unit with:

- stable rule ID;
- title;
- category;
- OWASP/CWE mapping;
- severity default;
- prerequisites;
- applicability test;
- test procedure;
- safe payload policy;
- proof condition;
- suspected condition;
- stop conditions;
- evidence schema;
- remediation guidance;
- deterministic rule version.

### 4.6 Scan domain

A **Scan** is an immutable historical execution record once finished. It references:

- scanner version/commit;
- target snapshot;
- specification hash;
- rule catalogue version;
- scan profile;
- identity configuration snapshot without secrets;
- start/end timestamps;
- request counts;
- outcome;
- findings/evidence.

## 5. Execution lifecycle

```text
DRAFT
  -> PREFLIGHT
      -> BLOCKED              (scope/safety/config invalid)
      -> READY
          -> INVENTORY
          -> PLAN
          -> EXECUTING
              -> STOPPED      (safety ceiling/user stop/fatal target condition)
              -> COMPLETED
              -> FAILED
          -> REPORTABLE
```

### DRAFT

User configures project, target, spec, identities and profile.

### PREFLIGHT

System must verify:

- target resolves to an allowed target;
- scheme/host/port/base URL match allow-list policy;
- profile is non-destructive unless explicitly configured for a lab-controlled write case;
- request ceilings are present;
- identity requirements for selected rules are satisfied;
- secrets are available only in runtime secret storage/environment;
- target is reachable;
- no redirect escapes authorised scope.

### INVENTORY

Parse specification and build normalised operations. Live probing is restricted to safe discovery operations defined in the inventory policy.

### PLAN

Compute applicable rules before execution where possible. The plan must expose estimated operation/test counts so the user can understand scan scope.

### EXECUTING

All requests pass through the shared HTTP executor. Rule code must not bypass it.

### COMPLETED/STOPPED/FAILED

Persist outcome and metrics. `STOPPED` is not treated as a clean pass.

## 6. Shared HTTP executor

All network I/O MUST go through one controlled executor providing:

- target-scope validation before every request;
- redirect revalidation;
- timeout policy;
- per-host concurrency ceiling;
- rate limiting;
- total-request budget;
- resource-test sub-budget;
- maximum response body capture size;
- content-type handling;
- retry policy limited to idempotent/transient cases;
- request/response timing;
- redaction hooks;
- correlation IDs;
- cancellation/stop support.

No rule module may instantiate an unrestricted independent HTTP client.

## 7. Specification ingestion

### 7.1 OpenAPI

Support OpenAPI 3.x first. If OpenAPI 2/Swagger can be accepted with a small compatibility layer, add it later without delaying the core.

Ingestion must:

- validate/parse safely;
- normalise server/base URL information;
- extract operations/parameters/security requirements;
- hash original source;
- preserve parse warnings;
- never silently discard unsupported constructs.

### 7.2 Postman

Support collection-based endpoint extraction and auth metadata where practical. Postman support is specification assistance, not a requirement to execute arbitrary collection scripts.

Do not run untrusted Postman pre-request/test JavaScript as part of the scanner.

## 8. Identity/session manager

Responsibilities:

- inject configured auth headers/cookies safely;
- maintain isolated sessions per controlled identity;
- support token refresh only through explicitly configured mechanisms;
- label observations by identity context;
- prevent credentials leaking into stored evidence;
- offer anonymous context for authentication checks;
- enable pairwise/multi-role comparisons for authorisation rules.

For laboratory evaluation, identities should have deterministic fixtures and disposable credentials supplied through local environment configuration.

## 9. Authorisation comparison engine

Authorisation rules require a reusable differential engine rather than one-off response checks.

The comparison layer should be able to consider:

- HTTP status;
- response schema/shape;
- stable semantic fields;
- object identifiers;
- ownership markers supplied by lab/test metadata;
- response length only as weak supporting evidence;
- error semantics;
- mutation result/side-effect confirmation in controlled labs.

Do not equate `200` with vulnerability or `403` with safety without analysing the rule-specific proof condition.

## 10. Evidence pipeline

Evidence flow must be:

```text
raw observation in memory
    -> rule-specific evidence extraction
    -> global secret redaction
    -> size/field minimisation
    -> persistence
```

Raw unredacted HTTP exchanges must not be persisted by default.

The redaction layer must cover at least:

- `Authorization` headers;
- cookies / `Set-Cookie`;
- known API-key headers;
- password-like JSON/form fields;
- access/refresh token-like values;
- configurable sensitive field names.

## 11. Finding classifier

A rule returns structured observations; the classifier creates a finding with:

- state: `confirmed`, `suspected`, `informational`;
- severity: `critical`, `high`, `medium`, `low`, `info`;
- confidence: numeric or ordinal consistent across the project;
- concise title;
- explanation;
- evidence references;
- remediation;
- mapping metadata.

Severity and confidence must be separate concepts.

## 12. Local application API/UI

The dashboard is intentionally minimal. Required capabilities:

- list/create projects;
- configure target/scope;
- import specification;
- configure identity metadata/secrets references;
- select scan profile;
- show preflight result;
- start/stop scan;
- show progress/request counts;
- list/filter findings;
- inspect redacted evidence;
- export report/evaluation artefacts.

Do not build user registration, billing, teams, cloud accounts, distributed workers or enterprise RBAC for this dissertation.

## 13. CLI

The CLI is required because it improves reproducibility and automated evaluation.

Planned conceptual commands:

```text
scanner project create
scanner spec import
scanner preflight
scanner scan run
scanner scan show
scanner findings list
scanner report export
scanner lab up
scanner lab reset
scanner evaluate run
```

Exact syntax may evolve, but every final research experiment must be runnable non-interactively from documented commands.

## 14. Persistence

SQLite is the default because the artefact is local-first and low-complexity.

Use migrations from the beginning. The data model must separate:

- project configuration;
- scan snapshots;
- inventory/specification metadata;
- observations/evidence;
- findings;
- evaluation ground truth/results.

Credentials and bearer material must never be persisted as ordinary database fields.

## 15. Determinism and provenance

Every scan/evaluation output should capture enough provenance to reproduce it:

- Git commit/version;
- rule catalogue version;
- lab version/image digest where practical;
- spec hash;
- ground-truth manifest version;
- seed/reset version;
- scan profile;
- runtime timestamp and duration.

## 16. Dependency boundaries

The core scanner MUST NOT depend on:

- external AI/LLM services;
- proprietary vulnerability APIs;
- cloud queues;
- cloud databases;
- internet connectivity except where the intentionally authorised target itself requires it.

This keeps the project economically feasible and reproducible.

## 17. Security architecture invariants

1. All HTTP traffic uses the controlled executor.
2. Every request revalidates authorised target scope.
3. Redirects cannot escape scope.
4. Secrets are runtime-only and redacted before persistence.
5. Rules stop at proof-of-condition.
6. Request budgets are enforced centrally.
7. Lab write tests use disposable seeded objects.
8. Evaluation does not depend on production targets.
9. Scanner and lab logs must not print credentials/tokens.
10. Any feature that weakens these invariants requires explicit design review and must not be introduced opportunistically.
