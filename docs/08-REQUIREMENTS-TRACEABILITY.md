# Proposal-to-Implementation Traceability

## 1. Purpose

This document ensures the engineering build remains traceable to the academic proposal. It is not a replacement for the proposal; it maps proposal commitments to repository components and acceptance evidence.

## 2. Objective traceability

| Proposal objective / commitment | Engineering location | Required proof |
|---|---|---|
| Define a bounded OWASP-aligned API test catalogue | `docs/02-TEST-CATALOGUE.md`, `src/delicious_scanner/rules/` | Versioned rule catalogue and automated tests |
| Source-language-independent architecture | `docs/01-ARCHITECTURE.md` | Same scanner runs against Python, Node.js and Java labs without target-language scanner changes |
| Accept authorised target, API description and controlled identities | Project/Target/Specification/Identity domains | Dashboard/CLI configuration + preflight tests |
| Enforce allow-listing, rate limiting and non-destructive defaults | `docs/06-SAFETY-SECURITY-MODEL.md`, preflight and controlled HTTP executor | Unit/integration tests demonstrating hard blocking/ceilings |
| Detect BOLA | `AUTHZ-BOLA-*` | Vulnerable/corrected lab integration results |
| Detect BFLA | `AUTHZ-BFLA-*` | Vulnerable/corrected lab integration results |
| Detect BOPLA/mass assignment | `AUTHZ-BOPLA-*` | Vulnerable/corrected lab integration results |
| Test token/session faults | `AUTHN-*` | Controlled lab/session fixtures and rule evidence |
| Check CORS/TLS/headers/errors/risky methods/docs | `CONFIG-*` | Rule-level tests and seeded/controlled observations |
| Compare endpoint inventory with specification | `INVENTORY-*` | Known documented/undocumented lab cases |
| Bounded rate-limit/resource behaviour | `RESOURCE-*` | Ceiling tests prove scanner cannot exceed configured safe budget |
| Build at least three implementation-stack labs | `labs/` | FastAPI/Express/Spring Boot services with deterministic reset |
| Document ground truth | `labs/*/ground-truth/manifest.yaml` | Versioned manifest + direct lab functional tests independent of scanner |
| Store evidence with endpoint/rule/redacted traffic/severity/mapping/time/remediation | data/evidence/finding models | Schema tests and exported canonical reports |
| Strip credentials/tokens before storing/exporting evidence | redaction pipeline | Synthetic secret leakage tests across DB/log/export paths |
| Compare against OWASP ZAP | `evaluation/` | Pinned/documented ZAP baseline and normalized results |
| Measure coverage/precision/recall/false positives/scan time/reproducibility | `evaluation/` | Generated metrics dataset and analysis |
| Minimal web interface | FastAPI + lightweight server-rendered dashboard | Project/scan/findings/report journeys work locally |
| Explicit scope before scan | preflight state machine | Scan cannot transition to READY/EXECUTING without valid scope |
| Exclude DoS, credential stuffing, unrestricted fuzzing and exploitation beyond proof | charter, safety model, agent contract | No such capability in code; hard stop tests for relevant limits |

## 3. Research-question traceability

### RQ1 — Reliably testable black-box controls

Evidence sources:

- rule applicability/result counts;
- confirmed/suspected/inconclusive distribution;
- category-by-category evaluation across labs;
- documented limitations for conditions that cannot be reliably proven black-box.

Engineering requirement:

The scanner must preserve `INCONCLUSIVE` and `NOT_APPLICABLE` as first-class outcomes so RQ1 is not distorted into a binary vulnerable/not-vulnerable claim.

### RQ2 — Detection accuracy across stacks versus baseline

Evidence sources:

- three-stack ground truth;
- scanner TP/FP/FN metrics;
- ZAP applicable baseline results;
- per-stack detection summary.

Engineering requirement:

Ground truth and lab direct functional tests must exist independently of scanner findings.

### RQ3 — False-positive/time/evidence trade-offs

Evidence sources:

- request count and wall-clock duration;
- confirmed versus suspected classifications;
- corrected-mode negative cases;
- repeated runs;
- evidence size/quality metadata.

Engineering requirement:

Rule output must retain confidence, evidence references and timing/request statistics.

### RQ4 — Reproducible OWASP-aligned reporting

Evidence sources:

- canonical JSON reports;
- HTML reports;
- OWASP/CWE mapping;
- safe reproduction instructions;
- provenance metadata;
- reviewer/examiner demonstration.

Engineering requirement:

Every confirmed finding must identify the exact rule/version, endpoint, expected/observed behaviour and redacted proof.

## 4. Safety/ethics traceability

| Safety commitment | Implementation mechanism | Test/evidence |
|---|---|---|
| Written authorisation required for non-lab targets | target metadata + operating policy | preflight/config validation and documentation |
| Local target allow-list | centralized scope validator | allowed/disallowed target tests |
| Request-rate ceilings | HTTP executor limiter | limit enforcement tests |
| Total request ceiling | scan/request budget | exhaustion test |
| Non-destructive default | Safe Read-Only profile | profile tests |
| Writes only on controlled disposable objects | Controlled Lab Full profile + fixture metadata | mutation rule precondition/cleanup tests |
| Stop at proof condition | rule stop semantics | request-count assertions |
| Token/password/session redaction | redaction pipeline | synthetic secret leakage tests |
| Synthetic lab data only | lab fixtures | fixture review/tests |
| No production system dependency | local Docker Compose labs | clean-machine reproduction |

## 5. Delimitation traceability

The engineering build must not silently expand beyond:

- RESTful HTTP APIs;
- black-box/specification-assisted testing;
- selected OWASP API Security Top 10 2023 categories that can be tested safely;
- synthetic/authorised targets.

The following are not required completion criteria:

- GraphQL scanner;
- SOAP scanner;
- message-queue scanner;
- SAST/source-code analysis;
- full penetration-testing framework;
- production SaaS hosting;
- generic exploit chaining.

## 6. Final artefact traceability checklist

Before final dissertation evaluation/release, verify:

- [ ] Every implemented scanner rule maps to a catalogue ID.
- [ ] Every seeded lab vulnerability maps to a ground-truth ID and expected rule.
- [ ] Every expected rule has at least one positive and corrected/negative evaluation case where applicable.
- [ ] Every confirmed exported finding includes reproducible redacted evidence.
- [ ] Every scan captures scanner/rule/spec/profile provenance.
- [ ] Every final research run records the exact lab/ground-truth version.
- [ ] Metric formulas and units of analysis are fixed before final data collection.
- [ ] ZAP version/configuration is pinned and documented.
- [ ] Unimplemented OWASP categories are reported as not covered, not secure.
- [ ] Safety boundaries remain enforced in code and tests.
- [ ] No real credentials or production data are present in repository/evaluation artefacts.
