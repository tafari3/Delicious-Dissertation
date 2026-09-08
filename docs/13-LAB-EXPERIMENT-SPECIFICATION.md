# Laboratory Experiment Specification

## 1. Purpose and freeze point

This document defines the canonical synthetic e-government laboratory contract that implementation and evaluation must share. It removes ambiguity about roles, operations, seeded security cases, corrected behaviour and evaluation matching before scanner detection logic is tuned against the laboratories.

Ground truth belongs to the laboratory/evaluation layer. Ordinary scanner detection code must never read this document or generated ground-truth manifests at runtime to decide whether a target is vulnerable.

The detailed manifest schema may evolve during P2/P9, but the research semantics below must remain stable unless changed through a reviewed methodology update before final data collection.

## 2. Common laboratory contract

All three labs MUST provide:

- one deterministic vulnerable mode and one deterministic corrected mode;
- the same normal business workflow in both modes except for intentional seeded differences;
- synthetic records only;
- stable logical fixture IDs;
- controlled role/identity fixtures;
- deterministic seed/reset;
- health/version/mode endpoint or equivalent deterministic metadata;
- OpenAPI 3.x description or equivalent import artefact;
- direct functional tests proving every seeded positive and paired corrected negative case;
- loopback-only canonical publication;
- no external production dependency;
- no privileged container, host networking, Docker socket or unnecessary host mounts.

Canonical modes:

```text
vulnerable
corrected
```

Canonical common metadata endpoint recommendation:

```text
GET /_lab/meta
```

Response fields should include at minimum `lab_id`, `lab_version`, `mode`, `fixture_version` and non-secret build provenance.

## 3. Stable fixture naming

Use logical fixture names in manifests/evaluation rather than relying on database-generated IDs.

Examples:

```text
citizen-a
citizen-b
patient-a
patient-b
applicant-a
applicant-b
registry-officer
clinician
processing-officer
supervisor
admin
citizen-profile-a
citizen-profile-b
health-record-a
health-record-b
permit-application-a
permit-application-b
```

Internally, services may use UUIDs. Reset tooling must produce a stable logical-name-to-runtime-ID map when runtime IDs are needed.

## 4. Lab A — Citizen Records API

**Canonical lab ID:** `citizen-records-fastapi`

**Stack:** Python / FastAPI

### 4.1 Roles

- `citizen-a`
- `citizen-b`
- `registry-officer`
- `admin`

### 4.2 Representative entities

- citizen profile;
- contact/address details;
- citizen service application/request;
- record verification status;
- officer case note;
- administrative account/record function.

### 4.3 Minimum operation contract

Paths may be refined during P2, but operation keys and semantics must remain traceable.

| Operation key | Suggested API operation | Intended normal access |
|---|---|---|
| `CR-PROFILE-READ` | `GET /api/v1/citizens/{citizen_id}` | citizen owns record; officer/admin according to policy |
| `CR-PROFILE-UPDATE` | `PATCH /api/v1/citizens/{citizen_id}` | citizen may update allowed self-service fields only |
| `CR-APPLICATION-READ` | `GET /api/v1/applications/{application_id}` | owning citizen and authorised staff |
| `CR-APPLICATION-UPDATE` | `PATCH /api/v1/applications/{application_id}` | controlled allowed fields by owner/staff |
| `CR-VERIFY` | `POST /api/v1/admin/citizens/{citizen_id}/verify` | officer/admin only |
| `CR-LEGACY-LOOKUP` | `GET /api/v1/legacy/citizen-lookup/{citizen_id}` | intentionally undocumented case when enabled |

### 4.4 Seeded cases

At minimum:

- `GT-CR-BOLA-READ-001` -> `AUTHZ-BOLA-001`: `citizen-a` can read `citizen-b` protected profile in vulnerable mode; corrected mode denies or safely masks access.
- `GT-CR-BOLA-WRITE-001` -> `AUTHZ-BOLA-002`: `citizen-a` can change a disposable allowed-profile field on `citizen-b`; corrected mode prevents the change.
- `GT-CR-BFLA-001` -> `AUTHZ-BFLA-001`: citizen can invoke the privileged verification function on a disposable fixture; corrected mode restricts it to staff.
- `GT-CR-BOPLA-WRITE-001` -> `AUTHZ-BOPLA-002`: citizen can set a protected server-controlled field such as `verification_status`; corrected mode ignores/rejects and does not persist it.
- `GT-CR-AUTHN-001` -> `AUTHN-MISSING-001`: one protected application/profile operation accepts anonymous access in vulnerable mode; corrected mode requires authentication.
- `GT-CR-INVENTORY-001` -> `INVENTORY-DIFF-001`: controlled legacy operation is live but absent from the vulnerable-mode specification fixture; paired corrected/documented mode restores inventory agreement or removes the route according to the frozen case definition.

Optional configuration cases may be added only if they remain bounded and independently testable.

## 5. Lab B — Public Health Records API

**Canonical lab ID:** `public-health-express`

**Stack:** Node.js / Express

### 5.1 Roles

- `patient-a`
- `patient-b`
- `clinician`
- `records-officer`
- `admin`

### 5.2 Representative entities

- patient profile;
- appointment;
- laboratory result;
- synthetic clinical record/summary;
- records-administration field;
- clinician/records workflow.

All health data is invented and must be visibly synthetic.

### 5.3 Minimum operation contract

| Operation key | Suggested API operation | Intended normal access |
|---|---|---|
| `PH-PATIENT-READ` | `GET /api/v1/patients/{patient_id}` | patient owns record; authorised clinician/staff according to policy |
| `PH-LAB-RESULT-READ` | `GET /api/v1/lab-results/{result_id}` | owning patient and authorised clinician |
| `PH-APPOINTMENT-READ` | `GET /api/v1/appointments/{appointment_id}` | owning patient and authorised staff |
| `PH-PATIENT-UPDATE` | `PATCH /api/v1/patients/{patient_id}` | restricted self-service fields or authorised staff |
| `PH-RECORDS-FLAG` | `PATCH /api/v1/records/{record_id}` | records officer/admin only for protected fields |
| `PH-ADMIN-EXPORT` | `GET /api/v1/admin/records/summary` | admin/authorised records staff only; synthetic bounded summary only |

### 5.4 Seeded cases

At minimum:

- `GT-PH-BOLA-READ-001` -> `AUTHZ-BOLA-001`: `patient-a` can read `patient-b` laboratory result; corrected mode denies/masks it.
- `GT-PH-BFLA-001` -> `AUTHZ-BFLA-001`: patient can reach a staff-only bounded records function; corrected mode enforces role control.
- `GT-PH-BOPLA-READ-001` -> `AUTHZ-BOPLA-001`: restricted role receives a protected synthetic administrative property; corrected mode omits it.
- `GT-PH-BOPLA-WRITE-001` -> `AUTHZ-BOPLA-002`: restricted role can persist a protected records field on a disposable synthetic record; corrected mode prevents persistence.
- `GT-PH-AUTHN-SESSION-001` -> `AUTHN-SESSION-001` or `AUTHN-EXPIRED-001`: deterministic revoked/expired test token remains accepted in vulnerable mode; corrected mode rejects it.
- `GT-PH-CONFIG-ERROR-001` -> `CONFIG-ERROR-001`: a bounded malformed parameter exposes a synthetic/framework stack detail in vulnerable mode; corrected mode returns a sanitised error.

Optional CORS/header observations may be included if their expected semantics are explicit and do not depend on browser-page assumptions.

## 6. Lab C — Permit & Licensing API

**Canonical lab ID:** `permit-licensing-spring`

**Stack:** Java / Spring Boot

### 6.1 Roles

- `applicant-a`
- `applicant-b`
- `processing-officer`
- `supervisor`
- `admin`

### 6.2 Representative entities

- permit/licence application;
- supporting document metadata;
- application status;
- permit/licence record;
- processing note;
- approval/supervisor action.

### 6.3 Minimum operation contract

| Operation key | Suggested API operation | Intended normal access |
|---|---|---|
| `PL-APPLICATION-READ` | `GET /api/v1/applications/{application_id}` | owning applicant and authorised staff |
| `PL-APPLICATION-UPDATE` | `PATCH /api/v1/applications/{application_id}` | applicant allowed fields; staff workflow fields restricted |
| `PL-DOCUMENT-READ` | `GET /api/v1/documents/{document_id}` | owning applicant and authorised staff |
| `PL-APPROVE` | `POST /api/v1/applications/{application_id}/approve` | supervisor/admin only |
| `PL-LICENCE-READ` | `GET /api/v1/licences/{licence_id}` | owner/authorised staff according to policy |
| `PL-DOCS` | `/docs` or `/openapi.*` equivalent | exposure classification depends on seeded case/context |

### 6.4 Seeded cases

At minimum:

- `GT-PL-BOLA-READ-001` -> `AUTHZ-BOLA-001`: `applicant-a` can read `applicant-b` application/document; corrected mode denies/masks it.
- `GT-PL-BOLA-WRITE-001` -> `AUTHZ-BOLA-002`: `applicant-a` can modify a disposable applicant-owned field on `applicant-b` application; corrected mode prevents it.
- `GT-PL-BFLA-001` -> `AUTHZ-BFLA-001`: applicant/processing officer below required privilege can invoke approval; corrected mode permits supervisor/admin only.
- `GT-PL-BOPLA-WRITE-001` -> `AUTHZ-BOPLA-002`: applicant can persist protected `status`, `approved_by` or equivalent synthetic workflow field; corrected mode prevents persistence.
- `GT-PL-AUTHN-INCONSISTENT-001` -> `AUTHN-INCONSISTENT-001`: one sibling protected operation has inconsistent authentication in vulnerable mode; corrected mode aligns requirements.
- `GT-PL-CONFIG-DOCS-001` -> `CONFIG-DOCS-001`: vulnerable mode exposes documentation containing deliberately non-public operation metadata; corrected mode applies the frozen expected safe behaviour.

A bounded rate-control case may be placed here if it can be proven under the strict resource-test sub-budget without stress behaviour.

## 7. Coverage matrix

The labs must collectively provide positive and paired corrected cases for the dissertation's high-value catalogue. P2 should not create dozens of duplicate vulnerabilities merely to inflate sample size.

Minimum intended coverage:

| Rule family | Citizen Records | Public Health | Permit & Licensing |
|---|---:|---:|---:|
| BOLA read | required | required | required |
| BOLA controlled mutation | required | optional | required |
| BFLA | required | required | required |
| BOPLA read | optional | required | optional |
| BOPLA write/mass assignment | required | required | required |
| Missing/invalid/session auth | required | required | required via one auth family case |
| Error/config observation | optional | required | optional |
| Documentation/inventory | required inventory | optional | required docs |
| Bounded resource control | optional | optional | one safe case if retained |

P2 may refine exact distribution, but every final implemented rule used in headline evaluation must have a predeclared positive and negative evaluation case somewhere in the suite.

## 8. Ground-truth manifest model

Recommended per-lab path:

```text
labs/<lab-id>/ground-truth/manifest.yaml
```

Recommended case structure:

```yaml
schema_version: 1
lab_id: citizen-records-fastapi
lab_version: 1
fixture_version: 1
cases:
  - case_id: GT-CR-BOLA-READ-001
    rule_id: AUTHZ-BOLA-001
    operation_key: CR-PROFILE-READ
    fixture_key: citizen-profile-b
    attacker_identity: citizen-a
    owner_identity: citizen-b
    positive_mode: vulnerable
    negative_mode: corrected
    expected_vulnerable_behavior: protected record becomes observable to wrong identity
    expected_corrected_behavior: access is denied or safely masked without protected record disclosure
```

Do not encode scanner-specific heuristic outputs into ground truth. Ground truth describes intended service security behaviour.

## 9. Primary evaluation unit and deterministic matching

For final headline metrics, the primary evaluation unit is a predeclared case tuple equivalent to:

```text
(lab_id, mode, case_id, expected_rule_id, operation_key, fixture/property key)
```

For each paired case:

- vulnerable mode is the positive unit;
- corrected mode is the negative unit.

A scanner finding matches a case only through the committed matcher using rule ID plus the relevant operation/fixture/property dimensions. Free-text similarity is not a valid matcher.

Headline classification:

- **TP:** matching `CONFIRMED` finding for a positive vulnerable-mode case;
- **FN:** no matching `CONFIRMED` finding for a positive vulnerable-mode case after a valid completed test; preserve `INCONCLUSIVE`/`ERROR` separately in diagnostic analysis rather than silently treating failed runs as normal negatives;
- **FP:** matching `CONFIRMED` finding for the paired corrected-mode negative case;
- **TN:** no matching `CONFIRMED` finding for a valid, actually executed paired corrected-mode negative case.

Before P9 finalizes metric code, document treatment of `SUSPECTED`, `INCONCLUSIVE`, `NOT_APPLICABLE` and `ERROR` for headline versus secondary analyses. Do not choose this treatment after seeing final performance.

Unexpected scanner findings outside predeclared headline case tuples must be retained and reported separately. They may be investigated, but must not be silently discarded or retroactively converted into ground-truth cases to improve metrics.

## 10. Direct lab functional proof

Before scanner rule implementation is tuned against a case, direct lab tests must prove:

1. vulnerable mode exposes exactly the intended weakness;
2. corrected mode fixes that weakness;
3. unrelated workflow behaviour remains equivalent across modes;
4. reset restores the canonical fixture state;
5. ground-truth case metadata matches the direct test semantics.

This is the primary defence against circular evaluation.

## 11. Evaluation repetition

Final key profiles should be repeated using the value frozen in the methodology before final data collection. The current engineering default is five runs per lab/mode/profile, but this is a reproducibility check rather than a claim of statistical power.

Every run must retain validity state and reason. Failed, flaky or inconvenient runs are not silently removed.

## 12. OWASP ZAP comparison

ZAP is a general-purpose baseline, not an identical implementation of the proposed scanner.

For every ground-truth case, the evaluation dataset must record a ZAP applicability state such as:

```text
EQUIVALENTLY_TESTABLE
PARTIALLY_TESTABLE
NOT_EQUIVALENTLY_TESTABLE
```

Only equivalent/meaningfully comparable cases should be used for direct detection comparison. Unsupported multi-identity semantic authorisation behaviour must not be labelled a conventional ZAP false negative merely because the proposed scanner has a different capability.

## 13. Optional independent benchmark

The academic proposal allows an independently developed deliberately vulnerable API benchmark as secondary validation if schedule permits. It is optional and must never displace the three required e-government labs or change their ground truth after scanner results are observed.

## 14. Final freeze rule

Before P10 final data collection, freeze and hash/version:

- all ground-truth manifests;
- lab images/versions and fixture versions;
- rule catalogue versions;
- evaluation case tuples;
- matching logic;
- metric formulas and state-treatment rules;
- scanner profile;
- ZAP version/configuration.

A later methodological change invalidates and restarts the affected experiment set, with the change recorded explicitly.
