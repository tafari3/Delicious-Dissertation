# Project Charter and Locked Scope

## 1. Project identity

**Repository:** `tafari3/Delicious-Dissertation`

**Academic project:** *Automated API Security Testing and Misconfiguration Scanner for Zimbabwean E-Government Systems: A Laboratory-Based Evaluation*

The artefact is a local-first REST API security testing and misconfiguration scanner. It operates through explicitly authorised interfaces, available API descriptions and controlled identities; it does not require target source code.

## 2. Finished product definition

The completed scanner must be able to:

1. register an explicitly authorised target and immutable scan scope;
2. import OpenAPI/Postman descriptions where available;
3. build a normalised endpoint inventory;
4. configure isolated controlled identities;
5. run a bounded, non-destructive-by-default test catalogue;
6. test selected BOLA/BFLA/BOPLA, authentication/session, configuration and inventory conditions;
7. preserve minimal redacted evidence and complete result states;
8. classify findings by severity/confidence and OWASP/CWE mapping;
9. automatically generate HTML, PDF, JSON and CSV reports with remediation guidance;
10. evaluate against independent synthetic ground truth and an applicability-aware OWASP ZAP baseline;
11. after the controlled gate passes, validate within the exact authorised ZCHPC operational scope.

## 3. Controlled academic lab

The current dissertation has one academic lab, not three.

**Lab:** Synthetic Government Permit and Service Application API

**Engineering ID:** `government-permit-service-fastapi`

**Default stack:** Python/FastAPI + small relational database, hosted on the Linux VM already provided by ZCHPC.

Roles: two applicants for cross-user tests, officer and administrator.

The lab uses only synthetic data and has vulnerable/corrected states, deterministic reset, OpenAPI, direct contract tests and independent ground truth.

## 4. ZCHPC operational validation

ZCHPC validation is a second-stage real-world validation after controlled lab success. Signed project authorisation exists, but every run must still match an explicit local scope definition reflecting the approved assets/interfaces/accounts/traffic/time window.

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
- no scanner access to lab ground truth during detection.

## 6. Evaluation acceptance

The controlled lab must support deterministic TP/FP/FN and defensible TN/FPR measurement, precision, recall, F1, scan duration, request counts, error/inconclusive states and repeated-run/report reproducibility.

ZCHPC validation records applicability, repeatability, evidence quality, confirmed/suspected/inconclusive observations and operational constraints separately.

## 7. Completion criteria

Project completion requires:

- clean installation/reproduction;
- enforced safety preflight;
- working inventory and identity handling;
- implemented bounded test catalogue;
- one reproducible synthetic lab with frozen ground truth;
- automatic HTML/PDF/JSON/CSV reporting;
- controlled lab accuracy evaluation and applicable ZAP comparison;
- authorised ZCHPC validation performed only after the controlled gate and only within signed scope;
- final research dataset/provenance sufficient for examiner reproduction;
- no real credentials or confidential target evidence committed.

## 8. Delimitations

Not required for this dissertation: three implementation stacks, extra government labs, fintech/mobile-money/healthcare labs, SAST, comprehensive GraphQL/SOAP/gRPC, full penetration testing, hypervisor exploitation, production SaaS or LLM services.

Future commercialisation may add those environments after the dissertation.
