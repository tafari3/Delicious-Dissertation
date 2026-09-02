# Project Charter and Locked Scope

## 1. Project identity

**Working repository:** `tafari3/Delicious-Dissertation`

**Academic project:** *Autonomous Cross-Platform Application Programming Interface (API) Security Testing and Misconfiguration Scanner for Zimbabwean Fintech and E-Government Systems*

This repository implements the artefact described in the approved project proposal. The scanner is a **source-language-independent, black-box REST API security testing tool**. It operates at the HTTP/API boundary and does not require access to application source code.

## 2. Primary research objective

Determine whether a bounded, cross-platform scanner can reliably identify and report selected API-specific authorisation and security misconfiguration weaknesses across different REST API implementations while:

- keeping false positives low;
- remaining safe and non-destructive by default;
- generating reproducible evidence;
- working across implementation stacks;
- and producing results that can be compared against a documented ground truth and OWASP ZAP.

## 3. Research questions preserved from the proposal

The implementation and evaluation MUST remain capable of answering:

1. **RQ1** — Which API-specific authorisation and misconfiguration controls can be tested reliably using a black-box, specification-assisted approach without source-code access?
2. **RQ2** — How accurately does the scanner identify seeded vulnerabilities across different REST API implementation stacks compared with a general-purpose security-testing baseline?
3. **RQ3** — What trade-offs in false-positive rate, scan time and evidence quality arise when authorisation and misconfiguration checks are combined into one bounded workflow?
4. **RQ4** — How effectively can the scanner translate technical findings into reproducible, OWASP-aligned reports suitable for remediation and audit?

Engineering decisions MUST NOT make these questions impossible to measure.

## 4. Product definition

The finished artefact is a local-first security assessment application that can:

1. create a scan project;
2. register an explicitly authorised REST API target;
3. import an OpenAPI document or Postman collection where available;
4. build an endpoint and operation inventory;
5. configure controlled test identities and roles;
6. validate scope and safety constraints before execution;
7. run an autonomous bounded test catalogue;
8. compare responses across identities, roles, objects and operations;
9. inspect authentication/session and API security configuration;
10. record redacted, reproducible evidence;
11. classify findings by confidence and severity;
12. map findings to OWASP API Security Top 10 2023 and CWE where appropriate;
13. export human-readable and machine-readable reports;
14. run repeatable evaluation against vulnerable laboratory APIs and OWASP ZAP.

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
- session/token reuse and basic lifecycle faults that are observable black-box;
- inconsistent authentication requirements across equivalent operations.

It MUST NOT perform credential stuffing, password spraying or account takeover attempts.

### 5.3 Configuration/misconfiguration testing

The scanner MUST support checks for:

- CORS policy weaknesses;
- TLS configuration observations that are safely testable from the client boundary;
- relevant security header omissions or unsafe values;
- verbose error or stack-trace leakage;
- risky HTTP methods;
- exposed interactive/API documentation;
- endpoint/specification inventory mismatches.

### 5.4 Resource-control testing

The scanner MUST support **bounded** rate-limit/resource-control observations using conservative ceilings and explicit stop conditions. It MUST NOT perform denial-of-service, stress, saturation or destructive load testing.

## 6. Cross-platform requirement

The scanner must demonstrate comparable operation against at least three REST API implementation stacks. The initial engineering choice is:

- Python laboratory API;
- Node.js laboratory API;
- Java laboratory API.

The scanner must not contain language-specific assumptions that make findings depend on the target implementation language.

## 7. Laboratory scenarios

Evaluation will use synthetic Zimbabwean workflow analogues only:

- **Mobile Money API** — wallets, balances, transfers, beneficiaries and transaction history;
- **Revenue/Tax API** — taxpayer profiles, obligations, returns/payments and officer/admin operations;
- **Citizen Services API** — citizen profiles, applications/records and privileged case-management operations.

No real financial, taxpayer, citizen or production data is permitted.

Each laboratory must have:

- a known-vulnerable variant/state;
- a corrected variant/state;
- seeded synthetic data;
- controlled identities/roles;
- a machine-readable ground-truth manifest;
- deterministic reset/seed procedures.

## 8. Safety and ethics invariants

These are hard requirements, not optional features.

### 8.1 Target authorisation

A scan MUST NOT start unless the target is explicitly present in the locally configured allow-list/scope policy.

### 8.2 Non-destructive default

The default scan profile MUST avoid destructive mutations. Tests that require a write operation may run only against controlled disposable objects and must have a documented cleanup strategy.

### 8.3 Rate ceilings

Every scan MUST have request-rate and total-request ceilings. Resource-control checks MUST use a stricter independent ceiling.

### 8.4 Proof-of-condition

Once sufficient evidence exists to demonstrate a vulnerability, the scanner MUST stop escalating that test. It must not continue into extraction, persistence, service disruption or privilege abuse.

### 8.5 Secrets and evidence

Passwords, bearer tokens, API keys, cookies, session identifiers and other credentials MUST be redacted before evidence is persisted or exported.

### 8.6 Prohibited capabilities

The project MUST NOT implement:

- credential stuffing;
- password spraying;
- unrestricted fuzzing;
- destructive fuzzing;
- high-impact denial-of-service testing;
- exploitation beyond proof-of-condition;
- arbitrary attack scripting against unapproved targets;
- production scanning without explicit written authorisation and project/university approval where applicable.

## 9. Delimitations preserved from the proposal

The prototype targets RESTful HTTP APIs.

The following are outside the dissertation artefact scope unless the proposal is formally changed:

- comprehensive GraphQL testing;
- SOAP testing;
- message-queue security testing;
- source-code/static analysis;
- full penetration testing;
- production-grade multi-tenant SaaS deployment;
- active exploitation frameworks.

## 10. Required evidence model

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
- **Suspected** — evidence is significant but insufficient for a definitive proof;
- **Informational** — observation requiring review but not asserted as a vulnerability.

## 11. Evaluation acceptance criteria

The final evaluation dataset MUST permit calculation of:

- true positives (TP);
- false positives (FP);
- false negatives (FN);
- precision;
- recall;
- F1 score;
- false-positive rate as defined in the evaluation protocol;
- scan duration;
- test/finding counts;
- reproducibility/stability across repeated runs;
- cross-stack success rate;
- comparison with OWASP ZAP where the same weakness is within ZAP's practical observable scope.

The ground truth must be authored **before** the final scanner evaluation to avoid retrofitting expected results to scanner output.

## 12. Definition of project completion

The engineering project is complete only when all of the following hold:

1. the scanner can be installed and run from a clean documented environment;
2. target allow-listing and safety preflight are enforced;
3. OpenAPI/Postman-assisted inventory works;
4. controlled multi-identity authorisation testing works;
5. the locked test catalogue has implemented rules with automated tests;
6. evidence is redacted before persistence/export;
7. the dashboard can configure a scan and review findings;
8. all three laboratory stacks are reproducible and contain documented ground truth;
9. vulnerable and corrected variants can be evaluated deterministically;
10. the evaluation harness calculates the required metrics;
11. OWASP ZAP baseline runs are reproducible where applicable;
12. repeated runs produce an auditable research dataset;
13. all required verification commands pass;
14. documentation is sufficient for a supervisor/examiner to reproduce the demonstration.

## 13. Design principle

This is a **research artefact, not a commercial vulnerability-management platform**. Prefer the smallest architecture that answers the research questions rigorously. Do not add distributed services, multi-tenant infrastructure, complex message brokers, cloud dependencies, AI/LLM requirements or enterprise features unless a later requirement demonstrates that they are necessary to answer the approved research problem.
