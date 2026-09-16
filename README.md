# Delicious Dissertation

Engineering repository for the University of Zimbabwe capstone project **Automated API Security Testing and Misconfiguration Scanner for Zimbabwean E-Government Systems: A Cloud-Based Evaluation**.

## Final research shape

The artefact is a safe, automated REST API security testing and misconfiguration scanner for Zimbabwean e-government systems. It must identify selected API security weaknesses, preserve reproducible redacted evidence, and automatically generate security assessment reports.

The cloud is the evaluation environment, not a replacement contribution. The scanner remains the primary research artefact.

The dissertation uses a two-stage evaluation:

1. **Controlled replica-cloud validation** — build a small **XCP-ng + Xen Orchestra** research cloud with a few VMs, then deploy one **Synthetic Government Permit and Service Application API** and the scanner inside that controlled environment. The lab uses synthetic users/data, vulnerable and corrected states, deterministic reset, selected deliberately seeded API/deployment weaknesses and independent frozen ground truth.
2. **Authorised ZCHPC cloud validation** — only after the controlled replica-cloud gate passes, apply the proven scanner within the exact scope covered by the existing signed ZCHPC authorisation. This stage uses a restricted non-destructive profile and is analysed separately from controlled accuracy because complete operational ground truth may not be known.

XCP-ng is the hypervisor. Xen Orchestra is the management/orchestration layer and may run as a VM/appliance or on another approved management node. The controlled cloud should resemble the relevant ZCHPC virtualisation pattern without claiming to be an exact production clone.

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
- selected safe deployment/cloud misconfiguration observations where they are deterministic and within scope;
- evidence minimisation and secret redaction;
- automatic **HTML and PDF** human-readable reports;
- automatic **JSON and CSV** machine-readable exports;
- OWASP API Security Top 10 / CWE classification and remediation guidance;
- reproducible controlled-cloud evaluation and an applicability-aware OWASP ZAP baseline;
- later authorised ZCHPC real-world validation.

NIST and ISO mappings are contextual/informative only; the project does not claim to certify compliance.

## Controlled replica cloud

Canonical application lab ID: `government-permit-service-fastapi`.

Minimum logical deployment roles:

- XCP-ng host providing the controlled virtualisation layer;
- Xen Orchestra management/orchestration service;
- scanner VM;
- synthetic e-government API VM;
- database/supporting service either on a separate VM or colocated with the API VM if resources require it.

The scanner and target must remain logically distinguishable even if a constrained lab consolidates supporting services. Management access should be separated from the service/test network wherever the available infrastructure permits.

Minimum application roles:

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

## Ground truth and cloud cases

Application and selected deployment/cloud cases are declared before final scanner tuning. Example case classes include object/function/property authorisation, authentication, CORS, error handling, documentation exposure, inventory drift, exposed management/service ports, incorrect network reachability, insecure service binding and other bounded deployment observations that can be safely created and corrected in the replica cloud.

Ground truth is established independently through direct lab/configuration proof. Scanner detector logic cannot read the ground-truth manifest when deciding whether a condition exists.

## Current state

Planning is being reconciled to the final two-stage cloud evaluation design. After this reconciliation is integrated, **P1 — Repository and runtime foundation** continues on the existing `phase-1/foundation` branch.

Before P1 starts, that branch must point to the exact integrated reconciliation commit recorded in issue #2.

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
infra/replica-cloud/
reports/
migrations/
scripts/
.github/workflows/
```

## Phase sequence

```text
P1  Repository and runtime foundation
P2  Synthetic permit/service lab, replica-cloud deployment definition and independent ground truth
P3  Specification ingestion and endpoint inventory
P4  Safety, persistence, identity and controlled HTTP execution
P5  Authorisation engine
P6  Authentication/configuration/inventory/resource rules
P7  Evidence, findings and automatic reporting
P8  Dashboard and CLI completion
P9  Controlled XCP-ng/Xen Orchestra cloud evaluation and OWASP ZAP baseline
P10 Authorised ZCHPC cloud validation and final research release
```

Fintech, mobile-money, healthcare and additional e-government/commercial labs are future work, not current dissertation requirements.
