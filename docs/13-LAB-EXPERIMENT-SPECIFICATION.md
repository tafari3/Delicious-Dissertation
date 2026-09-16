# Controlled Replica-Cloud Experiment Specification

## 1. Purpose

This is the canonical contract for the controlled Stage 1 environment used to prove scanner safety, accuracy and repeatability before ZCHPC operational validation.

The controlled environment contains one synthetic e-government application deployed inside a small XCP-ng/Xen Orchestra research cloud plus a bounded set of reversible deployment/cloud misconfiguration cases.

Ground truth belongs to lab/evaluation code. Ordinary scanner detection code must never read this document or generated ground-truth manifests at runtime to decide whether the target is vulnerable.

## 2. Cloud identity and topology

**Virtualisation:** XCP-ng hypervisor.

**Management/orchestration:** Xen Orchestra.

Xen Orchestra is not the hypervisor. It may run as a VM/appliance or on another approved management node according to the actual lab deployment.

Minimum logical roles:

- scanner VM;
- synthetic e-government API VM;
- database/supporting service, preferably separate where resources permit;
- Xen Orchestra management/orchestration;
- management and service/test network roles kept distinct wherever feasible.

The exact hostnames, IP addresses, VLAN IDs, storage repositories and credentials are environment-specific and must be recorded from the actual controlled lab rather than invented in this repository.

## 3. Application lab identity

**ID:** `government-permit-service-fastapi`

**Name:** Synthetic Government Permit and Service Application API

**Stack:** Python/FastAPI + small relational database.

The application is a representative research workflow, not a replica of a named ministry, agency or ZCHPC production application.

## 4. Common application contract

The lab must provide:

- `vulnerable` and `corrected` modes;
- the same ordinary workflow in both modes except intentional seeded differences;
- synthetic users/records/documents/application states only;
- stable logical fixture IDs;
- deterministic seed/reset;
- health/lab-version/mode/fixture metadata;
- OpenAPI 3.x description;
- direct functional tests proving positive and paired corrected cases;
- machine-readable independent ground truth;
- no production/external dependency;
- controlled exposure inside the replica cloud.

Recommended metadata endpoint: `GET /_lab/meta`.

## 5. Roles and fixtures

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

## 6. Minimum operation contract

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

## 7. Headline application cases

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

## 8. Headline controlled cloud/deployment cases

P2/P9 may implement a manageable subset of the following, using stable IDs and direct proof:

- `GT-CLD-NET-001`: a management/service endpoint is reachable from a lab network that should not reach it; secure state removes that reachability.
- `GT-CLD-DB-001`: database port is reachable from the scanner/user-facing lab segment when the expected secure state permits only the application path.
- `GT-CLD-BIND-001`: a supporting service binds to an unnecessarily broad interface; secure state restricts binding.
- `GT-CLD-PORT-001`: an unnecessary service/port is exposed to the controlled test segment; secure state removes or restricts it.
- `GT-CLD-TLS-001`: a selected deterministic TLS/certificate configuration weakness exists on a controlled endpoint; secure state corrects it.
- `GT-CLD-SEG-001`: a declared network-segmentation rule is intentionally weakened in the replica; secure state restores the rule.

Optional cases such as lab-only permission or backup/snapshot exposure require a deterministic, reversible and non-destructive proof method before inclusion.

Do not seed VM escape, hypervisor exploit, persistence, lateral movement or DoS cases.

## 9. Ground-truth manifests

Application path:

`labs/government-permit-service-fastapi/ground-truth/manifest.yaml`

Controlled cloud/deployment path:

`evaluation/ground-truth/controlled-cloud.yaml`

Recommended application case structure:

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

Recommended cloud case structure:

```yaml
schema_version: 1
cloud_lab_id: controlled-xcpng-xo
cloud_lab_version: 1
cases:
  - case_id: GT-CLD-DB-001
    observation_type: network_reachability
    source_role: scanner
    target_role: database
    expected_insecure_state: reachable
    expected_secure_state: blocked
```

Ground truth describes actual service/configuration behaviour, not scanner heuristics.

## 10. Primary evaluation units

Application case tuple:

```text
(lab_id, mode, case_id, expected_rule_id, operation_key, fixture/property key)
```

Controlled cloud case tuple:

```text
(cloud_lab_id, state, case_id, observation_type, source_role, target_role)
```

Vulnerable/insecure state is the positive unit; corrected/secure state is its paired negative unit. Matching uses committed deterministic IDs/dimensions, never free-text similarity.

## 11. Direct proof before scanner tuning

For each application case, direct tests prove:

1. vulnerable mode exposes exactly the intended condition;
2. corrected mode removes it;
3. unrelated workflow behaviour remains equivalent;
4. reset restores canonical state;
5. ground-truth metadata matches direct semantics.

For each controlled cloud case, direct configuration/reachability proof establishes the insecure state and the corrected secure state independently of scanner output. The proof mechanism itself must remain bounded and non-destructive.

## 12. Final freeze

Before final P9 data collection, freeze/hash cloud topology/version metadata, lab and fixture versions, ground truth, rule catalogue, case tuples, matcher, metric/state treatment, scanner profile and ZAP configuration. Any later methodological change invalidates/restarts the affected controlled experiment set and is documented.
