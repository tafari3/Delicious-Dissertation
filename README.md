# Delicious Dissertation

Engineering repository for the University of Zimbabwe capstone project **Automated API Security Testing and Misconfiguration Scanner for Zimbabwean E-Government Systems: A Laboratory-Based Evaluation**.

## Final research shape

The topic is unchanged. The artefact is a safe, automated REST API security testing and misconfiguration scanner for Zimbabwean e-government systems. It must identify selected API security weaknesses, preserve reproducible redacted evidence, and automatically generate security assessment reports.

The dissertation uses a staged evaluation:

1. **Controlled laboratory validation** — build one small **Synthetic Government Permit and Service Application API** specifically for the dissertation on the Linux VM already provided by ZCHPC. The lab uses synthetic users/data, vulnerable and corrected states, deterministic reset and independent ground truth.
2. **Authorised ZCHPC cloud validation** — only after the controlled lab gate passes, apply the proven scanner within the exact scope covered by the existing signed ZCHPC authorisation. This stage uses a restricted non-destructive profile and is analysed separately from lab accuracy because complete operational ground truth may not be known.

The scanner must not deliberately introduce weaknesses into the operational ZCHPC environment and must not test assets, tenants, accounts, interfaces, traffic levels or time windows outside the signed scope.

## Core artefact

Planned scanner capabilities include:

- authorised target registration and scope allow-listing;
- OpenAPI/Postman-assisted endpoint inventory;
- isolated controlled identities;
- BOLA, BFLA and BOPLA/mass-assignment checks;
- selected authentication/session checks;
- selected CORS/TLS/security-header/error/method/documentation checks;
- API inventory-drift checks;
- tightly bounded resource-control observations;
- evidence minimisation and secret redaction;
- automatic **HTML and PDF** human-readable reports;
- automatic **JSON and CSV** machine-readable exports;
- OWASP API Security Top 10 / CWE classification and remediation guidance;
- reproducible controlled-lab evaluation and an applicability-aware OWASP ZAP baseline;
- later authorised ZCHPC real-world validation.

## Controlled lab

Canonical lab ID: `government-permit-service-fastapi`

Minimum roles:

- `applicant-a`
- `applicant-b`
- `officer`
- `admin`

Representative operations:

- login/authentication;
- submit permit/service application;
- read/update application;
- officer approval;
- document metadata;
- small admin surface;
- OpenAPI/documentation surface.

The lab is a research testbed, not a replica of a named ministry or public body.

## Current state

Planning has been reconciled to the final proposal. The next implementation phase is **P1 — Repository and runtime foundation** on the existing `phase-1/foundation` branch.

Before AntiGravity starts P1, that branch must point to the same reconciliation commit as `main`, and issue #2 must record the same exact SHA.

## Authoritative documents

Read in this order:

1. `docs/00A-ACADEMIC-PROPOSAL-BASELINE.md`
2. `docs/00-PROJECT-CHARTER.md`
3. `docs/06-SAFETY-SECURITY-MODEL.md`
4. `docs/12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md`
5. `docs/11-RED-TEAM-ATTACK-MATRIX.md`
6. `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`
7. `docs/01-ARCHITECTURE.md`
8. `docs/02-TEST-CATALOGUE.md`
9. `docs/03-USER-JOURNEYS.md`
10. `docs/04-LABS-AND-EVALUATION.md`
11. `docs/05-DATA-AND-REPORTING.md`
12. `docs/08-REQUIREMENTS-TRACEABILITY.md`
13. `docs/09-CONFIGURATION-DEFAULTS.md`
14. `docs/07-IMPLEMENTATION-PLAN.md`
15. `docs/10-REPOSITORY-AND-DELIVERY.md`
16. `docs/14-ANTIGRAVITY-HANDOFF.md`
17. `AGENTS.md`

## Planned repository shape

```text
src/delicious_scanner/
tests/
labs/government-permit-service-fastapi/
evaluation/
reports/
migrations/
scripts/
.github/workflows/
```

## Phase sequence

```text
P1  Repository and runtime foundation
P2  Synthetic permit/service lab and independent ground truth
P3  Specification ingestion and endpoint inventory
P4  Safety, persistence, identity and controlled HTTP execution
P5  Authorisation engine
P6  Authentication/configuration/inventory/resource rules
P7  Evidence, findings and automatic reporting
P8  Dashboard and CLI completion
P9  Controlled laboratory evaluation and OWASP ZAP baseline
P10 Authorised ZCHPC cloud validation and final research release
```

Fintech, mobile-money, healthcare and additional e-government/commercial labs are future work, not current dissertation requirements.
