# Laboratory Experiment Specification

## 1. Purpose

This is the canonical contract for the single synthetic e-government laboratory used to prove scanner accuracy before ZCHPC operational validation.

Ground truth belongs to lab/evaluation code. Ordinary scanner detection code must never read this document or generated ground-truth manifests at runtime to decide whether the target is vulnerable.

## 2. Lab identity

**ID:** `government-permit-service-fastapi`

**Name:** Synthetic Government Permit and Service Application API

**Stack:** Python/FastAPI + small relational database.

**Host context:** Linux VM already provided by ZCHPC; Docker/Compose may be used where permitted.

This is a representative research workflow, not a replica of a named ministry, agency or ZCHPC production application.

## 3. Common contract

The lab must provide:

- `vulnerable` and `corrected` modes;
- the same ordinary workflow in both modes except intentional seeded differences;
- synthetic users/records/documents/transactions only;
- stable logical fixture IDs;
- deterministic seed/reset;
- health/lab-version/mode/fixture metadata;
- OpenAPI 3.x description;
- direct functional tests proving positive and paired corrected cases;
- machine-readable independent ground truth;
- no production/external dependency;
- controlled local exposure.

Recommended metadata endpoint: `GET /_lab/meta`.

## 4. Roles and fixtures

Controlled identities:

- `applicant-a`
- `applicant-b`
- `officer`
- `admin`

Representative fixtures:

- `application-a` owned by `applicant-a`;
- `application-b` owned by `applicant-b`;
- `document-a`, `document-b` metadata;
- protected `status`/`approved_by` workflow fields;
- one disposable approval/update object;
- deterministic valid, invalid and, where feasible, expired/revoked test credentials.

## 5. Minimum operation contract

| Operation key | Suggested operation | Intended access |
|---|---|---|
| AUTH-LOGIN | `POST /api/v1/auth/login` | synthetic identities only |
| APP-CREATE | `POST /api/v1/applications` | authenticated applicant |
| APP-READ | `GET /api/v1/applications/{application_id}` | owner, officer/admin according to policy |
| APP-UPDATE | `PATCH /api/v1/applications/{application_id}` | owner permitted fields; staff workflow fields restricted |
| APP-APPROVE | `POST /api/v1/applications/{application_id}/approve` | officer/admin according to frozen policy |
| DOC-READ | `GET /api/v1/documents/{document_id}` | owner and authorised staff |
| ADMIN-USERS | `GET /api/v1/admin/users` | admin only |
| LAB-DOCS | `/docs` / `/openapi.json` | exposure semantics depend on seeded case |
| LAB-INVENTORY-HIDDEN | bounded known route such as `GET /api/v1/internal/status` | intentionally omitted from vulnerable spec fixture for inventory case |

Exact paths may be refined in P2, but operation keys/semantics and ground-truth mapping remain versioned and reviewed.

## 6. Headline seeded cases

At minimum:

- `GT-GPS-BOLA-READ-001` -> `AUTHZ-BOLA-001`: `applicant-a` can read `application-b` in vulnerable mode; corrected mode denies/masks protected content.
- `GT-GPS-BOLA-WRITE-001` -> `AUTHZ-BOLA-002`: `applicant-a` can make the smallest reversible/disposable change to `application-b`; corrected mode prevents persistence.
- `GT-GPS-BFLA-001` -> `AUTHZ-BFLA-001`: applicant can invoke the officer/admin approval function on a disposable fixture; corrected mode enforces privilege.
- `GT-GPS-BOPLA-WRITE-001` -> `AUTHZ-BOPLA-002`: applicant can persist a protected field such as `status`; corrected mode rejects/ignores it and read-back proves no change.
- `GT-GPS-AUTHN-MISSING-001` -> `AUTHN-MISSING-001`: one protected read accepts anonymous access in vulnerable mode; corrected mode requires authentication.
- `GT-GPS-AUTHN-INVALID-001` -> `AUTHN-INVALID-001`: clearly invalid locally generated token is accepted for a protected operation in vulnerable mode; corrected mode rejects it.
- `GT-GPS-AUTHN-EXPIRED-001` -> `AUTHN-EXPIRED-001`: include only if a deterministic expired/revoked fixture can be created cleanly; otherwise mark the rule not applicable for headline evaluation.
- `GT-GPS-CONFIG-CORS-001` -> `CONFIG-CORS-001`: vulnerable mode demonstrates a clearly unsafe credentialed arbitrary-origin policy against a protected response; corrected mode enforces the frozen safe policy.
- `GT-GPS-CONFIG-ERROR-001` -> `CONFIG-ERROR-001`: bounded malformed input exposes synthetic/framework internals in vulnerable mode; corrected mode sanitises it.
- `GT-GPS-CONFIG-DOCS-001` -> `CONFIG-DOCS-001`: vulnerable mode exposes deliberately non-public operation metadata according to the frozen case; corrected mode applies the expected safe behaviour.
- `GT-GPS-INVENTORY-001` -> `INVENTORY-DIFF-001`: a bounded known live route is absent from the vulnerable specification; corrected state restores inventory agreement or removes the route according to the frozen case definition.

Additional headline cases may be added before final freeze only if they are independently testable and do not inflate the dataset merely to improve metrics.

## 7. Ground-truth manifest

Path:

`labs/government-permit-service-fastapi/ground-truth/manifest.yaml`

Recommended case structure:

```yaml
schema_version: 1
lab_id: government-permit-service-fastapi
lab_version: 1
fixture_version: 1
cases:
  - case_id: GT-GPS-BOLA-READ-001
    rule_id: AUTHZ-BOLA-001
    operation_key: APP-READ
    fixture_key: application-b
    attacker_identity: applicant-a
    owner_identity: applicant-b
    positive_mode: vulnerable
    negative_mode: corrected
```

Ground truth describes service security behaviour, not scanner heuristics.

## 8. Primary evaluation unit

Headline case tuple:

```text
(lab_id, mode, case_id, expected_rule_id, operation_key, fixture/property key)
```

Vulnerable mode is the positive unit; corrected mode is its paired negative unit. Matching uses committed deterministic IDs/dimensions, never free-text similarity.

## 9. Direct proof before scanner tuning

For each seeded case, P2 direct tests prove:

1. vulnerable mode exposes exactly the intended condition;
2. corrected mode removes it;
3. unrelated workflow behaviour remains equivalent;
4. reset restores canonical state;
5. ground-truth metadata matches direct semantics.

## 10. Final freeze

Before final P9 data collection, freeze/hash lab and fixture versions, ground truth, rule catalogue, case tuples, matcher, metric/state treatment, scanner profile and ZAP configuration. Any later methodological change invalidates/restarts the affected controlled experiment set and is documented.
