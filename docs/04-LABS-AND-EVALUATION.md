# Laboratories and Evaluation Protocol

## 1. Purpose

The dissertation evaluates the scanner against known, independently defined ground truth rather than unknown live systems. The laboratory suite is therefore a first-class research artefact, not merely demonstration infrastructure.

The laboratories must permit repeatable measurement of detection performance, false-positive behaviour, cross-stack portability and evidence reproducibility while using synthetic data only.

The detailed lab contract is frozen in `docs/13-LAB-EXPERIMENT-SPECIFICATION.md` and takes precedence over examples in this document.

## 2. Required laboratory stacks and scenarios

The current locked mapping is:

1. **Python / FastAPI** — Citizen Records API;
2. **Node.js / Express** — Public Health Records API;
3. **Java / Spring Boot** — Permit & Licensing API.

The scenario-to-stack mapping may be changed only through a reviewed design change if the total set still contains three materially different server implementation stacks and the academic baseline remains satisfied.

## 3. Common laboratory contract

Every lab must provide:

- Dockerfile/build definition;
- health endpoint;
- deterministic lab metadata including lab ID/version/mode;
- OpenAPI description or equivalent import artefact;
- deterministic seed/reset procedure;
- synthetic fixtures only;
- controlled identities and roles;
- vulnerable and corrected modes/versions;
- machine-readable independent ground truth;
- stable fixture identifiers where authorisation tests require them;
- direct functional tests proving vulnerable and corrected behaviour without using scanner detection logic;
- no dependency on external production services.

Canonical vulnerable laboratories publish to loopback only and run without privileged containers, host networking or Docker-socket access.

## 4. Scenario A — Citizen Records API

**Lab ID:** `citizen-records-fastapi`

Representative roles:

- `citizen-a`;
- `citizen-b`;
- `registry-officer`;
- `admin`.

Representative entities:

- citizen profile;
- contact/address information;
- service application/request;
- verification state;
- officer case-management information.

Seeded cases include controlled BOLA read/mutation, BFLA, protected-property write, missing authentication and an inventory mismatch as specified in `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`.

No real citizen identity or production record is used.

## 5. Scenario B — Public Health Records API

**Lab ID:** `public-health-express`

Representative roles:

- `patient-a`;
- `patient-b`;
- `clinician`;
- `records-officer`;
- `admin`.

Representative entities:

- patient profile;
- appointment;
- laboratory result;
- synthetic clinical record/summary;
- administrative records fields.

Seeded cases include controlled BOLA, BFLA, protected-property exposure/write, deterministic token/session behaviour and bounded error leakage as specified in the laboratory experiment specification.

All health data is explicitly synthetic.

## 6. Scenario C — Permit & Licensing API

**Lab ID:** `permit-licensing-spring`

Representative roles:

- `applicant-a`;
- `applicant-b`;
- `processing-officer`;
- `supervisor`;
- `admin`.

Representative entities:

- permit/licence application;
- supporting document metadata;
- application status;
- licence/permit record;
- processing note;
- approval action.

Seeded cases include controlled BOLA read/mutation, BFLA approval, mass assignment/protected-property write, inconsistent authentication and documentation exposure as specified in the laboratory experiment specification.

## 7. Representative, not replica

The labs reproduce common public-service access-control relationships for research. They do **not** claim to reproduce the internal architecture, endpoints, databases, security posture or implementation of any named Zimbabwean ministry, agency, department or ZCHPC service.

Evaluation results apply to the research artefact and the controlled test environments only.

## 8. Ground-truth manifest

Each lab must have a version-controlled manifest such as:

```text
labs/<lab-id>/ground-truth/manifest.yaml
```

Ground truth describes intended service security behaviour and its paired vulnerable/corrected cases. It must not contain scanner heuristic expectations beyond the stable scanner rule ID used for deterministic matching.

A representative structure is defined in `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`.

The scanner detector packages must not read/import these manifests during ordinary scanning.

## 9. Vulnerable versus corrected state

Preferred design:

- same service and synthetic fixtures;
- vulnerability behaviour toggled through a deterministic mode/profile or controlled build variant;
- corrected state removes the seeded weakness without changing unrelated workflow semantics.

This enables direct A/B evaluation and a defensible paired negative case.

Avoid maintaining two unrelated applications that drift from one another.

## 10. Fixture model

Use stable logical fixture names rather than opaque runtime IDs where possible. Reset tooling may expose deterministic logical-to-runtime mappings if UUIDs are used internally.

Example logical references:

```text
citizen-a
citizen-b
citizen-profile-b
patient-a
patient-b
lab-result-b
applicant-a
applicant-b
permit-application-b
supervisor
admin
```

## 11. Reset invariant

Before every evaluation run:

1. stop/reset relevant lab state or invoke deterministic reset;
2. re-seed canonical fixtures;
3. verify health;
4. verify expected lab ID/version/mode;
5. verify fixture version;
6. verify ground-truth manifest hash/version in the evaluation layer.

A run without successful reset/verification is invalid research evidence and must be retained with its invalidity reason rather than silently discarded.

## 12. Evaluation dataset

Every scanner evaluation run should emit a machine-readable record containing at minimum:

- run ID;
- scanner commit/version;
- rule catalogue version;
- lab ID/version/mode;
- fixture version;
- ground-truth manifest hash;
- matching-logic version;
- specification hash;
- scan profile;
- start/end time and duration;
- requests sent;
- rule executions and scanner findings;
- matched ground-truth case IDs;
- TP/FP/FN/TN where defensibly applicable;
- errors/inconclusive cases;
- validity state/reason;
- environment/runtime metadata needed for reproduction.

## 13. Primary evaluation unit and matching

The primary headline evaluation unit is the predeclared case tuple defined in `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`.

Matching must use deterministic dimensions such as:

- lab ID;
- case ID;
- expected rule ID;
- operation key;
- fixture/property key;
- lab mode.

A finding must not become a TP merely because its free text resembles a seeded weakness.

Unexpected findings outside the predeclared headline case set remain visible and are analysed separately; they must not be discarded or retroactively turned into ground truth merely to improve metrics.

## 14. Core metrics

### Precision

```text
precision = TP / (TP + FP)
```

### Recall

```text
recall = TP / (TP + FN)
```

### F1 score

```text
F1 = 2 * precision * recall / (precision + recall)
```

### False-positive rate

Where a predeclared executed negative-case denominator gives defensible true negatives:

```text
FPR = FP / (FP + TN)
```

If TN is not meaningful for an analysis, report false positives and precision rather than manufacturing an FPR.

### Scan duration and request count

Record wall-clock duration together with transmitted request count and stopped/inconclusive states.

### Reproducibility/stability

Repeat key frozen evaluation profiles and report whether case-level outcomes remain consistent across runs. The exact repetition count and formula must be fixed before final data collection.

### Cross-stack portability

Report successful execution and relevant detection coverage across all three laboratory stacks without scanner logic changes tied to target implementation language.

## 15. Result-state treatment

The scanner preserves:

```text
NOT_APPLICABLE
PASS_OBSERVED
CONFIRMED
SUSPECTED
INFORMATIONAL
INCONCLUSIVE
ERROR
```

Before final data collection, P9 must freeze how each state contributes to headline and secondary metrics. `ERROR` and `INCONCLUSIVE` must never be silently converted into successful passes or removed from the dataset.

## 16. Repetition plan

The current engineering default is five repeated runs per lab/mode/final profile. This is primarily a stability/reproducibility check, not a claim of statistical sufficiency.

The exact number is frozen before final collection. Every run is retained with validity metadata.

## 17. OWASP ZAP baseline

OWASP ZAP is the general-purpose baseline named in the proposal.

Baseline principles:

- pin/document a ZAP version/container;
- use the same reset laboratory state and scope;
- import OpenAPI where supported;
- configure authentication where practical and reproducible;
- preserve raw baseline output in sanitised research artefacts as appropriate;
- normalize findings without rewriting their meaning;
- record an explicit applicability/coverage dimension.

For each case classify ZAP comparability, for example:

```text
EQUIVALENTLY_TESTABLE
PARTIALLY_TESTABLE
NOT_EQUIVALENTLY_TESTABLE
```

Do not count unsupported multi-identity semantic authorisation behaviour as an ordinary ZAP false negative merely because the proposed scanner implements a different testing model.

## 18. Optional independent benchmark

An independently developed deliberately vulnerable API benchmark may be used as a secondary validation target if schedule permits. It is optional. It must use a safe local/authorised deployment and must not displace the three required e-government labs.

## 19. Optional ZCHPC laboratory deployment

If formal permission/resources are granted, an isolated copy of the student's own laboratory environment may be deployed to an authorised ZCHPC test resource to examine portability in a local cloud context.

This is optional and does not change the target scope: ZCHPC production services, management interfaces, unrelated tenants and production government applications are not evaluated.

Failure to obtain ZCHPC access does not block completion.

## 20. Evaluation scripts

Planned repository paths:

```text
evaluation/
  profiles/
  scripts/
  schemas/
  results/          # ignored or sample-only
  analysis/
```

Required conceptual commands:

```text
make labs-up
make labs-reset
make evaluate-scanner
make evaluate-zap
make evaluate-summary
```

The final evaluation must be runnable non-interactively from documented commands.

## 21. Research artefact preservation

Commit:

- evaluation schemas;
- scripts;
- ground-truth manifests;
- direct lab contract tests;
- small sanitised synthetic sample outputs;
- analysis code/notebooks if used;
- final redacted aggregate datasets suitable for dissertation reproduction.

Do not commit:

- secrets;
- real government/health/citizen data;
- production target data;
- bearer tokens/cookies;
- uncontrolled raw dumps containing sensitive material.

## 22. Threats to validity to control

Engineering must actively reduce:

- scanner detector logic learning/reading lab ground truth;
- mode drift beyond seeded cases;
- inconsistent difficulty caused by accidental lab differences;
- post-hoc matcher changes;
- post-hoc metric/state-treatment changes;
- selective removal of failed/poor runs;
- unfair ZAP comparison;
- data leakage between repetitions;
- timing flakiness in resource-control tests;
- manually relabelling ambiguous outcomes after seeing scanner results.

## 23. Final evaluation acceptance gate

Final research data collection does not begin until:

1. all three labs reset deterministically;
2. direct lab functional tests prove vulnerable and corrected behaviour;
3. ground-truth manifests are reviewed, versioned and frozen;
4. scanner profile and rule catalogue are frozen/versioned;
5. evaluation case tuples and matching logic are tested and frozen;
6. metric formulas and state-treatment rules are frozen;
7. ZAP baseline version/configuration is pinned/documented;
8. scanner verification suite passes;
9. evidence redaction tests pass;
10. the exact repository commit used for evaluation is tagged or otherwise immutably recorded.
