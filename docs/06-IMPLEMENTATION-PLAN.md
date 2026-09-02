# Implementation Plan

## 1. Execution strategy

Implementation is divided into small, verifiable phases. AntiGravity should complete one phase at a time and prove its acceptance criteria before moving forward.

The sequence is designed around the research risk: first make safety/inventory reproducible, then build laboratories and differential authorisation capability, then reporting/evaluation.

```text
P0  Blueprint / source of truth
P1  Repository + runtime foundation
P2  Safety, scope and persistence foundation
P3  Specification ingestion + inventory
P4  Laboratory suite + ground truth
P5  Identity/session + HTTP execution engine
P6  Authorisation rules
P7  Authentication/config/inventory/resource rules
P8  Evidence, findings and reports
P9  Local dashboard + CLI completion
P10 Evaluation harness + OWASP ZAP baseline
P11 Hardening, repeated experiments and dissertation release
```

## 2. P0 — Blueprint / source of truth

### Deliverables

- project charter;
- architecture;
- test catalogue;
- user journeys;
- labs/evaluation protocol;
- data/reporting model;
- implementation plan;
- `AGENTS.md` execution rules;
- repository README aligned to source of truth.

### Exit criteria

- proposal requirements traceable into the blueprint;
- no contradiction with safety delimitations;
- implementation phases have objective gates;
- AntiGravity can determine what to build without inventing core product scope.

## 3. P1 — Repository and runtime foundation

### Objective

Create a clean Python project and deterministic development environment without implementing security rules yet.

### Deliverables

Suggested structure:

```text
scanner/
  pyproject.toml
  src/delicious_scanner/
    __init__.py
    cli/
    web/
    domain/
    services/
    rules/
    evidence/
    persistence/
  tests/

labs/
evaluation/
docs/
scripts/
.github/workflows/
Makefile
.env.example
.gitignore
```

### Requirements

- Python 3.12+;
- locked dependency strategy (`uv.lock`, Poetry lock, or equivalent); choose one and document it;
- pytest;
- Ruff or equivalent lint/format tool;
- type checking with mypy/pyright where practical;
- FastAPI app with `/health`;
- Typer CLI with `--version`/health command;
- SQLAlchemy + migration framework;
- structured logging with secret-safe defaults;
- Docker Compose skeleton for labs;
- CI workflow for verification.

### Canonical task surface

Establish commands conceptually equivalent to:

```text
make setup
make format-check
make lint
make typecheck
make test
make verify
```

`make verify` should become the one local/CI acceptance command.

### Exit criteria

- clean checkout can bootstrap;
- application starts;
- CLI starts;
- database migrates from empty state;
- CI runs `make verify`;
- no secrets committed.

## 4. P2 — Safety, scope and persistence foundation

### Objective

Implement the invariants that every later rule relies upon before any active test engine is built.

### Deliverables

- project/target/identity metadata models;
- target allow-list/scope validator;
- redirect scope validator;
- request budget model;
- scan profile model;
- runtime secret references;
- scan state machine;
- evidence redactor skeleton;
- database migrations.

### Required tests

- exact host allowed;
- disallowed host blocked;
- subdomain confusion blocked unless explicitly allowed;
- scheme/port mismatch blocked;
- redirect out of scope blocked;
- request budget cannot be missing/unbounded;
- secret values removed from header/body evidence;
- scan cannot enter `READY` with failed hard preflight.

### Exit criteria

Safety foundation is fully unit-tested and no later network code needs to invent scope logic.

## 5. P3 — Specification ingestion and inventory

### Objective

Import OpenAPI/Postman artefacts and build a normalized operation inventory.

### Deliverables

- OpenAPI 3.x parser/normalizer;
- Postman collection parser for endpoint/auth metadata without script execution;
- spec hashing/provenance;
- parse warnings;
- operation inventory model;
- candidate object-ID/property heuristics as metadata only;
- inventory CLI/UI endpoints;
- import fixtures/tests.

### Exit criteria

- valid OpenAPI fixture imports deterministically;
- malformed spec fails explicitly;
- unsupported constructs produce warnings;
- embedded Postman scripts are not executed;
- inventory output is stable and machine-readable.

## 6. P4 — Laboratory suite and ground truth

### Objective

Build the research targets before scanner detection logic is considered complete.

### Deliverables

- FastAPI mobile-money lab;
- Express revenue/tax lab;
- Spring Boot citizen-services lab;
- Docker Compose orchestration;
- vulnerable/corrected modes;
- seed/reset tooling;
- controlled identities;
- OpenAPI descriptions;
- ground-truth manifests;
- lab functional tests independent of scanner.

### Critical rule

Ground truth is authored from intended seeded behaviour and lab tests, not generated from scanner findings.

### Exit criteria

For every ground-truth case:

- a direct lab test demonstrates vulnerability in vulnerable mode;
- corresponding direct test demonstrates corrected behaviour in corrected mode;
- reset is deterministic;
- no scanner code is needed for lab functional tests.

## 7. P5 — Identity/session and controlled HTTP engine

### Objective

Create the only allowed scanner network execution layer.

### Deliverables

- shared `httpx` client/executor;
- scope revalidation;
- redirect validation;
- per-host concurrency/rate limits;
- total request budget;
- resource-test sub-budget;
- timeouts;
- response capture limits;
- request timings;
- cancellation;
- identity-isolated sessions;
- auth injection from runtime secret references;
- redaction hooks;
- preflight connectivity check.

### Exit criteria

- rule code can perform requests only through controlled context;
- budget exhaustion stops further requests;
- redirect escapes cannot occur;
- secrets do not enter persisted test fixtures/logs;
- cancellation is tested.

## 8. P6 — Authorisation engine

### Objective

Implement the central research contribution first.

### Deliverables

- rule protocol/framework;
- applicability engine;
- differential response comparator;
- fixture/owned-object binding for evaluation;
- `AUTHZ-BOLA-001`;
- `AUTHZ-BOLA-002`;
- `AUTHZ-BFLA-001`;
- `AUTHZ-BFLA-002`;
- `AUTHZ-BOPLA-001`;
- `AUTHZ-BOPLA-002`.

### Exit criteria for each rule

- unit proof-condition tests;
- corrected negative tests;
- budget test;
- evidence redaction test;
- integration test against seeded vulnerable lab;
- integration test against corrected lab;
- confirmed/suspected/inconclusive semantics verified.

### Phase exit criteria

The scanner demonstrates at least one confirmed authorisation finding on each relevant lab without target-language-specific scanner modifications and produces no corresponding confirmed finding on corrected cases.

## 9. P7 — Authentication, configuration, inventory and resource rules

### Deliverables

Authentication:

- `AUTHN-MISSING-001`;
- `AUTHN-INVALID-001`;
- `AUTHN-EXPIRED-001` where deterministic lab fixture exists;
- `AUTHN-SESSION-001` where deterministic lab fixture exists;
- `AUTHN-INCONSISTENT-001`.

Configuration:

- `CONFIG-CORS-001`;
- `CONFIG-HEADERS-001`;
- `CONFIG-TLS-001`;
- `CONFIG-ERROR-001`;
- `CONFIG-METHOD-001`;
- `CONFIG-DOCS-001`.

Inventory:

- `INVENTORY-DIFF-001`;
- `INVENTORY-DIFF-002`;
- `INVENTORY-AUTH-001`.

Resource:

- `RESOURCE-RATE-001`;
- optional `RESOURCE-SIZE-001` if the bounded implementation is useful and safe.

### Exit criteria

Same per-rule test gate as P6. Resource tests additionally require explicit assertions that request ceilings cannot be exceeded.

## 10. P8 — Evidence, findings and reporting

### Objective

Turn observations into auditable research/security output.

### Deliverables

- evidence persistence;
- finding classifier;
- stable finding fingerprints;
- OWASP/CWE mapping registry;
- severity/confidence model;
- canonical JSON report schema;
- CSV exports;
- HTML report;
- limitations/inconclusive sections;
- provenance metadata.

### Exit criteria

- schema validation passes;
- seeded secret values never appear in persisted/exported artefacts;
- confirmed finding contains rule/evidence/provenance/remediation;
- suspected/inconclusive statuses render distinctly;
- report never claims unimplemented OWASP categories are secure.

## 11. P9 — Dashboard and CLI completion

### Dashboard

Implement the journeys defined in `03-USER-JOURNEYS.md` without adding commercial-platform features.

### CLI

Expose the research workflows non-interactively.

Minimum final conceptual capabilities:

```text
project create/list
spec import
inventory list
preflight
scan plan
scan run/stop/show
findings list/show
report export
labs up/reset/status
evaluate run/summary
```

### Exit criteria

A representative scan can be configured and reviewed through the dashboard, while a complete evaluation can run from CLI/scripts with no browser interaction.

## 12. P10 — Evaluation harness and OWASP ZAP baseline

### Deliverables

- evaluation run schema;
- ground-truth matcher;
- TP/FP/FN calculator;
- precision/recall/F1 computation;
- explicit FPR methodology where TN is defined;
- duration/request metrics;
- repeated-run stability calculation;
- cross-stack result summaries;
- pinned/documented ZAP baseline;
- normalized ZAP results;
- result export suitable for dissertation tables/figures.

### Exit criteria

A single documented command/sequence can reset labs, run scanner evaluation, run applicable ZAP baseline, and generate a reproducible summary without manual relabelling.

## 13. P11 — Hardening and final research release

### Work

- dependency/security review;
- false-positive triage based on pre-final test runs without changing ground truth to suit scanner;
- deterministic clean-machine reproduction;
- accessibility/usability cleanup for demo;
- documentation cleanup;
- repeated final experiments;
- archive/tag final evaluation commit;
- generate final aggregate dataset;
- produce diagrams/tables needed by dissertation from the evaluation dataset.

### Exit criteria

All project-completion criteria in `00-PROJECT-CHARTER.md` hold.

## 14. Implementation issue map

After P0 is merged, create one parent tracking issue and phase issues such as:

```text
P1 Foundation
P2 Safety and persistence
P3 Specification inventory
P4 Laboratory suite
P5 Controlled HTTP and identities
P6 Authorisation engine
P7 Remaining scanner rules
P8 Evidence and reporting
P9 Dashboard and CLI
P10 Evaluation and ZAP baseline
P11 Final hardening/research release
```

Break phase issues into smaller implementation issues only when execution reaches that phase. Do not create hundreds of speculative tickets up front.

## 15. Pull request policy

For implementation:

- one coherent active delivery PR per current phase/workstream where practical;
- PR body states scope and acceptance commands;
- all changes pass `make verify` (or canonical replacement) before merge;
- exact PR head used for final verification;
- merge only after checking that no unresolved review/CI findings remain;
- do not mix unrelated refactors/features into a phase PR.

## 16. Definition of a finished task

A task is not finished because code exists. It is finished when:

1. requirement is implemented;
2. automated tests prove positive and negative behaviour;
3. safety invariants are covered where relevant;
4. docs/config examples are updated;
5. canonical verification passes;
6. integration proof exists when the task affects runtime behaviour;
7. no secret or generated sensitive evidence is committed.

## 17. Anti-overengineering rule

Before introducing any of the following, implementation must document why the approved research questions cannot be answered cleanly without it:

- message broker;
- Kubernetes;
- distributed workers;
- microservices split;
- external database server;
- React/SPA frontend;
- cloud deployment requirement;
- LLM/AI dependency;
- multi-tenancy;
- enterprise authentication/RBAC;
- plugin marketplace.

Default answer for this dissertation is **do not add them**.
