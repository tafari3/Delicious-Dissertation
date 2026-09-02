# Delicious Dissertation

Engineering repository for the University of Zimbabwe capstone project **Autonomous Cross-Platform Application Programming Interface (API) Security Testing and Misconfiguration Scanner for Zimbabwean Fintech and E-Government Systems**.

## Mission

Build and evaluate a safe, autonomous, cross-platform, black-box REST API security scanner that combines selected authorisation, authentication, configuration, inventory and bounded resource-control checks into one reproducible evidence-producing workflow.

The project is evaluated against deliberately vulnerable synthetic Zimbabwean fintech/e-government laboratory scenarios across multiple technology stacks. It is **not** an uncontrolled penetration-testing framework and must not be used against unauthorised production systems.

## Current state

**Phase 0 — implementation blueprint.**

No scanner implementation should begin until the Phase-0 planning package is merged. After that, AntiGravity should begin **P1 — Repository and runtime foundation** and follow the phase gates in `docs/06-IMPLEMENTATION-PLAN.md`.

## Authoritative planning documents

Read in this order:

1. [`docs/00-PROJECT-CHARTER.md`](docs/00-PROJECT-CHARTER.md) — locked scope, research questions, safety invariants and completion definition.
2. [`docs/02-TEST-CATALOGUE.md`](docs/02-TEST-CATALOGUE.md) — exact bounded scanner rule catalogue and result semantics.
3. [`docs/01-ARCHITECTURE.md`](docs/01-ARCHITECTURE.md) — component boundaries, controlled HTTP execution, identity, inventory and evidence architecture.
4. [`docs/03-USER-JOURNEYS.md`](docs/03-USER-JOURNEYS.md) — operator/dashboard/CLI flows and safety preflight UX.
5. [`docs/04-LABS-AND-EVALUATION.md`](docs/04-LABS-AND-EVALUATION.md) — three-stack laboratories, ground truth, OWASP ZAP baseline and research metrics.
6. [`docs/05-DATA-AND-REPORTING.md`](docs/05-DATA-AND-REPORTING.md) — persistence, redaction, evidence and report schemas.
7. [`docs/06-IMPLEMENTATION-PLAN.md`](docs/06-IMPLEMENTATION-PLAN.md) — phased build sequence and acceptance gates.
8. [`docs/07-REQUIREMENTS-TRACEABILITY.md`](docs/07-REQUIREMENTS-TRACEABILITY.md) — map from proposal commitments/research questions to engineering evidence.
9. [`AGENTS.md`](AGENTS.md) — mandatory AntiGravity/AI-agent execution contract.

## Planned architecture

- Python 3.12+ scanner core;
- `httpx` controlled HTTP executor;
- Pydantic domain/configuration models;
- SQLAlchemy + SQLite local evidence store;
- FastAPI local application surface;
- Typer CLI;
- lightweight server-rendered dashboard;
- Docker Compose laboratory environment;
- FastAPI, Express and Spring Boot synthetic API labs;
- OWASP ZAP comparative baseline;
- JSON/CSV/HTML evidence and evaluation exports.

The scanner must not depend on cloud services, LLM APIs or target source code.

## Planned repository shape

```text
Delicious-Dissertation/
├── AGENTS.md
├── README.md
├── docs/
├── scanner/
├── labs/
│   ├── mobile-money/
│   ├── revenue-tax/
│   └── citizen-services/
├── evaluation/
├── scripts/
├── .github/workflows/
└── Makefile
```

Implementation directories are created in P1/P4 when their acceptance criteria become active; Phase 0 intentionally establishes the contract before scaffolding code.

## Safety boundary

Hard invariants include:

- explicit target allow-listing;
- redirect scope validation;
- hard request/rate ceilings;
- non-destructive default profile;
- disposable fixtures for controlled write tests;
- proof-of-condition stopping;
- credential/token/cookie redaction before persistence/export;
- no credential stuffing, password spraying, destructive/unrestricted fuzzing or DoS testing.

## Implementation sequence

```text
P0 Blueprint
 -> P1 Foundation
 -> P2 Safety/Persistence
 -> P3 Specification/Inventory
 -> P4 Labs/Ground Truth
 -> P5 Controlled HTTP/Identities
 -> P6 Authorisation Engine
 -> P7 Remaining Rules
 -> P8 Evidence/Reporting
 -> P9 Dashboard/CLI
 -> P10 Evaluation/ZAP
 -> P11 Hardening/Final Research Release
```

AntiGravity must follow `AGENTS.md` and the current phase acceptance criteria rather than improvising product scope.
