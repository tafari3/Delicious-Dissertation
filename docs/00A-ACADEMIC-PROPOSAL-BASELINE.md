# Academic Proposal Baseline

## 1. Status

This file is the repository-local baseline for the submission-ready academic proposal approved for implementation planning in September 2026.

**Project title:** *Automated API Security and Misconfiguration Scanner for Zimbabwean E-Government Systems: A Laboratory-Based Evaluation*

The purpose of this file is to keep implementation, tests, issues and dissertation evidence aligned with the current academic scope without relying on prior chat history. If the supervisor formally approves a scope change, update this file and every affected authoritative document in one reviewed change before implementation continues.

## 2. Current research scope

The dissertation focuses on Zimbabwean **e-government REST APIs** and controlled cloud/VM deployments.

The project will design, implement and evaluate an automated API security testing and misconfiguration scanner that identifies selected:

- authorisation weaknesses;
- authentication and session weaknesses;
- configuration/misconfiguration weaknesses;
- endpoint/specification inventory weaknesses;
- bounded resource-control observations.

The scanner must produce reproducible, redacted evidence aligned with the OWASP API Security Top 10 (2023) and CWE where appropriate.

## 3. Aim

To design, implement and evaluate an automated API security testing and misconfiguration scanner that identifies selected authorisation, authentication, configuration and inventory weaknesses in representative Zimbabwean e-government REST APIs and produces reproducible, OWASP-aligned evidence.

## 4. Objectives

1. Review literature published from 2022 onward on Zimbabwean e-government, public-sector cybersecurity, cloud infrastructure and REST API security, together with OWASP API Security Top 10 (2023), to define a safe bounded test catalogue.
2. Design a scanner architecture that accepts an authorised target, an OpenAPI/Postman description where available and controlled test identities while enforcing allow-listing, request-rate ceilings, secret redaction and non-destructive profiles.
3. Implement automated checks for BOLA, BFLA, BOPLA/mass assignment, token/session weaknesses, CORS/TLS/security headers, risky HTTP methods, information leakage, exposed documentation, endpoint-inventory drift and bounded rate-limit behaviour.
4. Build three deliberately vulnerable e-government laboratory APIs representing citizen-record, public-health-record and permit/licensing workflows. Each laboratory uses synthetic records, defined roles, documented independent ground truth and vulnerable/corrected behaviour across different implementation stacks.
5. Evaluate the scanner against documented ground truth and OWASP ZAP using vulnerability coverage, precision, recall, F1 score, false-positive behaviour, scan time and repeatability of evidence.

## 5. Research questions

- **RQ1:** Which API-specific authorisation, authentication, configuration and inventory controls can be tested reliably using automated, specification-assisted testing with controlled user identities?
- **RQ2:** How accurately does the proposed scanner identify seeded weaknesses across different REST API implementation stacks when compared with documented ground truth and OWASP ZAP?
- **RQ3:** What trade-offs in false-positive rate, scan time and evidence quality arise when the selected checks are combined into one bounded security-testing workflow?
- **RQ4:** How effectively can the scanner support e-government security assurance by translating technical test behaviour into reproducible, OWASP-aligned remediation evidence?

## 6. Laboratory evaluation model

The dissertation uses three representative synthetic e-government workflows:

1. **Citizen Records API** — Python / FastAPI;
2. **Public Health Records API** — Node.js / Express;
3. **Permit & Licensing API** — Java / Spring Boot.

The stack-to-scenario mapping may be changed only through a reviewed scope/design change while preserving three materially different implementation stacks.

Each lab must have:

- synthetic data only;
- controlled test identities and roles;
- deterministic seed/reset;
- vulnerable and corrected modes;
- machine-readable independent ground truth;
- direct functional tests proving the intended vulnerable and corrected behaviour;
- an API description suitable for scanner inventory testing;
- loopback-only canonical exposure;
- no dependency on a real government or production system.

The laboratories are representative workflows, not replicas of named ministries, agencies or national systems.

## 7. ZCHPC boundary

ZCHPC is a relevant Zimbabwean cloud/national-computing context. If formal permission and resources are granted, an isolated copy of the student's **own laboratory environment** may be hosted on an authorised ZCHPC test resource.

ZCHPC production services, management plane, hypervisor, network fabric, unrelated tenants and production government applications are **not** dissertation evaluation targets.

The dissertation must remain fully completable without ZCHPC access by using student-controlled VM/container infrastructure.

## 8. Evaluation commitments

The final evaluation must:

- establish ground truth before final scanner evaluation;
- run the scanner against both vulnerable and corrected modes;
- preserve all valid and invalid/failed runs with explicit validity reasons;
- calculate TP, FP, FN and, where a defensible negative-case denominator is predeclared, TN;
- calculate precision, recall and F1 score;
- report false-positive rate only where TN is defensibly defined;
- record scan duration and request counts;
- repeat key runs to measure stability/reproducibility;
- compare across the three implementation stacks;
- use OWASP ZAP as a general-purpose baseline only where equivalent observation is practical;
- distinguish `not equivalently tested` from `tested and missed` for ZAP comparison.

## 9. Safety and ethics commitments

The project must enforce:

- explicit authorised target scope;
- non-destructive defaults;
- strict request/rate/concurrency budgets;
- stricter bounded resource-control budgets;
- proof-of-condition stopping;
- synthetic laboratory data only;
- secret/token/cookie/password redaction before persistence/export;
- no unauthorised production scanning;
- no credential stuffing or password spraying;
- no destructive/unrestricted fuzzing;
- no denial-of-service, stress or saturation testing;
- no exploitation beyond the minimum proof condition.

## 10. Delimitations

Current dissertation scope excludes:

- comprehensive GraphQL testing;
- SOAP testing;
- message-queue security testing;
- native mobile-application testing;
- source-code/static analysis;
- full penetration testing;
- cloud-management-plane or hypervisor assessment;
- production-grade SaaS/multi-tenancy;
- exploit chaining;
- fintech and digital-payment API evaluation.

**Fintech is future work only** after the e-government dissertation implementation and evaluation are complete.

## 11. Terminology lock

Repository documentation, code-facing descriptions, UI text and reports should use terminology consistent with the current proposal, including:

- automated API security testing;
- API-interface behaviour;
- specification-assisted testing;
- controlled test identities;
- laboratory-based evaluation;
- source-language independence / portability across implementation stacks.

Do not reintroduce terminology from superseded proposal drafts merely because it remains in Git history.

## 12. Traceability rule

Every implementation phase must remain traceable to these academic commitments. Engineering may refine internal package names, algorithms and implementation details, but must not silently change:

- the e-government-only evaluation scope;
- the three representative laboratory classes;
- the research questions;
- the safety boundary;
- the ground-truth/evaluation methodology;
- the role of ZCHPC;
- or the future-work status of fintech.
