# Project Charter and Locked Scope

## 1. Project identity

**Working repository:** `tafari3/Delicious-Dissertation`

**Academic project:** *Automated API Security and Misconfiguration Scanner for Zimbabwean E-Government Systems: A Laboratory-Based Evaluation*

This repository implements the artefact described in the current academic proposal baseline. The scanner is a source-language-independent REST API security testing tool operating through authorised API interfaces, available API descriptions and controlled test identities. It does not require target source code.

## 2. Primary research objective

Determine whether a bounded automated scanner can reliably identify and report selected API-specific authorisation, authentication/session, configuration and inventory weaknesses across different REST API implementations while:

- keeping false positives low;
- remaining safe and non-destructive by default;
- generating reproducible evidence;
- working across implementation stacks;
- and producing results that can be compared against documented ground truth and OWASP ZAP.

## 3. Research questions

The implementation and evaluation MUST remain capable of answering:

1. **RQ1** — Which API-specific authorisation, authentication, configuration and inventory controls can be tested reliably using automated, specification-assisted testing with controlled user identities?
2. **RQ2** — How accurately does the proposed scanner identify seeded weaknesses across different REST API implementation stacks when compared with documented ground truth and OWASP ZAP?
3. **RQ3** — What trade-offs in false-positive rate, scan time and evidence quality arise when the selected checks are combined into one bounded security-testing workflow?
4. **RQ4** — How effectively can the scanner support e-government security assurance by translating technical test behaviour into reproducible, OWASP-aligned remediation evidence?

Engineering decisions MUST NOT make these questions impossible to measure.

## 4. Product definition

The finished artefact is a local-first security assessment application that can:

1. create a scan project;
2. register an explicitly authorised REST API target;
3. import an OpenAPI document or Postman collection where available;
4. build an endpoint and operation inventory;
5. configure controlled test identities and roles;
6. validate scope and safety constraints before execution;
7. run an automated bounded test catalogue;
8. compare responses across identities, roles, objects and operations;
9. inspect authentication/session and API security configuration;
10. record redacted, reproducible evidence;
11. classify findings by confidence and severity;
12. map findings to OWASP API Security Top 10 2023 and CWE where appropriate;
13. export human-readable and machine-readable reports;
14. run repeatable evaluation against vulnerable and corrected e-government laboratory APIs and OWASP ZAP.

## 5. Locked functional scope

### 5.1 Authorisation testing

The scanner MUST support checks for:

- Broken Object Level Authorisation (BOLA);
- Broken Function Level Authorisation (BFLA);
- Broken Object Property Level Authorisation / mass assignment (BOPLA);
- role and ownership differential behaviour using controlled identities.

### 5.2 Authentication/session testing

The scanner MUST support bounded checks for:

- missing authentication on protected operations;
- invalid, expired or malformed token handling where a controlled test can be performed;
- session/token reuse and basic lifecycle faults that are observable through API behaviour;
- inconsistent authentication requirements across equivalent operations.

It MUST NOT perform credential stuffing, password spraying or account takeover attempts.

### 5.3 Configuration/misconfiguration testing

The scanner MUST support checks for:

- CORS policy weaknesses;
- TLS configuration observations safely testable from the client/API boundary;
- relevant security header omissions or unsafe values;
- verbose error or stack-trace leakage;
- risky HTTP methods;
- exposed interactive/API documentation;
- endpoint/specification inventory mismatches.

### 5.4 Resource-control testing

The scanner MUST support **bounded** rate-limit/resource-control observations using conservative ceilings and explicit stop conditions. It MUST NOT perform denial-of-service, stress, saturation or destructive load testing.

## 6. Cross-platform requirement

The scanner must demonstrate comparable operation against at least three REST API implementation stacks. The current engineering choice is:

- Python / FastAPI;
- Node.js / Express;
- Java / Spring Boot.

The scanner must not contain target-language-specific assumptions that make findings depend on the target implementation language.

## 7. Laboratory scenarios

Evaluation will use synthetic Zimbabwean e-government workflow analogues only:

- **Citizen Records API** — citizen profiles, records, applications and officer/admin case-management operations;
- **Public Health Records API** — patient records, appointments, laboratory results and clinician/records/admin operations;
- **Permit & Licensing API** — applications, supporting documents, permits/licences, processing and supervisor/admin operations.

These laboratories are representative research workflows, not replicas of any named Zimbabwean government system.

No real citizen, health, identity, permit, financial or production data is permitted.

Each laboratory must have:

- a known-vulnerable mode/state;
- a corrected mode/state;
- seeded synthetic data;
- controlled identities/roles;
- a machine-readable ground-truth manifest;
- deterministic reset/seed procedures;
- direct functional tests that prove both vulnerable and corrected behaviour independently of the scanner.

The exact lab role and endpoint contracts are defined in `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`.

## 8. ZCHPC and cloud scope

ZCHPC is a relevant Zimbabwean cloud/national-computing context, not a default scan target.

If formal permission and resources are granted, an isolated copy of the student's own laboratory environment may be deployed to an authorised ZCHPC test resource to examine portability in a local cloud environment.

The scanner must not probe ZCHPC production services, management plane, hypervisor, unrelated tenants, network fabric or production government applications as part of the dissertation evaluation.

Failure to obtain ZCHPC access does not block project completion; the full evaluation must remain reproducible on student-controlled local/VM/container infrastructure.

## 9. Safety and ethics invariants

These are hard requirements, not optional features.

### 9.1 Target authorisation

A scan MUST NOT start unless the target is explicitly present in the locally configured allow-list/scope policy.

### 9.2 Non-destructive default

The default scan profile MUST avoid destructive mutations. Tests that require a write operation may run only against controlled disposable objects and must have a documented cleanup/reset strategy.

### 9.3 Rate ceilings

Every scan MUST have request-rate and total-request ceilings. Resource-control checks MUST use a stricter independent ceiling.

### 9.4 Proof-of-condition

Once sufficient evidence exists to demonstrate a vulnerability, the scanner MUST stop escalating that test. It must not continue into unnecessary extraction, persistence, service disruption or privilege abuse.

### 9.5 Secrets and evidence

Passwords, bearer tokens, API keys, cookies, session identifiers and other credentials MUST be redacted before evidence is persisted or exported.

### 9.6 Prohibited capabilities

The project MUST NOT implement:

- credential stuffing;
- password spraying;
- unrestricted fuzzing;
- destructive fuzzing;
- high-impact denial-of-service testing;
- exploitation beyond proof-of-condition;
- arbitrary attack scripting against unapproved targets;
- production scanning without explicit written authorisation and project/university approval where applicable.

## 10. Delimitations

The prototype targets RESTful HTTP APIs.

The following are outside the dissertation artefact scope unless the academic proposal is formally changed:

- comprehensive GraphQL testing;
- SOAP testing;
- message-queue security testing;
- source-code/static analysis;
- full penetration testing;
- production-grade multi-tenant SaaS deployment;
- active exploitation frameworks;
- ZCHPC/cloud-management-plane security assessment;
- fintech and digital-payment evaluation.

Fintech is reserved for future work after the e-government implementation and evaluation are complete.

## 11. Required evidence model

Every scanner finding must be attributable to:

- scan identifier;
- target and endpoint/operation;
- test rule identifier and version;
- test identity/role context, in redacted form;
- timestamp;
- safe request summary;
- response observation/differential;
- redacted request/response evidence where needed;
- severity;
- confidence;
- OWASP API Security Top 10 mapping;
- CWE mapping where appropriate;
- remediation note;
- reproducibility instructions.

Findings must distinguish at minimum:

- **Confirmed** — scanner observed the defined proof condition;
- **Suspected** — evidence is significant but insufficient for definitive proof;
- **Informational** — noteworthy observation without vulnerability assertion.

Rule execution must also preserve `NOT_APPLICABLE`, `PASS_OBSERVED`, `INCONCLUSIVE` and `ERROR` states as defined in the test catalogue.

## 12. Evaluation acceptance criteria

The final evaluation dataset MUST permit calculation/reporting of:

- true positives (TP);
- false positives (FP);
- false negatives (FN);
- true negatives (TN) where the unit of analysis makes them defensible;
- precision;
- recall;
- F1 score;
- false-positive rate where a defensible TN denominator is predeclared;
- scan duration;
- request/test/finding counts;
- reproducibility/stability across repeated runs;
- cross-stack success/coverage;
- comparison with OWASP ZAP where the same weakness is within ZAP's practical observable scope.

The primary evaluation unit, matching key and ground truth must be fixed before final data collection. Ground truth must be authored before the scanner is tuned against final evaluation results.

## 13. Definition of project completion

The engineering project is complete only when all of the following hold:

1. the scanner can be installed and run from a clean documented environment;
2. target allow-listing and safety preflight are enforced;
3. OpenAPI/Postman-assisted inventory works;
4. controlled multi-identity authorisation testing works;
5. the locked test catalogue has implemented rules with automated tests;
6. evidence is redacted before persistence/export;
7. the dashboard can configure a scan and review findings;
8. all three e-government laboratory stacks are reproducible and contain documented independent ground truth;
9. vulnerable and corrected variants can be evaluated deterministically;
10. the evaluation harness calculates the required metrics;
11. OWASP ZAP baseline runs are reproducible where applicable;
12. repeated runs produce an auditable research dataset;
13. all required verification commands pass;
14. documentation is sufficient for a supervisor/examiner to reproduce the demonstration;
15. no claim is made about the security posture of a named Zimbabwean government or ZCHPC production system from the laboratory results.

## 14. Design principle

This is a **research artefact, not a commercial vulnerability-management platform**. Prefer the smallest architecture that answers the research questions rigorously. Do not add distributed services, multi-tenant infrastructure, complex message brokers, cloud dependencies, AI/LLM requirements or enterprise features unless a later requirement demonstrates that they are necessary to answer the approved research problem.
