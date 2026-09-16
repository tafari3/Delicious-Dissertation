# Controlled Cloud and Evaluation Protocol

## 1. Purpose

The dissertation separates a controlled cloud accuracy experiment from later real-world ZCHPC validation. The controlled XCP-ng/Xen Orchestra replica provides independent ground truth; the ZCHPC operational stage provides applicability evidence but is not assumed to have complete ground truth.

## 2. Controlled cloud

**Virtualisation:** XCP-ng hypervisor with Xen Orchestra management/orchestration.

**Application lab ID:** `government-permit-service-fastapi`

**Application name:** Synthetic Government Permit and Service Application API

**Application stack:** FastAPI + small relational database, containerised where useful.

**Application roles:** `applicant-a`, `applicant-b`, `officer`, `admin`.

Representative entities: application, applicant profile, document metadata, application status, officer decision/approval and small admin surface.

Minimum logical cloud roles are scanner VM, target API VM and Xen Orchestra management. A database/supporting VM is preferred where resources permit but may be consolidated with the target if documented.

## 3. Application lab contract

The application lab must provide:

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

## 4. Controlled deployment/cloud cases

The replica cloud may contain selected bounded, reversible cases such as:

- unnecessary service/port exposure;
- incorrect firewall/network reachability;
- management service exposure to an inappropriate lab network;
- database reachability from a disallowed lab segment;
- insecure service binding;
- selected TLS/certificate configuration weakness;
- weak segmentation between controlled VMs/networks;
- lab-only role/permission misconfiguration where deterministic and safe;
- backup/snapshot exposure only where a contained non-destructive case exists.

Each case must have a stable case ID, expected secure state and direct proof method. Do not add VM escape, destructive hypervisor exploitation, persistence, lateral movement or DoS as controlled cases.

## 5. Ground truth

Recommended application path:

`labs/government-permit-service-fastapi/ground-truth/manifest.yaml`

Recommended cloud/deployment path:

`evaluation/ground-truth/controlled-cloud.yaml`

Ground truth describes intended service/configuration behaviour, not scanner heuristics. Scanner detector packages cannot read/import it while deciding findings.

Before scanner tuning for final evaluation, direct tests/configuration checks prove each case and its corrected/secure counterpart independently.

## 6. Controlled evaluation

Before each final controlled run:

1. restore/verify the declared replica-cloud state;
2. reset and seed the synthetic application;
3. verify cloud/lab/case versions and hashes;
4. record ground-truth hashes in the evaluation layer only;
5. run the scanner under the frozen profile;
6. store canonical result/report;
7. run the applicable ZAP baseline;
8. match scanner findings to frozen cases deterministically;
9. retain failed/invalid runs with explicit reasons.

## 7. Metrics

Report TP, FP and FN; TN/FPR only where a defensible executed negative-case denominator exists. Calculate precision, recall and F1. Also record scan duration, request count, `INCONCLUSIVE`/`ERROR` outcomes, evidence/report reproducibility and repeated-run stability.

The exact repetition count, matcher, formulas/state treatment, scanner profile, cloud/lab versions, ground truth and ZAP baseline are frozen before final controlled data collection. Repetition count is reported as a study protocol choice, not as an automatic guarantee of statistical significance.

## 8. OWASP ZAP

ZAP is a general-purpose comparison baseline only where equivalent observation is practical. Record each case as `EQUIVALENTLY_TESTABLE`, `PARTIALLY_TESTABLE` or `NOT_EQUIVALENTLY_TESTABLE`. Do not call unsupported multi-identity semantics ordinary ZAP false negatives.

Cloud/deployment cases outside ZAP's equivalent observation surface are reported as coverage differences rather than forced into misleading scanner-versus-ZAP accuracy counts.

## 9. Gate to operational validation

P10 cannot begin until the controlled environment demonstrates:

- enforced target allow-listing;
- hard request/rate/concurrency budgets;
- evidence/secret redaction;
- deterministic reset/state verification;
- reproducible findings/reports;
- sufficient discrimination between seeded insecure/vulnerable states and corrected/secure states;
- no unresolved critical safety failures.

## 10. Authorised ZCHPC validation

The scanner is then applied to the actual ZCHPC cloud environment only within the signed project authorisation. Exact targets, credentials and sensitive scope details remain local and are not committed.

Use the `authorised-zchpc` profile:

- read-only/non-destructive by default;
- stricter traffic ceilings;
- exact allow-list and address policy;
- approved test identities only;
- no deliberately introduced operational weaknesses;
- no hypervisor exploitation, VM escape, DoS, persistence, lateral movement or unrelated-tenant access.

Potential observations depend on approved interfaces and may include API/service exposure, authentication/access-control behaviour, TLS/HTTP configuration, exposed documentation, service inventory differences and safe externally observable deployment misconfigurations.

## 11. Separate interpretation

Controlled cloud findings support quantitative accuracy because ground truth is known.

ZCHPC findings support applicability, confirmation workflow, repeatability, evidence quality, runtime/request-count and operational-safety analysis. Do not calculate recall/FN/FPR against an operational environment unless an independently justified complete denominator exists. Do not claim a limited authorised validation certifies the entire ZCHPC cloud.

## 12. Final gates

P9 cannot close until controlled ground truth, matching, metrics, reporting and ZAP comparison are reproducible.

P10 cannot begin operational scanning until P9 passes and the authorised-ZCHPC local configuration is reviewed against the signed scope.
