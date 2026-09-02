# Delicious Dissertation

Engineering repository for the University of Zimbabwe capstone project **Autonomous Cross-Platform Application Programming Interface (API) Security Testing and Misconfiguration Scanner for Zimbabwean Fintech and E-Government Systems**.

## Mission

Build and evaluate a safe, autonomous, cross-platform, black-box REST API security scanner that combines selected authorisation, authentication, configuration, inventory and bounded resource-control checks into one reproducible evidence-producing workflow.

The project is evaluated against deliberately vulnerable synthetic Zimbabwean fintech/e-government laboratory scenarios across multiple technology stacks. It is **not** an uncontrolled penetration-testing framework and must not be used against unauthorised production systems.

## Current state

**Phase 0 — implementation blueprint.**

No scanner implementation should begin until the Phase-0 planning package is merged. After that, AntiGravity begins **P1 — Repository and runtime foundation** from exact `main` and follows `docs/07-IMPLEMENTATION-PLAN.md`.

## Authoritative planning documents

Read in this order:

1. [`docs/00-PROJECT-CHARTER.md`](docs/00-PROJECT-CHARTER.md) — locked project scope, research questions and completion definition.
2. [`docs/06-SAFETY-SECURITY-MODEL.md`](docs/06-SAFETY-SECURITY-MODEL.md) — hard safety, ethics, scope and evidence invariants.
3. [`docs/01-ARCHITECTURE.md`](docs/01-ARCHITECTURE.md) — component boundaries, controlled HTTP execution, identity, inventory and evidence architecture.
4. [`docs/02-TEST-CATALOGUE.md`](docs/02-TEST-CATALOGUE.md) — bounded scanner rules, proof conditions, result semantics and stop conditions.
5. [`docs/03-USER-JOURNEYS.md`](docs/03-USER-JOURNEYS.md) — operator/dashboard/CLI workflows and safety-preflight UX.
6. [`docs/04-LABS-AND-EVALUATION.md`](docs/04-LABS-AND-EVALUATION.md) — three-stack laboratories, independent ground truth, OWASP ZAP baseline and research metrics.
7. [`docs/05-DATA-AND-REPORTING.md`](docs/05-DATA-AND-REPORTING.md) — persistence, redaction, evidence, findings and report schemas.
8. [`docs/08-REQUIREMENTS-TRACEABILITY.md`](docs/08-REQUIREMENTS-TRACEABILITY.md) — map from proposal objectives/research questions to engineering and evaluation evidence.
9. [`docs/09-CONFIGURATION-DEFAULTS.md`](docs/09-CONFIGURATION-DEFAULTS.md) — initial ports, request ceilings, evidence limits and scan-profile defaults.
10. [`docs/07-IMPLEMENTATION-PLAN.md`](docs/07-IMPLEMENTATION-PLAN.md) — canonical P0–P10 build sequence and acceptance gates.
11. [`docs/10-REPOSITORY-AND-DELIVERY.md`](docs/10-REPOSITORY-AND-DELIVERY.md) — repository layout, Git/CI model and AntiGravity handoff workflow.
12. [`AGENTS.md`](AGENTS.md) — mandatory AntiGravity/AI-agent execution contract.

## Planned architecture

- Python scanner/application core;
- `httpx` controlled HTTP executor;
- typed Pydantic configuration/domain models;
- SQLAlchemy + SQLite local evidence store;
- FastAPI local application surface;
- Typer CLI;
- lightweight server-rendered dashboard;
- Docker Compose laboratory environment;
- FastAPI mobile-money laboratory;
- Express revenue/tax laboratory;
- Spring Boot citizen-services laboratory;
- OWASP ZAP comparative baseline;
- JSON/CSV/HTML evidence and evaluation exports.

The scanner must not depend on cloud services, LLM APIs or target source code.

## Planned repository shape

```text
Delicious-Dissertation/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── Makefile
├── docker-compose.yml
├── docs/
├── src/delicious_scanner/
├── tests/
├── labs/
│   ├── mobile-money-fastapi/
│   ├── revenue-express/
│   └── citizen-services-spring/
├── evaluation/
├── scripts/
├── migrations/
└── .github/workflows/
```

Implementation directories are created when their phase becomes active; Phase 0 intentionally establishes the contract before scaffolding product code.

## Safety boundary

Hard invariants include:

- explicit target allow-listing;
- redirect scope validation;
- hard request/rate ceilings;
- one controlled HTTP execution path;
- non-destructive default profile;
- disposable fixtures for controlled write tests;
- proof-of-condition stopping;
- credential/token/cookie redaction before persistence/export;
- no credential stuffing, password spraying, destructive/unrestricted fuzzing or DoS testing.

## Canonical implementation sequence

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

AntiGravity must follow `AGENTS.md`, the current phase issue and the exact phase acceptance criteria rather than improvising product scope.