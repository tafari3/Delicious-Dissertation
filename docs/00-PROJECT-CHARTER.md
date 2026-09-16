# Project Charter and Locked Scope

## 1. Project identity

**Repository:** `tafari3/Delicious-Dissertation`

**Academic project:** *Automated API Security Testing and Misconfiguration Scanner for Zimbabwean E-Government Systems: A Cloud-Based Evaluation*

The artefact is a local-first REST API security testing and misconfiguration scanner. It operates through explicitly authorised interfaces, available API descriptions and controlled identities; it does not require target source code.

The scanner remains the contribution. The cloud provides the controlled and operational evaluation environments.

## 2. Finished product definition

The completed scanner must be able to:

1. register an explicitly authorised target and immutable scan scope;
2. import OpenAPI/Postman descriptions where available;
3. build a normalised endpoint inventory;
4. configure isolated controlled identities;
5. run a bounded, non-destructive-by-default test catalogue;
6. test selected BOLA/BFLA/BOPLA, authentication/session, configuration, inventory and bounded deployment conditions;
7. preserve minimal redacted evidence and complete result states;
8. classify findings by severity/confidence and OWASP/CWE mapping;
9. automatically generate HTML, PDF, JSON and CSV reports with remediation guidance;
10. evaluate against independent controlled-cloud ground truth and an applicability-aware OWASP ZAP baseline;
11. after the controlled gate passes, validate within the exact authorised ZCHPC operational scope.

## 3. Stage 1 — controlled replica cloud

The dissertation uses one application lab inside a small controlled **XCP-ng + Xen Orchestra** cloud, not three application labs.

**Lab:** Synthetic Government Permit and Service Application API

**Engineering ID:** `government-permit-service-fastapi`

**Default stack:** Python/FastAPI + small relational database.

The controlled virtualisation layer uses XCP-ng. Xen Orchestra provides management/orchestration and is not treated as the hypervisor. The exact lab VM count may be adapted to available resources, but the scanner and synthetic target remain logically distinct and the design preserves a separate management boundary wherever the infrastructure permits.

Expected logical roles are scanner, synthetic API and database/supporting service, plus Xen Orchestra management. A separate database VM is preferred when resources permit; colocating the database with the API is acceptable if documented and does not invalidate a seeded network case.

Roles: two applicants for cross-user tests, officer and administrator.

The application uses only synthetic data and has vulnerable/corrected states, deterministic reset, OpenAPI, direct contract tests and independent ground truth.

The replica cloud may also contain selected reversible deployment/network misconfigurations with predeclared expected secure states. It is not a destructive hypervisor exploitation environment.

## 4. Stage 2 — ZCHPC operational validation

ZCHPC validation is the real-world validation stage after controlled replica-cloud success. Signed project authorisation exists, but every run must still match an explicit local scope definition reflecting the approved assets/interfaces/accounts/traffic/time window.

The operational environment is never deliberately made vulnerable for the dissertation. No claim may extrapolate a limited authorised scan into certification or a complete assessment of the entire ZCHPC cloud.

## 5. Safety invariants

Hard requirements:

- explicit allow-list and destination/scope validation;
- one controlled HTTP executor;
- request/rate/concurrency budgets;
- non-destructive default;
- disposable lab objects for mutation checks;
- proof-of-condition stopping;
- redaction before persistence/export;
- no credential stuffing/password spraying;
- no destructive/unrestricted fuzzing;
- no denial-of-service, VM escape, persistence or lateral movement;
- no unrelated ZCHPC tenants/assets;
- no scanner access to controlled ground truth during detection.

## 6. Evaluation acceptance

The controlled replica cloud must support deterministic TP/FP/FN and defensible TN/FPR measurement, precision, recall, F1, scan duration, request counts, error/inconclusive states and repeated-run/report reproducibility.

Ground truth is established independently using direct application tests and direct lab configuration/reachability checks. It is frozen before final evaluation.

ZCHPC validation records applicability, repeatability, evidence quality, confirmed/suspected/inconclusive observations and operational constraints separately.

## 7. Completion criteria

Project completion requires:

- clean installation/reproduction;
- enforced safety preflight;
- working inventory and identity handling;
- implemented bounded test catalogue;
- one reproducible synthetic application lab inside the controlled XCP-ng/Xen Orchestra environment;
- selected controlled deployment/cloud cases with frozen independent ground truth;
- automatic HTML/PDF/JSON/CSV reporting;
- controlled-cloud accuracy evaluation and applicable ZAP comparison;
- authorised ZCHPC validation performed only after the controlled gate and only within signed scope;
- final research dataset/provenance sufficient for examiner reproduction;
- no real credentials or confidential target evidence committed.

## 8. Delimitations

Not required for this dissertation: three implementation stacks, extra government application labs, fintech/mobile-money/healthcare labs, SAST, comprehensive GraphQL/SOAP/gRPC, unrestricted penetration testing, hypervisor exploitation, production SaaS or LLM services.

Future commercialisation may add those environments after the dissertation.
