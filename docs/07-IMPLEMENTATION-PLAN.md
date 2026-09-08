# Implementation Plan and Acceptance Gates

## 1. Delivery principle

AntiGravity implements the dissertation in sequential, verifiable phases. A phase is complete only when its acceptance criteria are proven by automated tests and reproducible commands.

Canonical sequence:

```text
P0  Blueprint / source of truth
P1  Repository and runtime foundation
P2  E-government laboratory suite and independent ground truth
P3  Specification ingestion and endpoint inventory
P4  Safety, persistence, identity and controlled HTTP execution
P5  Authorisation engine
P6  Authentication/configuration/inventory/resource rules
P7  Evidence, findings and reporting
P8  Dashboard and CLI completion
P9  Evaluation harness and OWASP ZAP baseline
P10 Final hardening, repeated experiments and research release
```

Laboratory ground truth is established before scanner detection logic is tuned against it.

Every phase must also satisfy applicable cases in `docs/11-RED-TEAM-ATTACK-MATRIX.md`, locks in `docs/12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md`, and the current academic scope in `docs/00A-ACADEMIC-PROPOSAL-BASELINE.md`.

## 2. P0 — Blueprint / source of truth

### Deliverables

- academic proposal baseline;
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
- adversarial attack matrix and hardening locks;
- laboratory experiment specification;
- AntiGravity VM handoff;
- `AGENTS.md` execution contract.

### Exit gate

- current proposal requirements are traceable into engineering artefacts;
- e-government-only scope is internally consistent;
- lab scenarios and evaluation units are defined before implementation;
- safety/research-integrity boundaries are internally consistent;
- one canonical P1-P10 sequence exists.

## 3. P1 — Repository and runtime foundation

### Objective

Create a clean, installable Python application and deterministic developer/CI command surface without implementing labs or vulnerability rules.

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
- Docker Compose root skeleton;
- `.env.example` and `.gitignore`;
- CI workflow;
- full-SHA pinning for third-party GitHub Actions;
- explicit least-privilege workflow permissions;
- PR verification without privileged secrets;
- repository secret-scanning gate;
- terminal/control-sequence sanitisation baseline;
- documented future target HTTP-client contract with ambient proxy environment ignored by default.

### Stable command contract

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

`make verify` becomes the normal local/CI acceptance command.

### Exit gate

A clean VM can clone, bootstrap, start the app/CLI and pass `make verify` without manually editing source files. Applicable P1 CRITICAL/HIGH adversarial and supply-chain cases pass.

## 4. P2 — E-government laboratory suite and independent ground truth

### Objective

Build the synthetic research targets and independent ground truth before scanner detection logic.

### Required laboratories

- `citizen-records-fastapi` — Python/FastAPI Citizen Records API;
- `public-health-express` — Node.js/Express Public Health Records API;
- `permit-licensing-spring` — Java/Spring Boot Permit & Licensing API.

### Deliverables

- deterministic synthetic fixtures;
- controlled identities/roles from `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`;
- vulnerable and corrected modes;
- OpenAPI artefacts;
- deterministic health/version/mode/fixture metadata;
- seed/reset tooling;
- ground-truth manifests;
- direct lab functional tests independent of scanner code;
- locked/pinned dependency mechanisms for all three lab ecosystems;
- loopback-only canonical publication;
- unprivileged/no-host-network/no-Docker-socket containment;
- no production/external service dependency.

### Critical invariant

The scanner must not be used to define whether a lab is vulnerable. Ground truth comes from intentional seeded behaviour plus direct functional tests.

### Exit gate

For every seeded case:

- vulnerable-mode direct test proves the weakness;
- corrected-mode direct test proves the fix;
- unrelated semantics remain aligned;
- reset is deterministic;
- health/version/mode/fixture metadata is verifiable;
- machine-readable ground truth matches the direct test semantics;
- applicable `RT-LAB-001..004` cases pass.

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
- foundation for documented/undocumented comparisons;
- safe YAML loader;
- external-reference resolution disabled by default;
- import/recursion/reference/decompression ceilings as applicable;
- imported server metadata unable to expand authorised target scope.

### Exit gate

API descriptions from all three labs produce stable normalized inventories and uncertainty is never silently discarded. Applicable parser/import adversarial cases pass.

## 6. P4 — Safety, persistence, identity and controlled HTTP execution

### Objective

Implement every invariant required before a scanner rule can issue target traffic.

### Deliverables

- Project/Target/Specification/Identity metadata models;
- SQLite migrations;
- scan profile model;
- scan lifecycle/state machine;
- target allow-list/scope validator;
- canonical URL/address/path policy;
- actual destination/DNS validation against immutable scope snapshot;
- redirect revalidation;
- runtime secret resolver/references;
- redaction pipeline foundation;
- central `httpx` executor;
- rate/concurrency/total request budgets;
- resource-test sub-budget;
- timeouts and response capture limits;
- isolated identity sessions including clean anonymous context;
- preflight and deterministic scan planner;
- cooperative cancellation;
- ambient proxy environment ignored by default;
- atomic budget reservation under concurrency;
- sanitised exceptions/logging;
- bounded safe file-secret resolution.

### Exit gate

No scanner rule needs or is permitted to create an unrestricted target HTTP client or duplicate scope logic. All applicable P4 CRITICAL/HIGH scope, budget, secret, identity, state and DB adversarial cases pass before P5.

## 7. P5 — Authorisation engine

### Objective

Implement the principal multi-identity authorisation contribution.

### Foundation

- versioned rule protocol;
- applicability engine;
- differential response comparator;
- fixture/owned-object binding for controlled evaluation;
- structured evidence builder;
- complete rule result semantics.

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
8. proof ambiguous behaviour is not mislabeled confirmed;
9. applicable semantic-adversarial tests.

### Exit gate

Rules detect seeded cases across relevant lab stacks without target-language-specific scanner code and do not confirm corresponding corrected cases. Cleanup/reset failure blocks unsafe continuation. Status code, body length or reflected identifiers alone cannot confirm a vulnerability.

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
- optional `RESOURCE-SIZE-001` when useful, deterministic and safely bounded.

### Exit gate

Every implemented rule has deterministic applicability/non-applicability behaviour, positive and corrected/negative evidence where applicable, and resource rules prove hard ceilings under concurrency/failure. Applicable semantic and budget adversarial cases pass.

## 9. P7 — Evidence, findings and reporting

### Deliverables

- redaction-before-persistence pipeline;
- evidence minimisation/size limits;
- finding classifier;
- stable finding fingerprints;
- severity/confidence model;
- OWASP/CWE mapping registry;
- canonical JSON report + JSON Schema;
- CSV research outputs with formula neutralisation;
- human-readable escaped HTML report;
- mandatory limitations/inconclusive/error section;
- provenance metadata;
- safe filesystem export naming;
- explicit persisted-size bounds.

### Exit gate

Synthetic secrets are proven absent from DB evidence, logs, JSON/CSV/HTML exports and snapshots. Applicable report/database/web-output adversarial cases pass.

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

Expose equivalent research workflows non-interactively, including lab/evaluation entrypoints.

### Security requirements

- loopback bind by default;
- Host/authority validation;
- no wildcard/permissive CORS;
- CSRF protection for browser state changes;
- escaped target-controlled content;
- no resolved secret returned/rendered;
- safe download/export path handling;
- terminal-control sanitisation.

### Exit gate

A representative scan can be configured/reviewed from the browser while complete research evaluation remains runnable without browser interaction. Applicable local-web adversarial cases pass.

## 11. P9 — Evaluation harness and OWASP ZAP baseline

### Deliverables

- deterministic evaluation runner;
- lab reset/version/mode/fixture verification;
- evaluation-only ground-truth ingestion;
- architectural separation preventing detector access to ground truth;
- deterministic finding-to-case matcher using the case tuple in `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`;
- TP/FP/FN/TN calculations where defensible;
- precision/recall/F1;
- explicit FPR method when TN is valid;
- frozen treatment of `SUSPECTED`, `INCONCLUSIVE`, `ERROR` and `NOT_APPLICABLE` for headline/secondary metrics;
- request count/duration metrics;
- repeated-run stability;
- cross-stack summaries;
- pinned/documented OWASP ZAP baseline;
- ZAP applicability states (`EQUIVALENTLY_TESTABLE`, `PARTIALLY_TESTABLE`, `NOT_EQUIVALENTLY_TESTABLE`);
- normalized ZAP output;
- JSON/CSV datasets suitable for dissertation analysis;
- retention of unexpected findings and invalid/failed runs with reasons.

### Exit gate

One documented command/sequence resets labs, runs scanner evaluation, runs applicable ZAP baseline and produces metrics tied to exact scanner/lab/ground-truth/matcher/spec/profile versions without manual result relabelling. Applicable research-integrity adversarial cases pass.

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
- dissertation figures/tables generated from canonical evaluation output;
- freeze ground truth, case tuples, matching logic, metric/state-treatment rules and ZAP configuration before final collection;
- retain failed/flaky/inconvenient runs with explicit validity/exclusion reason;
- optional authorised ZCHPC deployment of the student's own labs only if permission exists and schedule permits.

### Exit gate

All charter completion criteria hold and another technically competent person can reproduce the dissertation demonstration/evaluation without undocumented manual steps. All applicable CRITICAL/HIGH adversarial cases pass.

## 13. Issue model

Maintain one phase issue for P1-P10. Create smaller issues only when an independent slice/dependency actually appears.

Do not create hundreds of speculative tasks.

## 14. Pull request gate

For implementation:

- use one coherent active delivery PR per current phase/slice where practical;
- state objective, acceptance criteria and verification commands;
- list applicable adversarial cases/results;
- run verification against exact PR head;
- resolve real CI/review/adversarial failures on the same PR;
- do not mix unrelated refactors/features;
- merge only when phase-specific evidence is reproducible.

## 15. Definition of a finished task

Code existing is not enough. A task is finished only when:

1. requirement is implemented;
2. positive and negative automated tests exist;
3. relevant safety invariants are proven;
4. applicable CRITICAL/HIGH adversarial cases are proven;
5. docs/config examples are updated;
6. canonical verification passes;
7. runtime/lab integration evidence exists where applicable;
8. no secret, real personal data or sensitive generated evidence is committed.

## 16. Anti-overengineering rule

Do not introduce message brokers, Kubernetes, distributed workers, external DB infrastructure, SPA frameworks, cloud dependencies, LLM services, multi-tenancy or enterprise platform features unless the approved research questions demonstrably cannot be answered without them.

## 17. Scope lock

Do not reintroduce fintech/digital-payment laboratories into P1-P10. Fintech is future work.

Do not make ZCHPC access a dependency. Any ZCHPC work is optional authorised hosting of the student's isolated labs, not assessment of production infrastructure.

## 18. Adversarial phase gate

`docs/11-RED-TEAM-ATTACK-MATRIX.md` is mandatory. A phase cannot close while an applicable CRITICAL/HIGH case is untested/failing unless genuine non-applicability is documented without weakening a hard safety/research requirement.
