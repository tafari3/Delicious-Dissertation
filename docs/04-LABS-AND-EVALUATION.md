# Laboratory and Evaluation Protocol

## 1. Purpose

The dissertation separates a controlled accuracy experiment from later real-world validation. The controlled lab provides independent ground truth; the ZCHPC operational stage provides applicability evidence but is not assumed to have complete ground truth.

## 2. Canonical controlled lab

**ID:** `government-permit-service-fastapi`

**Name:** Synthetic Government Permit and Service Application API

**Host context:** Linux VM already provided by ZCHPC.

**Stack:** FastAPI + small relational database, containerised where permitted.

**Roles:** `applicant-a`, `applicant-b`, `officer`, `admin`.

Representative entities: application, applicant profile, document metadata, application status, officer decision/approval and small admin surface.

## 3. Lab contract

The lab must provide:

- synthetic data only;
- vulnerable and corrected modes;
- deterministic seed/reset;
- stable logical fixture IDs;
- controlled identities/roles;
- OpenAPI description;
- health/version/mode/fixture metadata;
- machine-readable independent ground truth;
- direct functional tests proving each vulnerable and corrected case without scanner code;
- no production/external service dependency.

## 4. Ground truth

Recommended path:

`labs/government-permit-service-fastapi/ground-truth/manifest.yaml`

Ground truth describes intended service behaviour, not scanner heuristics. Scanner detector packages cannot read/import it.

## 5. Controlled evaluation

Before each run:

1. reset and seed lab;
2. verify lab ID/version/mode/fixture version;
3. record ground-truth hash in the evaluation layer only;
4. run scanner under frozen profile;
5. store canonical result/report;
6. run applicable ZAP baseline;
7. match findings to frozen cases deterministically.

Invalid/failed runs remain in the dataset with reasons.

## 6. Metrics

Report TP, FP and FN; TN/FPR only where a defensible executed negative-case denominator exists. Calculate precision, recall and F1. Also record scan duration, request count, `INCONCLUSIVE`/`ERROR` outcomes, evidence/report reproducibility and repeated-run stability.

The exact repetition count, matcher, formulas/state treatment, scanner profile, lab/fixture versions and ZAP baseline are frozen before final controlled data collection.

## 7. OWASP ZAP

ZAP is a general-purpose comparison baseline only where equivalent observation is practical. Record each case as `EQUIVALENTLY_TESTABLE`, `PARTIALLY_TESTABLE` or `NOT_EQUIVALENTLY_TESTABLE`. Do not call unsupported multi-identity semantics ordinary ZAP false negatives.

## 8. Authorised ZCHPC validation

This starts only after P9 controlled-lab acceptance.

The scanner is then applied to the actual ZCHPC cloud environment only within the signed project authorisation. Exact targets, credentials and sensitive scope details remain local and are not committed.

Use the `authorised-zchpc` profile:

- read-only/non-destructive by default;
- stricter traffic ceilings;
- exact allow-list and address policy;
- approved test identities only;
- no deliberately introduced operational weaknesses;
- no hypervisor exploitation, VM escape, DoS, persistence, lateral movement or unrelated-tenant access.

Potential observations depend on approved interfaces and may include API/service exposure, authentication/access-control behaviour, TLS/HTTP configuration, exposed documentation, service inventory differences and safe externally observable deployment misconfigurations.

## 9. Separate interpretation

Controlled lab findings support quantitative accuracy because ground truth is known.

ZCHPC findings support applicability/repeatability/evidence-quality analysis. Do not calculate recall/FN/FPR against an operational environment unless an independently justified complete denominator exists. Do not claim a limited authorised validation certifies the entire ZCHPC cloud.

## 10. Final gates

P9 cannot close until controlled ground truth, matching, metrics, reporting and ZAP comparison are reproducible.

P10 cannot begin operational scanning until P9 passes and the authorised-ZCHPC local configuration is reviewed against the signed scope.
