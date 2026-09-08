# Proposal-to-Implementation Traceability

## 1. Purpose

This document maps the current academic proposal commitments to repository components and acceptance evidence. The authoritative academic summary is `docs/00A-ACADEMIC-PROPOSAL-BASELINE.md`.

## 2. Objective traceability

| Proposal objective / commitment | Engineering location | Required proof |
|---|---|---|
| Define a bounded OWASP-aligned API test catalogue | `docs/02-TEST-CATALOGUE.md`, `src/delicious_scanner/rules/` | Versioned rule catalogue and automated tests |
| Source-language-independent architecture | `docs/01-ARCHITECTURE.md` | Same scanner runs against FastAPI, Express and Spring labs without target-language scanner changes |
| Accept authorised target, API description and controlled identities | Project/Target/Specification/Identity domains | Dashboard/CLI configuration + preflight tests |
| Enforce allow-listing, rate limiting and non-destructive defaults | `docs/06-SAFETY-SECURITY-MODEL.md`, preflight and controlled HTTP executor | Unit/integration tests demonstrating hard blocking/ceilings |
| Detect BOLA | `AUTHZ-BOLA-*` | Vulnerable/corrected lab integration results |
| Detect BFLA | `AUTHZ-BFLA-*` | Vulnerable/corrected lab integration results |
| Detect BOPLA/mass assignment | `AUTHZ-BOPLA-*` | Vulnerable/corrected lab integration results |
| Test token/session faults | `AUTHN-*` | Controlled lab/session fixtures and rule evidence |
| Check CORS/TLS/headers/errors/risky methods/docs | `CONFIG-*` | Rule-level tests and seeded/controlled observations |
| Compare endpoint inventory with specification | `INVENTORY-*` | Known documented/undocumented lab cases |
| Bounded rate-limit/resource behaviour | `RESOURCE-*` | Ceiling tests prove scanner cannot exceed configured safe budget |
| Build three e-government labs on different stacks | `labs/`, `docs/13-LAB-EXPERIMENT-SPECIFICATION.md` | Citizen Records/FastAPI, Public Health/Express, Permit & Licensing/Spring with deterministic reset |
| Document independent ground truth | `labs/*/ground-truth/manifest.yaml` | Versioned manifests + direct lab functional tests independent of scanner |
| Store evidence with endpoint/rule/redacted traffic/severity/mapping/time/remediation | data/evidence/finding models | Schema tests and exported canonical reports |
| Strip credentials/tokens before persistence/export | redaction pipeline | Synthetic secret leakage tests across DB/log/export paths |
| Compare against OWASP ZAP | `evaluation/` | Pinned/documented ZAP baseline and applicability-aware normalized results |
| Measure precision/recall/F1/false positives/scan time/reproducibility | `evaluation/` | Generated metrics dataset and analysis with predeclared units |
| Minimal web interface | FastAPI + lightweight server-rendered dashboard | Project/scan/findings/report journeys work locally |
| Explicit scope before scan | preflight state machine | Scan cannot transition to READY/EXECUTING without valid scope |
| Exclude DoS, credential attacks, destructive fuzzing and exploitation beyond proof | charter, safety model, agent contract | No such capability in code; hard-stop tests for relevant limits |
| Keep ZCHPC optional and non-production | charter, lab/evaluation protocol | Student-controlled lab can run locally; ZCHPC production is never required/targeted |
| Keep fintech outside current evaluation | academic baseline, charter | No fintech lab or headline evaluation dependency |

## 3. Research-question traceability

### RQ1 — Reliably testable API controls

Evidence sources:

- rule applicability/result counts;
- confirmed/suspected/inconclusive distribution;
- category-by-category evaluation across labs;
- documented limitations for conditions that cannot be reliably proven from authorised API-interface behaviour.

Engineering requirement:

Preserve `INCONCLUSIVE` and `NOT_APPLICABLE` as first-class outcomes so RQ1 is not distorted into a binary vulnerable/not-vulnerable claim.

### RQ2 — Detection accuracy across stacks versus ground truth and ZAP

Evidence sources:

- three-stack independent ground truth;
- scanner TP/FP/FN/TN where defensible;
- precision, recall and F1;
- ZAP applicable baseline results;
- per-stack detection summary.

Engineering requirement:

Ground truth and direct lab functional tests exist independently of scanner findings. ZAP comparison includes explicit applicability/coverage state.

### RQ3 — False-positive/time/evidence trade-offs

Evidence sources:

- request count and wall-clock duration;
- confirmed versus suspected classifications;
- paired corrected-mode negative cases;
- repeated runs;
- evidence size/quality metadata.

Engineering requirement:

Rule output retains confidence, evidence references and timing/request statistics. The evaluation unit and metric-state treatment are frozen before final collection.

### RQ4 — Reproducible OWASP-aligned e-government assurance

Evidence sources:

- canonical JSON reports;
- HTML reports;
- OWASP/CWE mapping;
- safe reproduction instructions;
- provenance metadata;
- supervisor/examiner demonstration.

Engineering requirement:

Every confirmed finding identifies the exact rule/version, endpoint, expected/observed behaviour and redacted proof.

## 4. Laboratory traceability

| Academic laboratory commitment | Canonical engineering lab | Required proof |
|---|---|---|
| Citizen-record public-service workflow | `citizen-records-fastapi` | Synthetic fixtures, roles, vulnerable/corrected direct tests and ground truth |
| Public-health-record workflow | `public-health-express` | Synthetic fixtures, roles, vulnerable/corrected direct tests and ground truth |
| Permit/licensing workflow | `permit-licensing-spring` | Synthetic fixtures, roles, vulnerable/corrected direct tests and ground truth |
| Different implementation stacks | FastAPI / Express / Spring Boot | Same scanner runs without target-language-specific detection logic |
| Representative, not replicas | Lab docs and reports | No claim that a lab models a named government system's internal design/security |
| Optional authorised ZCHPC hosting | deployment documentation only if permission exists | Own isolated lab only; project remains complete without ZCHPC access |

The exact role, operation and case contract is `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`.

## 5. Safety/ethics traceability

| Safety commitment | Implementation mechanism | Test/evidence |
|---|---|---|
| Written authorisation required for non-lab targets | target metadata + operating policy | preflight/config validation and documentation |
| Local target allow-list | centralized scope validator | allowed/disallowed target tests |
| Request-rate ceilings | HTTP executor limiter | limit enforcement tests |
| Total request ceiling | scan/request budget | exhaustion test |
| Non-destructive default | Safe Read-Only profile | profile tests |
| Writes only on controlled disposable objects | Controlled Lab Full profile + fixture metadata | mutation precondition/cleanup tests |
| Stop at proof condition | rule stop semantics | request-count assertions |
| Token/password/session redaction | redaction pipeline | synthetic secret leakage tests |
| Synthetic lab data only | lab fixtures | fixture review/tests |
| No production-system dependency | local Docker Compose labs | clean-machine reproduction |
| No ZCHPC production scanning | scope policy + docs | no production target in evaluation profiles |

## 6. Delimitation traceability

The engineering build must not silently expand beyond:

- RESTful HTTP APIs;
- automated specification-assisted API testing with controlled identities;
- selected OWASP API Security Top 10 2023 categories that can be tested safely;
- synthetic/explicitly authorised targets;
- e-government laboratory evaluation.

The following are not required completion criteria:

- GraphQL scanner;
- SOAP scanner;
- message-queue scanner;
- SAST/source-code analysis;
- full penetration-testing framework;
- production SaaS hosting;
- generic exploit chaining;
- ZCHPC/cloud-management-plane assessment;
- fintech/digital-payment laboratory evaluation.

## 7. Final artefact traceability checklist

Before final dissertation evaluation/release, verify:

- [ ] Every implemented scanner rule maps to a catalogue ID/version.
- [ ] Every headline evaluation case maps to a frozen ground-truth case ID and expected rule.
- [ ] Every evaluated rule has at least one predeclared positive and paired corrected/negative case where applicable.
- [ ] Every confirmed exported finding includes reproducible redacted evidence.
- [ ] Every scan captures scanner/rule/spec/profile provenance.
- [ ] Every final research run records exact lab/fixture/ground-truth versions.
- [ ] Evaluation unit, matcher, metric formulas and result-state treatment are fixed before final collection.
- [ ] ZAP version/configuration and applicability rules are pinned/documented.
- [ ] Unimplemented OWASP categories are reported as not covered, not secure.
- [ ] Safety boundaries remain enforced in code and tests.
- [ ] No real credentials or production data are present in repository/evaluation artefacts.
- [ ] No final claim extrapolates laboratory results into the security posture of a named government or ZCHPC production system.
