# Implementation Plan and Acceptance Gates

## 1. Delivery principle

AntiGravity implements the dissertation in sequential, verifiable phases. A phase is complete only when its acceptance criteria are proven by automated tests and reproducible commands.

The canonical sequence is:

```text
P0  Blueprint / source of truth
P1  Repository and runtime foundation
P2  Laboratory suite and independent ground truth
P3  Specification ingestion and endpoint inventory
P4  Safety, persistence, identity and controlled HTTP execution
P5  Authorisation engine
P6  Authentication/configuration/inventory/resource rules
P7  Evidence, findings and reporting
P8  Dashboard and CLI completion
P9  Evaluation harness and OWASP ZAP baseline
P10 Final hardening, repeated experiments and research release
```

The sequence deliberately establishes laboratory ground truth before scanner detection logic is tuned against it.

## 2. P0 — Blueprint / source of truth

### Deliverables

- project charter;
- architecture;
- test catalogue;
- user journeys;
- labs/evaluation protocol;
- data/reporting model;
- safety/security model;
- implementation plan;
- requirements traceability;
- repository/delivery model;
- `AGENTS.md` AntiGravity contract.

### Exit gate

- proposal requirements are traceable into engineering artefacts;
- safety boundaries are internally consistent;
- one canonical implementation sequence exists;
- no scanner implementation is required yet.

## 3. P1 — Repository and runtime foundation

### Objective

Create a clean, installable Python application and deterministic developer/CI command surface.

### Target layout

```text
pyproject.toml
Makefile
src/delicious_scanner/
tests/
labs/
evaluation/
scripts/
migrations/
.github/workflows/
```

### Requirements

- Python 3.12+;
- one locked dependency workflow, preferably `uv` unless a concrete blocker exists;
- package under `src/delicious_scanner/`;
- FastAPI health endpoint;
- Typer CLI with version/health command;
- SQLAlchemy 2.x and migration framework;
- SQLite development database;
- structured secret-safe logging baseline;
- pytest;
- Ruff formatting/linting;
- type checking with mypy or pyright;
- Docker Compose root entrypoint;
- CI workflow.

### Stable command contract

Expose wrappers equivalent to:

```text
make bootstrap
make format
make lint
make typecheck
make test
make verify
make app
make labs-up
make labs-down
```

`make verify` becomes the canonical local/CI acceptance command.

### Exit gate

A clean VM can clone, bootstrap, start the app/CLI and pass `make verify` without manually editing source files.

## 4. P2 — Laboratory suite and independent ground truth

### Objective

Build the synthetic research targets before scanner detection logic.

### Deliverables

- FastAPI mobile-money lab;
- Express revenue/tax lab;
- Spring Boot citizen-services lab;
- deterministic synthetic fixtures;
- controlled identities and roles;
- vulnerable and corrected modes;
- OpenAPI artefacts;
- seed/reset tooling;
- ground-truth manifests;
- direct lab functional tests independent of scanner code.

### Critical invariant

The scanner must not be used to define whether the lab is vulnerable. Ground truth is authored from the intentional seeded behaviour and direct functional tests.

### Exit gate

For every seeded case:

- vulnerable mode direct test proves the weakness;
- corrected mode direct test proves corrected behaviour;
- reset is deterministic;
- health/version/mode can be verified automatically.

## 5. P3 — Specification ingestion and endpoint inventory

### Objective

Create specification-assisted, source-language-independent inventory before active security rules.

### Deliverables

- OpenAPI 3.x parser/normaliser;
- Postman collection importer without script execution;
- specification hashing/provenance;
- parse warnings and unsupported-construct handling;
- normalized operation inventory;
- declared-auth metadata;
- candidate object-ID/property annotations;
- foundation for documented/undocumented comparisons.

### Exit gate

Representative API descriptions from all three labs produce stable normalized inventories and parsing uncertainty is never silently discarded.

## 6. P4 — Safety, persistence, identity and controlled HTTP execution

### Objective

Implement every invariant required before any scanner rule can issue traffic.

### Deliverables

- Project/Target/Specification/Identity metadata models;
- SQLite migrations;
- scan profile model;
- scan lifecycle/state machine;
- target allow-list/scope validator;
- redirect revalidation;
- runtime secret resolver/references;
- redaction pipeline foundation;
- central `httpx` executor;
- rate/concurrency/total request budgets;
- resource-test sub-budget;
- timeouts and response capture limits;
- isolated identity sessions;
- preflight and scan planner;
- cooperative cancellation.

### Required safety tests

- allowed host works;
- disallowed host blocked;
- scheme/port/base-path escapes blocked;
- redirects leaving scope blocked;
- missing/unbounded budgets rejected;
- mutation profile rejected for non-disposable targets;
- known fixture secrets removed before persistence/logging;
- budget exhaustion prevents additional requests;
- failed hard preflight cannot become `READY`.

### Exit gate

No scanner rule needs or is permitted to create its own unrestricted HTTP client or scope logic.

## 7. P5 — Authorisation engine

### Objective

Implement the principal research contribution.

### Foundation

- versioned rule protocol;
- applicability engine;
- differential response comparator;
- fixture/owned-object binding for controlled evaluation;
- structured evidence builder;
- result semantics (`CONFIRMED`, `SUSPECTED`, `INCONCLUSIVE`, etc.).

### Minimum rules

- `AUTHZ-BOLA-001` cross-user object read;
- `AUTHZ-BOLA-002` controlled cross-user mutation;
- `AUTHZ-BFLA-001` low-privilege privileged function;
- `AUTHZ-BFLA-002` anonymous privileged function;
- `AUTHZ-BOPLA-001` protected-property exposure;
- `AUTHZ-BOPLA-002` controlled mass assignment.

### Rule completion gate

Every rule requires:

1. applicability tests;
2. proof-condition tests;
3. corrected negative tests;
4. request-budget test;
5. evidence-redaction test;
6. integration proof against vulnerable lab case;
7. integration proof against corrected behaviour;
8. proof that ambiguous behaviour is not mislabelled confirmed.

### Phase exit gate

Authorisation rules detect their seeded cases across the relevant lab stacks without target-language-specific scanner code and do not confirm corresponding corrected cases.

## 8. P6 — Authentication, configuration, inventory and bounded resource rules

Implement the remaining locked catalogue:

### Authentication

- `AUTHN-MISSING-001`;
- `AUTHN-INVALID-001`;
- `AUTHN-EXPIRED-001` where deterministic fixture exists;
- `AUTHN-SESSION-001` where deterministic fixture exists;
- `AUTHN-INCONSISTENT-001`.

### Configuration

- `CONFIG-CORS-001`;
- `CONFIG-HEADERS-001`;
- `CONFIG-TLS-001`;
- `CONFIG-ERROR-001`;
- `CONFIG-METHOD-001`;
- `CONFIG-DOCS-001`.

### Inventory

- `INVENTORY-DIFF-001`;
- `INVENTORY-DIFF-002`;
- `INVENTORY-AUTH-001`.

### Resource control

- `RESOURCE-RATE-001`;
- optional `RESOURCE-SIZE-001` when demonstrably useful and bounded.

### Exit gate

Every implemented rule has deterministic applicability/non-applicability behaviour, positive and corrected/negative evidence where applicable, and resource rules prove their hard ceilings cannot be exceeded.

## 9. P7 — Evidence, findings and reporting

### Deliverables

- redaction-before-persistence pipeline;
- evidence minimisation/size limits;
- finding classifier;
- stable finding fingerprints;
- severity/confidence model;
- OWASP/CWE mapping registry;
- canonical JSON report + JSON Schema;
- CSV research outputs;
- human-readable HTML report;
- limitations/inconclusive section;
- provenance metadata.

### Exit gate

Automated tests inject known dummy secrets and prove they do not appear in database evidence, logs, JSON/CSV/HTML exports or test snapshots.

A confirmed finding contains rule/version, endpoint, expected/observed behaviour, redacted proof, mapping, remediation and reproduction guidance.

## 10. P8 — Dashboard and CLI completion

### Dashboard journeys

Implement the flows in `03-USER-JOURNEYS.md`:

1. project list/create;
2. target/scope configuration;
3. specification import;
4. inventory review;
5. identity configuration;
6. scan profile and safety preflight;
7. plan review;
8. run/stop/status;
9. findings list/detail;
10. report/export.

### CLI

Expose equivalent research workflows non-interactively, including lab/evaluation commands.

The UI must remain a thin layer over the same application services used by the CLI.

### Exit gate

A representative scan can be configured/reviewed from the browser, while the complete research evaluation can run without browser interaction.

## 11. P9 — Evaluation harness and OWASP ZAP baseline

### Deliverables

- deterministic evaluation runner;
- lab reset/version verification;
- ground-truth matcher;
- TP/FP/FN calculation;
- precision/recall/F1;
- explicit FPR method when TN is defined;
- request count/duration metrics;
- repeated-run stability;
- cross-stack summaries;
- pinned/documented OWASP ZAP baseline;
- normalized ZAP output;
- JSON/CSV datasets suitable for dissertation analysis.

### Exit gate

One documented command/sequence can reset labs, run scanner evaluation, run applicable ZAP baseline and produce metrics tied to exact scanner commit, lab version and ground-truth hash without manual result relabelling.

## 12. P10 — Final hardening, repeated experiments and research release

### Work

- dependency/security review;
- false-positive triage without changing ground truth to suit scanner;
- clean-environment reproduction;
- final UI/demo cleanup;
- documentation/reproduction guide;
- repeated final evaluation runs;
- immutable tag/commit for final experiment;
- final aggregate dataset;
- dissertation figures/tables generated from canonical evaluation output.

### Exit gate

All completion criteria in `00-PROJECT-CHARTER.md` hold and another technically competent person can reproduce the dissertation demonstration/evaluation without undocumented manual steps.

## 13. Issue model

After P0 is merged, create one parent implementation tracker plus one issue per phase P1–P10. Create smaller issues only when work reaches the phase and an independent slice is actually needed.

Do not create hundreds of speculative tasks.

## 14. Pull request gate

For implementation:

- use one coherent active delivery PR per current phase/slice where practical;
- state objective, acceptance criteria and verification commands in the PR;
- run verification against the exact PR head;
- resolve real CI/review findings on the same PR;
- do not mix unrelated refactors/features;
- merge only when the phase-specific evidence is reproducible.

## 15. Definition of a finished task

Code existing is not enough. A task is finished only when:

1. requirement is implemented;
2. positive and negative automated tests exist;
3. relevant safety invariants are proven;
4. docs/config examples are updated;
5. canonical verification passes;
6. runtime/lab integration evidence exists where applicable;
7. no secret/sensitive generated evidence is committed.

## 16. Anti-overengineering rule

Do not introduce message brokers, Kubernetes, distributed workers, external DB infrastructure, SPA frameworks, cloud dependencies, LLM services, multi-tenancy or enterprise platform features unless the approved research questions demonstrably cannot be answered without them.
