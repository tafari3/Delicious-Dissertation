# Scanner Architecture

## 1. Architectural objective

Build the smallest auditable architecture that supports safe, reproducible, specification-assisted API security testing across different REST implementation stacks.

The scanner must remain target-language independent. Scanner decisions are made from authorised HTTP/API behaviour, supplied API descriptions, configured identities, locally declared scope and observed response differentials.

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

- Citizen Records — Python / FastAPI
- Public Health Records — Node.js / Express
- Permit & Licensing — Java / Spring Boot

All labs run in Docker Compose for deterministic local evaluation. Their exact IDs, roles and experiment cases are defined in `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`.

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
| bounded observations      |
+-------------+-------------+
              |
              v
+---------------------------+
| Scan Planner              |
| deterministic rule plan   |
+-------------+-------------+
              |
              v
+---------------------------+
| Test Orchestrator         |
+-----+-----------+---------+
      |           |
      v           v
+-------------+  +-----------------------+
| Identity &  |  | Rule Modules          |
| Session Mgr |  | authz/auth/config/... |
+------+------+  +-----------+-----------+
       \                     /
        +---------+----------+
                  v
         +------------------+
         | HTTP Executor    |
         | scope/budget/etc |
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

* PDF export is optional if HTML is sufficient for the dissertation.
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
- environment classification (`lab`, `authorised-test`, etc.);
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
- title/category;
- OWASP/CWE mapping;
- severity default;
- prerequisites/applicability;
- deterministic test procedure;
- safe payload policy;
- proof condition;
- suspected/inconclusive conditions;
- stop conditions;
- evidence schema;
- remediation guidance;
- rule version.

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
      -> BLOCKED
      -> READY
          -> INVENTORY
          -> PLAN
          -> EXECUTING
              -> STOPPED
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
- profile is non-destructive unless explicitly configured for a controlled disposable lab write case;
- request ceilings are present;
- identity requirements for selected rules are satisfied;
- secrets are available only in runtime secret storage/environment;
- target is reachable;
- redirects cannot escape authorised scope.

### INVENTORY

Parse specification and build normalised operations. Live probing is restricted to safe, bounded discovery/observation defined by inventory policy.

### PLAN

Compute applicable rules before execution where possible. Expose estimated operation/test counts and maximum request budgets.

### EXECUTING

All target requests pass through the shared HTTP executor. Rule code must not bypass it.

### COMPLETED/STOPPED/FAILED

Persist outcome and metrics. `STOPPED` is not treated as a clean pass.

## 6. Shared HTTP executor

All network I/O MUST go through one controlled executor providing:

- target-scope validation before every request;
- actual destination validation;
- redirect revalidation;
- timeout policy;
- per-host concurrency ceiling;
- rate limiting;
- total-request budget;
- rule and resource-test sub-budgets;
- maximum response body capture size;
- content-type handling;
- retry policy limited to idempotent/transient cases;
- request/response timing;
- redaction hooks;
- correlation IDs;
- cancellation/stop support;
- ambient proxy environment disabled by default for target-facing traffic.

No rule module may instantiate an unrestricted independent HTTP client.

## 7. Specification ingestion

### 7.1 OpenAPI

Support OpenAPI 3.x first. OpenAPI 2/Swagger compatibility may be added later if it does not delay the core.

Ingestion must:

- parse with safe bounded loaders;
- normalise server/base URL information;
- extract operations/parameters/security requirements;
- hash original source;
- preserve parse warnings;
- never silently discard unsupported constructs;
- keep external reference retrieval disabled by default;
- prevent imported server metadata from expanding authorised network scope.

### 7.2 Postman

Support collection-based endpoint extraction and auth metadata where practical. Do not execute imported pre-request/test scripts.

## 8. Identity/session manager

Responsibilities:

- inject configured auth headers/cookies safely;
- maintain isolated sessions per controlled identity;
- support token refresh only through explicitly configured, scope-validated mechanisms;
- label observations by identity context;
- prevent credentials leaking into stored evidence;
- provide a clean anonymous context;
- enable pairwise/multi-role comparisons for authorisation rules.

For laboratory evaluation, identities use deterministic fixtures and disposable credentials supplied through local runtime configuration.

## 9. Authorisation comparison engine

Authorisation rules require a reusable differential engine rather than one-off response checks.

The comparison layer should consider:

- HTTP status;
- response schema/shape;
- stable semantic fields;
- object identifiers;
- ownership markers supplied through controlled project/lab metadata;
- response length only as weak supporting evidence;
- error semantics;
- mutation result/side-effect confirmation in controlled labs.

Do not equate `200` with vulnerability or `403` with safety without rule-specific proof.

## 10. Evidence pipeline

```text
raw observation in memory
    -> rule-specific evidence extraction
    -> global secret redaction
    -> size/field minimisation
    -> persistence
```

Raw unredacted HTTP exchanges must not be persisted by default.

Required redaction includes at least:

- `Authorization` headers;
- cookies / `Set-Cookie`;
- known API-key headers;
- password-like JSON/form fields;
- access/refresh token-like values;
- configurable sensitive field names;
- exact known runtime secret values.

## 11. Finding classifier

Rule executions preserve the complete execution-state model from `docs/02-TEST-CATALOGUE.md`. User-facing findings are created for appropriate `CONFIRMED`, `SUSPECTED` and `INFORMATIONAL` outcomes while `NOT_APPLICABLE`, `PASS_OBSERVED`, `INCONCLUSIVE` and `ERROR` remain visible in scan/evaluation records.

A finding includes:

- state;
- severity;
- confidence;
- concise title/explanation;
- evidence references;
- remediation;
- mapping metadata.

Severity and confidence are separate concepts.

## 12. Local application API/UI

Required capabilities:

- list/create projects;
- configure target/scope;
- import specification;
- configure identity metadata/secret references;
- select scan profile;
- show preflight result;
- start/stop scan;
- show progress/request counts;
- list/filter findings;
- inspect redacted evidence;
- export report/evaluation artefacts.

Do not build user registration, billing, teams, cloud accounts, distributed workers or enterprise RBAC for this dissertation.

## 13. CLI

The CLI is required for reproducibility and automated evaluation.

Conceptual commands:

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

Exact syntax may evolve, but final experiments must be runnable non-interactively from documented commands.

## 14. Persistence

SQLite is the default. Use migrations from the beginning.

Separate:

- project configuration;
- scan snapshots;
- inventory/specification metadata;
- observations/evidence;
- findings;
- evaluation results.

Ground-truth manifests remain version-controlled laboratory/evaluation artefacts and must not become ordinary scanner detector inputs.

Credentials and bearer material must never be persisted as ordinary database fields.

## 15. Determinism and provenance

Every scan/evaluation output should capture enough provenance to reproduce it:

- Git commit/version;
- rule catalogue version;
- lab version/image digest where practical;
- fixture version;
- spec hash;
- ground-truth manifest version/hash in evaluation records only;
- matcher version in evaluation records;
- scan profile;
- runtime timestamp/duration/request counts.

## 16. Dependency boundaries

The core scanner MUST NOT depend on:

- external AI/LLM services;
- proprietary vulnerability APIs;
- cloud queues;
- cloud databases;
- internet connectivity except where the intentionally authorised target itself requires it.

This keeps the project economically feasible and reproducible.

## 17. ZCHPC deployment boundary

The default architecture is local/VM/container based. If permission is later granted, an isolated copy of the student's own lab may be deployed to an authorised ZCHPC test resource without changing the core scanner architecture.

Do not add ZCHPC management-plane, hypervisor, unrelated tenant or production application assessment to the architecture.

## 18. Security architecture invariants

1. All target HTTP traffic uses the controlled executor.
2. Every request revalidates authorised target scope/destination.
3. Redirects cannot escape scope.
4. Secrets are runtime-only and redacted before persistence.
5. Rules stop at proof-of-condition.
6. Request budgets are enforced centrally and atomically.
7. Lab write tests use disposable seeded objects.
8. Evaluation does not depend on production targets.
9. Scanner/lab logs must not print credentials/tokens.
10. Detector code cannot read evaluation ground truth.
11. Any feature weakening these invariants requires explicit design review and must not be introduced opportunistically.
