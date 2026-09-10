# Implementation Plan and Acceptance Gates

## 1. Delivery principle

AntiGravity implements the dissertation sequentially. A phase is complete only when its implementation, automated tests, safety controls, adversarial gates and reproducible evidence all pass on the exact phase head.

Canonical sequence:

```text
P1  Repository and runtime foundation
P2  Synthetic permit/service laboratory and independent ground truth
P3  Specification ingestion and endpoint inventory
P4  Safety, persistence, identity and controlled HTTP execution
P5  Authorisation engine
P6  Authentication/configuration/inventory/resource rules
P7  Evidence, findings and automatic reporting
P8  Dashboard and CLI completion
P9  Controlled laboratory evaluation and OWASP ZAP baseline
P10 Authorised ZCHPC cloud validation and final research release
```

The topic remains Zimbabwean e-government API security. The controlled lab establishes measurable scanner accuracy. ZCHPC is the later authorised real-world validation environment.

## 2. P1 — Repository and runtime foundation

Create a clean, installable Python application and deterministic developer/CI command surface. Do not implement the lab or active scanner rules yet.

Required outputs include:

- `pyproject.toml` and reproducible dependency lock;
- `src/delicious_scanner/` package;
- FastAPI `/health`;
- Typer CLI health/version surface;
- SQLAlchemy 2.x + migrations + SQLite;
- secret-safe structured logging;
- pytest, Ruff and type checking;
- root Compose skeleton where Docker is available;
- `.env.example`, `.gitignore`, Makefile and CI;
- full-SHA third-party Actions, least-privilege permissions and PR-safe verification;
- repository secret scanning;
- terminal-control sanitisation baseline;
- documented future `httpx` target client contract with ambient proxy environment ignored by default.

Stable command surface:

```text
make bootstrap
make format
make lint
make typecheck
make test
make verify
make app
make labs-up
make labs-down
```

**Exit gate:** clean checkout bootstraps, app/CLI run, migrations work, `make verify` passes and applicable P1 CRITICAL/HIGH attack cases pass.

## 3. P2 — Synthetic permit/service laboratory and independent ground truth

Build one research target before scanner detector tuning:

`labs/government-permit-service-fastapi/`

Required:

- FastAPI + small relational database;
- synthetic users/data only;
- `applicant-a`, `applicant-b`, `officer`, `admin` fixtures;
- vulnerable and corrected modes;
- deterministic seed/reset;
- health/lab-version/mode/fixture metadata;
- OpenAPI artefact;
- direct functional tests independent of scanner code;
- `ground-truth/manifest.yaml`;
- locked dependencies;
- loopback/controlled local exposure on the provided Linux VM;
- no production service dependency.

**Exit gate:** every headline seeded case is independently proven vulnerable in vulnerable mode and corrected in corrected mode; unrelated workflow semantics remain aligned; reset and ground truth are deterministic; applicable `RT-LAB-*` gates pass.

## 4. P3 — Specification ingestion and endpoint inventory

Implement safe OpenAPI 3.x and Postman import, specification provenance/hashing, normalised operation inventory, declared-auth metadata, bounded variable/reference handling and documented/live inventory foundations.

Imported scripts remain inert; external reference fetching is disabled by default; imported server URLs cannot expand authorised target scope.

**Exit gate:** the controlled lab specification imports deterministically, malformed/unsupported cases fail or warn explicitly, and applicable `RT-SPEC-*`/network import gates pass.

## 5. P4 — Safety, persistence, identity and controlled HTTP execution

Implement Project/Target/Specification/Identity models, scan lifecycle, immutable scope/profile snapshots, exact allow-list and destination validation, redirect revalidation, runtime secret references, redaction foundation, central `httpx` executor, budgets, isolated identity sessions, preflight, deterministic planning and cancellation.

**Exit gate:** no rule can bypass central execution/scope controls, and all applicable P4 CRITICAL/HIGH scope, budget, secret, identity, state and DB gates pass.

## 6. P5 — Authorisation engine

Implement the versioned rule framework and controlled differential authorisation rules:

- `AUTHZ-BOLA-001/002`;
- `AUTHZ-BFLA-001/002`;
- `AUTHZ-BOPLA-001/002`.

Every rule needs applicability, proof, corrected-negative, budget, redaction and seeded-lab integration tests. Mutation proof requires independent read-back and reset.

**Exit gate:** applicable seeded cases in `government-permit-service-fastapi` are detected without false confirmation of corrected cases; semantic adversarial gates pass.

## 7. P6 — Authentication, configuration, inventory and bounded resource rules

Implement the locked non-authorisation catalogue where deterministic and safe:

- `AUTHN-MISSING-001`, `AUTHN-INVALID-001`, `AUTHN-EXPIRED-001`, `AUTHN-SESSION-001`, `AUTHN-INCONSISTENT-001`;
- `CONFIG-CORS-001`, `CONFIG-HEADERS-001`, `CONFIG-TLS-001`, `CONFIG-ERROR-001`, `CONFIG-METHOD-001`, `CONFIG-DOCS-001`;
- `INVENTORY-DIFF-001/002`, `INVENTORY-AUTH-001`;
- `RESOURCE-RATE-001` and optional `RESOURCE-SIZE-001` under strict sub-budgets.

Unsupported/unprovable cases remain `NOT_APPLICABLE` or `INCONCLUSIVE`.

## 8. P7 — Evidence, findings and automatic reporting

Reporting is a core product feature, not optional polish.

Required:

- redaction before persistence;
- evidence minimisation and hard size bounds;
- finding fingerprints, severity/confidence and OWASP/CWE mappings;
- canonical JSON report + schema;
- CSV research exports with formula neutralisation;
- escaped human-readable HTML report;
- required PDF report generated from the canonical report model/HTML;
- limitations/inconclusive/error section;
- provenance, request counts/timings and safe reproduction guidance;
- controlled export paths and operational-confidentiality handling.

**Exit gate:** known fixture secrets are absent from DB/log/HTML/PDF/JSON/CSV; report/schema/injection adversarial cases pass.

## 9. P8 — Dashboard and CLI completion

Complete equivalent browser and CLI workflows for project/target/spec/identity configuration, preflight, planning, scan execution, findings review and HTML/PDF/JSON/CSV report export.

Local web safety requires loopback default bind, Host validation, no permissive CORS, CSRF protection, escaped target content and safe export paths.

## 10. P9 — Controlled laboratory evaluation and OWASP ZAP baseline

Build the deterministic evaluation harness for the single controlled lab.

Required:

- reset/version/mode/fixture verification;
- evaluation-only ground-truth ingestion;
- detector/ground-truth architectural separation;
- deterministic case matching;
- TP/FP/FN and defensible TN/FPR;
- precision, recall, F1, duration/request counts;
- repeated-run and report reproducibility;
- pinned/documented OWASP ZAP baseline;
- ZAP applicability states;
- JSON/CSV research datasets with run-validity reasons;
- frozen ground truth, matcher, metric/state treatment, scanner profile and ZAP configuration before final controlled collection.

**Exit gate:** one documented sequence runs the controlled experiment reproducibly and all applicable `RT-EVAL-*`/`RT-LAB-005` gates pass.

## 11. P10 — Authorised ZCHPC cloud validation and final research release

P10 starts only after P9 passes.

Before any operational request:

1. load a local, non-committed `authorised-zchpc` target profile;
2. verify the profile matches the signed authorisation reference and exact approved assets/interfaces/accounts/traffic/time window;
3. use stricter, non-destructive defaults;
4. prove no lab mutation permission or seeded-ground-truth assumption carries into operational scanning.

Potential observations are limited to the approved externally observable surface, such as API/service exposure, approved authentication/access-control behaviour, TLS/HTTP security configuration, documentation exposure, service inventory differences and safe deployment misconfigurations.

Never deliberately introduce weaknesses into operational ZCHPC infrastructure. No VM escape, hypervisor exploitation, DoS/stress, persistence, lateral movement, unrelated tenants/assets or destructive fuzzing.

Operational results are analysed separately from controlled accuracy. Do not calculate recall/FN/FPR against ZCHPC unless a defensible complete independent denominator actually exists. Do not describe a limited validation as certification of the entire cloud.

Final release includes clean-environment reproduction, complete scanner/report regression, controlled evaluation evidence, a sanitised ZCHPC validation summary where publishable, final limitations and an immutable release identifier. Confidential operational data remains outside Git/public artefacts.

## 12. Scope lock

Do not reintroduce the former three-lab requirement. Additional e-government, fintech, mobile-money, healthcare or commercial labs are future work only.

A change to the research questions, one-lab model, ZCHPC validation boundary, metric semantics or CRITICAL/HIGH expected-safe behaviour requires an explicit reviewed scope/methodology change before code follows it.
