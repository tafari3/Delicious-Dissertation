# Delicious Dissertation

Engineering repository for the University of Zimbabwe capstone project **Automated API Security and Misconfiguration Scanner for Zimbabwean E-Government Systems: A Laboratory-Based Evaluation**.

## Mission

Build and evaluate a safe, automated REST API security scanner for representative Zimbabwean e-government workflows. The scanner combines selected authorisation, authentication/session, configuration, inventory and bounded resource-control checks into one reproducible evidence-producing workflow.

The project is evaluated against deliberately vulnerable **synthetic e-government laboratories** across multiple technology stacks. The laboratories use invented records and controlled identities; they are representative public-service workflows, not replicas of any named government system. The project is **not** an uncontrolled penetration-testing framework and must not be used against unauthorised production systems.

Fintech and digital-payment APIs are outside the current dissertation evaluation and are reserved for future work.

## Current state

Planning, adversarial review and the e-government scope lock are complete. The next implementation phase is **P1 — Repository and runtime foundation** on the existing `phase-1/foundation` branch.

Before AntiGravity starts P1, `phase-1/foundation` must point to the same commit as `main`. Issue #2 contains the exact handoff commit for the active phase.

## Authoritative planning documents

Read in this order:

1. [`docs/00A-ACADEMIC-PROPOSAL-BASELINE.md`](docs/00A-ACADEMIC-PROPOSAL-BASELINE.md) — submission proposal baseline, terminology, current scope and research commitments.
2. [`docs/00-PROJECT-CHARTER.md`](docs/00-PROJECT-CHARTER.md) — locked engineering scope, research questions and completion definition.
3. [`docs/06-SAFETY-SECURITY-MODEL.md`](docs/06-SAFETY-SECURITY-MODEL.md) — hard safety, ethics, scope and evidence invariants.
4. [`docs/12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md`](docs/12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md) — mandatory controls introduced by adversarial review.
5. [`docs/11-RED-TEAM-ATTACK-MATRIX.md`](docs/11-RED-TEAM-ATTACK-MATRIX.md) — adversarial acceptance catalogue covering the scanner, labs, UI, reports, evaluation and CI.
6. [`docs/13-LAB-EXPERIMENT-SPECIFICATION.md`](docs/13-LAB-EXPERIMENT-SPECIFICATION.md) — frozen laboratory roles, endpoint contracts, seeded cases and primary evaluation units.
7. [`docs/01-ARCHITECTURE.md`](docs/01-ARCHITECTURE.md) — component boundaries, controlled HTTP execution, identity, inventory and evidence architecture.
8. [`docs/02-TEST-CATALOGUE.md`](docs/02-TEST-CATALOGUE.md) — bounded scanner rules, proof conditions, result semantics and stop conditions.
9. [`docs/03-USER-JOURNEYS.md`](docs/03-USER-JOURNEYS.md) — operator/dashboard/CLI workflows and safety-preflight UX.
10. [`docs/04-LABS-AND-EVALUATION.md`](docs/04-LABS-AND-EVALUATION.md) — three-stack laboratories, independent ground truth, OWASP ZAP baseline and research metrics.
11. [`docs/05-DATA-AND-REPORTING.md`](docs/05-DATA-AND-REPORTING.md) — persistence, redaction, evidence, findings and report schemas.
12. [`docs/08-REQUIREMENTS-TRACEABILITY.md`](docs/08-REQUIREMENTS-TRACEABILITY.md) — map from proposal objectives/research questions to engineering and evaluation evidence.
13. [`docs/09-CONFIGURATION-DEFAULTS.md`](docs/09-CONFIGURATION-DEFAULTS.md) — initial ports, request ceilings, evidence limits and scan-profile defaults.
14. [`docs/07-IMPLEMENTATION-PLAN.md`](docs/07-IMPLEMENTATION-PLAN.md) — canonical P0–P10 build sequence with mandatory adversarial gates.
15. [`docs/10-REPOSITORY-AND-DELIVERY.md`](docs/10-REPOSITORY-AND-DELIVERY.md) — repository layout, Git/CI model and delivery workflow.
16. [`docs/14-ANTIGRAVITY-HANDOFF.md`](docs/14-ANTIGRAVITY-HANDOFF.md) — exact no-chat-context execution procedure for the VM.
17. [`AGENTS.md`](AGENTS.md) — mandatory AntiGravity/AI-agent execution contract.

If a future supervisor-approved academic change alters scope, update the proposal baseline, charter, traceability, lab specification, affected phase issues and implementation docs in one reviewed change before continuing implementation.

## Planned architecture

- Python scanner/application core;
- `httpx` controlled HTTP executor;
- typed Pydantic configuration/domain models;
- SQLAlchemy + SQLite local evidence store;
- FastAPI local application surface;
- Typer CLI;
- lightweight server-rendered dashboard;
- Docker Compose laboratory environment;
- FastAPI **Citizen Records** laboratory;
- Express **Public Health Records** laboratory;
- Spring Boot **Permit & Licensing** laboratory;
- OWASP ZAP comparative baseline;
- JSON/CSV/HTML evidence and evaluation exports.

The scanner must not depend on cloud services, LLM APIs or target source code. An authorised ZCHPC resource may optionally host an isolated copy of the student's own laboratory environment; ZCHPC production systems are not project targets.

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
│   ├── unit/
│   ├── integration/
│   ├── safety/
│   ├── red_team/
│   └── acceptance/
├── labs/
│   ├── citizen-records-fastapi/
│   ├── public-health-express/
│   └── permit-licensing-spring/
├── evaluation/
├── scripts/
├── migrations/
└── .github/workflows/
```

Implementation directories are created when their phase becomes active; the blueprint and adversarial contract intentionally exist before product scaffolding.

## Safety boundary

Hard invariants include:

- explicit target allow-listing;
- canonical URL/address/path validation;
- DNS/destination validation against immutable scan scope;
- redirect scope validation before transmission;
- ambient proxy environment ignored by default;
- hard atomic request/rate/resource ceilings;
- one controlled HTTP execution path;
- non-destructive default profile;
- disposable fixtures for controlled write tests;
- proof-of-condition stopping;
- credential/token/cookie redaction before persistence/export;
- safe specification parsing with external reference fetching disabled by default;
- loopback-contained vulnerable labs;
- CSRF/Host/CORS/output-escaping protection for the local dashboard;
- report/CSV/terminal injection hardening;
- least-privilege, SHA-pinned CI;
- no credential stuffing, password spraying, destructive/unrestricted fuzzing or denial-of-service testing.

## Canonical implementation sequence

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

AntiGravity must follow `AGENTS.md`, the active phase issue, the exact phase acceptance criteria and the applicable adversarial attack IDs rather than improvising product scope.
