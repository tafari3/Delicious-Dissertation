# Implementation Roadmap and Acceptance Gates

## 1. Delivery principle

Implementation proceeds in small vertical phases. A phase is complete only when its acceptance criteria are demonstrated by automated tests and reproducible commands. AntiGravity must not skip ahead by creating placeholder modules for later phases while the current phase is failing.

## 2. Phase sequence

```text
P0  Blueprint and execution contract
P1  Repository/runtime foundation
P2  Deterministic laboratory foundation
P3  Specification ingestion and endpoint inventory
P4  Scope, identity and controlled HTTP execution
P5  Authorisation scanner rules
P6  Authentication/configuration/inventory/resource rules
P7  Evidence, findings and reporting
P8  Local dashboard and operator workflows
P9  Evaluation harness and OWASP ZAP baseline
P10 Final research validation and reproducibility package
```

## P0 — Blueprint and execution contract

### Deliverables

- locked project charter;
- architecture;
- security test catalogue;
- user journeys;
- laboratories/evaluation protocol;
- data/evidence/reporting model;
- safety model;
- delivery model;
- AntiGravity instructions.

### Exit gate

No product implementation is required. Planning documents must be internally consistent and traceable to the proposal.

## P1 — Repository/runtime foundation

### Objective

Create a clean installable Python application with stable developer commands.

### Deliverables

- Python project metadata and dependency locking;
- package layout for scanner core, application API/UI, CLI and shared models;
- configuration loading;
- SQLAlchemy + migration baseline;
- health command/endpoint;
- structured logging with redaction hooks;
- pytest, formatting, linting and type-checking baseline;
- Docker Compose root file or equivalent lab orchestration entrypoint;
- CI workflow.

### Required commands

The exact tools may evolve, but the repository must expose stable wrappers such as:

```text
make bootstrap
make verify
make test
make app
make labs-up
make labs-down
```

Equivalent task-runner commands are acceptable if documented once and used consistently.

### Exit gate

A clean VM can clone, bootstrap and run verification without editing source files manually.

## P2 — Deterministic laboratory foundation

### Objective

Build the three synthetic target APIs before scanner detection logic is tuned against them.

### Deliverables

- FastAPI mobile-money lab;
- Express revenue/tax lab;
- Spring Boot citizen-services lab;
- deterministic fixtures;
- controlled identities/roles;
- vulnerable and corrected modes;
- OpenAPI artefacts;
- reset/seed scripts;
- machine-readable ground-truth manifests;
- lab conformance tests.

### Critical rule

Ground truth is authored independently of scanner output. Do not change a manifest merely to make a scanner result count as correct.

### Exit gate

Each lab can be reset, started, health-checked and independently verified as vulnerable/corrected according to its manifest.

## P3 — Specification ingestion and endpoint inventory

### Deliverables

- OpenAPI 3.x parser/normaliser;
- Postman collection importer without script execution;
- parse warnings and source hashing;
- normalised inventory model;
- operation annotations;
- documented/undocumented comparison foundation;
- CLI/UI-independent service layer tests.

### Exit gate

The same inventory representation is produced for representative operations across all three labs and parsing uncertainty is preserved rather than silently discarded.

## P4 — Scope, identity and controlled HTTP execution

### Deliverables

- target registration model;
- allow-list/scope validator;
- redirect revalidation;
- central `httpx` executor;
- global/per-rule budgets;
- timeouts/concurrency control;
- scan lifecycle/state machine;
- runtime secret resolver;
- identity/session isolation;
- scan planner/preflight;
- cooperative cancellation.

### Exit gate

Architecture tests demonstrate that rules cannot execute network requests outside the controlled executor path, and safety tests prove scope/budget enforcement.

## P5 — Authorisation scanner rules

Implement the catalogue authorisation rules first because they are the principal research contribution.

### Minimum rule set

- `AUTHZ-BOLA-001` cross-user object read;
- `AUTHZ-BOLA-002` controlled cross-user mutation;
- `AUTHZ-BFLA-001` low-privilege privileged function;
- `AUTHZ-BFLA-002` anonymous privileged function;
- `AUTHZ-BOPLA-001` protected-property exposure;
- `AUTHZ-BOPLA-002` controlled mass assignment.

### Implementation requirements

Every rule has:

- applicability function;
- deterministic request plan;
- request budget;
- proof/suspected conditions;
- evidence builder;
- stop condition;
- automated positive and negative lab tests.

### Exit gate

Authorisation rules detect their seeded vulnerable cases and do not assert the equivalent corrected cases as confirmed vulnerabilities.

## P6 — Authentication, configuration, inventory and bounded resource rules

### Deliverables

Implement the remaining locked catalogue categories, including:

- missing authentication;
- invalid/expired/revoked controlled token/session observations;
- authentication inconsistency;
- CORS;
- relevant TLS/header observations;
- verbose error leakage;
- risky HTTP methods;
- exposed API documentation;
- live/spec inventory mismatch;
- bounded rate/resource-control observation.

### Exit gate

Every implemented rule maps to at least one deterministic test case and has explicit non-applicability/inconclusive behaviour.

## P7 — Evidence, findings and reporting

### Deliverables

- redaction-before-persistence pipeline;
- evidence minimisation;
- finding classifier;
- severity/confidence model;
- canonical JSON report + schema;
- CSV research outputs;
- human-readable HTML report;
- OWASP/CWE mapping presentation;
- provenance metadata.

### Exit gate

Automated tests inject known dummy secrets and prove they cannot be found in persisted evidence or exported reports.

## P8 — Local dashboard and complete operator workflow

### Required screens

1. Home / project list;
2. Create/edit project;
3. target and scope configuration;
4. specification import summary;
5. inventory review;
6. identity metadata configuration;
7. scan profile/preflight;
8. execution status;
9. findings list/detail;
10. report/export and evaluation links.

### UI rule

The dashboard is a thin interface over the same application services used by the CLI. Do not duplicate scanner logic in route handlers/templates.

### Exit gate

The core user journey can be completed from the browser and from CLI using the same underlying models and produces equivalent scan records.

## P9 — Evaluation harness and OWASP ZAP baseline

### Deliverables

- deterministic evaluation runner;
- lab reset/verification integration;
- ground-truth matching;
- TP/FP/FN and derived metric calculation;
- repeated-run dataset generation;
- cross-stack comparison;
- ZAP baseline orchestration and normalisation where applicable;
- validity/inconclusive handling;
- CSV/JSON research dataset outputs.

### Exit gate

One command can execute a documented evaluation profile and produce metrics tied to scanner commit, lab version and ground-truth hash.

## P10 — Final research validation and reproducibility package

### Required final validation

- clean-environment bootstrap proof;
- all three labs vulnerable/corrected runs;
- repeated key runs;
- scanner-vs-ground-truth metrics;
- ZAP comparison;
- cross-platform summary;
- evidence quality review;
- all safety tests;
- final reports/datasets generated from tagged source;
- examiner/supervisor reproduction guide.

### Exit gate

The repository contains enough instructions and versioned artefacts for another technically competent person to reproduce the dissertation demonstration and evaluation without undocumented manual steps.

## 3. Quality gates applying to every implementation PR

Each implementation change should, where relevant, pass:

- formatter;
- lint;
- type checking;
- unit tests;
- integration tests;
- safety tests;
- secret-leak checks;
- lab contract tests;
- report/schema validation.

No failing verification is accepted as “good enough for now” on `main`.

## 4. Scope control

Do not add the following merely because they are attractive engineering features:

- distributed workers;
- Kubernetes;
- Redis/message brokers;
- cloud SaaS deployment;
- multi-tenancy/RBAC for scanner users;
- LLM-dependent vulnerability reasoning;
- plugin marketplace;
- GraphQL/SOAP engines;
- exploit chaining;
- enterprise vulnerability-management integrations.

They do not answer the approved dissertation research questions and increase delivery risk.

## 5. Change control

A design change that affects research scope, evaluation methodology, safety invariants, test catalogue semantics or laboratory ground truth must update the relevant authoritative document in the same PR and explain the reason. Implementation must not silently redefine the research experiment.