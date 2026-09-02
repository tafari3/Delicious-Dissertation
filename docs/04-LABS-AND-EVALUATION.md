# Laboratories and Evaluation Protocol

## 1. Purpose

The dissertation must evaluate the scanner against known ground truth, not against unknown live systems. The laboratory suite is therefore a first-class research artefact, not merely demo infrastructure.

The labs must prove that the scanner is cross-platform at the HTTP boundary and permit repeatable measurement of true positives, false positives and false negatives.

## 2. Required laboratory stacks

The initial locked stacks are:

1. **Python / FastAPI** — Mobile Money scenario;
2. **Node.js / Express** — Revenue/Tax scenario;
3. **Java / Spring Boot** — Citizen Services scenario.

The scenario-to-stack mapping may be swapped later only if the total set still contains three materially different server implementation stacks.

## 3. Common laboratory contract

Every lab must provide:

- Dockerfile;
- health endpoint;
- OpenAPI description or equivalent import artefact;
- deterministic seed/reset procedure;
- synthetic fixtures only;
- controlled identities and roles;
- vulnerable and corrected modes/versions;
- machine-readable ground truth;
- stable fixture identifiers where authorisation tests require them;
- test endpoint/base URL configuration;
- no dependency on external production services.

## 4. Scenario A — Mobile Money API

### Representative entities

- user/customer;
- wallet;
- beneficiary;
- transfer;
- transaction history;
- agent/support/admin operation where required for BFLA.

### Suggested roles

- `customer-a`;
- `customer-b`;
- `support-agent`;
- `admin`.

### Candidate seeded weaknesses

Use a controlled subset aligned with the scanner catalogue:

- BOLA read: customer A can read customer B wallet/transaction object by identifier;
- BOLA mutation: customer A can alter a disposable beneficiary or transfer metadata belonging to B;
- BOPLA: customer can set a protected property such as an internal status/limit flag on a disposable object;
- missing authentication on one protected route;
- verbose error leakage on a malformed-but-bounded parameter;
- CORS weakness;
- one undocumented/deprecated endpoint for inventory comparison;
- bounded rate-limit weakness/behaviour on a safe idempotent lookup or synthetic action.

The lab must not simulate irreversible monetary loss. All transfers are synthetic and disposable.

## 5. Scenario B — Revenue/Tax API

### Representative entities

- taxpayer profile;
- tax account;
- obligation;
- return/payment record;
- officer case/action;
- administrative configuration/report endpoint.

### Suggested roles

- `taxpayer-a`;
- `taxpayer-b`;
- `revenue-officer`;
- `admin`.

### Candidate seeded weaknesses

- BOLA on taxpayer/obligation lookup;
- BFLA where taxpayer can invoke officer-only operation using a harmless disposable record;
- sensitive property exposure in profile/account response;
- mass assignment on a protected status/property;
- inconsistent authentication between sibling endpoints;
- risky/unexpected HTTP method on a disposable resource;
- exposed API documentation with non-public operation metadata;
- specification/live inventory mismatch.

## 6. Scenario C — Citizen Services API

### Representative entities

- citizen profile;
- application/request;
- service record;
- case note/status;
- officer/admin workflow.

### Suggested roles

- `citizen-a`;
- `citizen-b`;
- `case-officer`;
- `admin`.

### Candidate seeded weaknesses

- cross-citizen profile/application read;
- cross-citizen disposable update;
- low-privilege access to case-officer/admin function;
- protected property exposure;
- expired/revoked controlled session accepted;
- security-header/TLS observations appropriate to local HTTPS mode where implemented;
- verbose error leak;
- documented endpoint absent or undocumented endpoint present.

## 7. Ground-truth manifest

Each lab must have a manifest under a path such as:

```text
labs/<lab>/ground-truth/manifest.yaml
```

Recommended schema:

```yaml
lab_id: mobile-money-fastapi
lab_version: 1
scenario: mobile-money
mode: vulnerable
vulnerabilities:
  - id: GT-MM-001
    rule_id: AUTHZ-BOLA-001
    endpoint: GET /wallets/{wallet_id}
    expected: vulnerable
    severity_hint: high
    fixture:
      owner_identity: customer-b
      attacker_identity: customer-a
      object_ref: wallet-b
    notes: Cross-user wallet read is intentionally permitted in vulnerable mode.
```

The exact schema can evolve, but it must remain machine-readable and version-controlled.

## 8. Vulnerable versus corrected state

Preferred design:

- same service and fixtures;
- vulnerability behaviour toggled through a deterministic mode/profile or separate container image/tag;
- corrected state removes the seeded weakness without changing unrelated semantics.

This enables direct A/B evaluation.

Avoid maintaining two unrelated applications that drift from each other.

## 9. Fixture model

Fixtures should include stable logical names rather than relying on opaque runtime database IDs where possible.

Example logical references:

```text
customer-a
customer-b
wallet-a
wallet-b
disposable-beneficiary-b
officer-only-case-1
```

The lab may internally use UUIDs, but reset tooling should expose deterministic fixture mapping to the evaluation harness.

## 10. Reset invariant

Before every evaluation run:

1. stop/reset relevant lab state or invoke deterministic reset;
2. re-seed canonical fixtures;
3. verify health;
4. verify expected lab mode/version;
5. verify ground-truth manifest hash/version.

A run without successful reset/verification is invalid research evidence.

## 11. Evaluation dataset

Every individual scanner evaluation run should emit a machine-readable record containing at minimum:

- run ID;
- scanner commit/version;
- lab ID/version/mode;
- ground-truth manifest hash;
- specification hash;
- scan profile;
- start/end time and duration;
- requests sent;
- scanner findings;
- matched ground-truth IDs;
- TP/FP/FN counts;
- errors/inconclusive cases;
- environment/runtime metadata needed for reproducibility.

## 12. Matching scanner findings to ground truth

Evaluation must use an explicit matching key/rule rather than manual judgement after results are seen.

Recommended primary matching dimensions:

- lab/ground-truth vulnerability ID;
- expected scanner rule ID;
- endpoint/operation or fixture scope;
- vulnerability mode.

A finding should not become a TP simply because its text sounds similar to a seeded weakness.

## 13. Core metrics

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

The dissertation must choose and document one denominator consistently. A practical rule-level experimental definition is:

```text
FPR = FP / (FP + TN)
```

If true negatives are not meaningfully enumerated for a particular analysis, report false positives and precision instead of inventing an FPR. The final methodology must explicitly define the unit of analysis (rule-operation test case, ground-truth case, or another defensible unit).

### Scan duration

Wall-clock runtime for the bounded profile, recorded with request count.

### Reproducibility/stability

Repeat key runs and measure whether the same ground-truth cases receive the same scanner classification.

Possible summary:

```text
stability = identical expected-case outcomes / repeated expected-case outcomes
```

The final formula/interpretation should be stated in the dissertation methodology.

### Cross-platform success rate

Measure successful execution/detection coverage across all three lab stacks without scanner target-language modifications.

## 14. Repetition plan

At minimum, key final evaluation profiles should be repeated multiple times per lab/mode to detect flaky behaviour.

The exact number of repeats should be fixed before final data collection. A practical starting point is 3–5 repeats per canonical configuration, subject to dissertation time constraints.

Do not selectively discard failed runs. Invalid runs must have a documented invalidation reason such as failed reset or infrastructure failure.

## 15. OWASP ZAP baseline

OWASP ZAP is the general-purpose baseline named in the proposal.

### Baseline principles

- use a documented pinned ZAP version/container where practical;
- use the same target lab mode;
- import/use OpenAPI where ZAP supports it;
- use a documented authentication setup when practical;
- avoid claiming ZAP should detect vulnerabilities outside its applicable automated baseline capabilities;
- preserve raw baseline output in research artefacts;
- normalize findings into the evaluation schema without rewriting their meaning.

### Comparison dimensions

For vulnerabilities meaningfully observable by both tools, compare:

- detection coverage;
- false positives;
- scan duration;
- evidence usefulness/reproducibility.

For identity-differential authorisation cases that ZAP cannot reliably model under the chosen baseline, record the limitation explicitly rather than counting unsupported capability as a conventional false negative without explanation.

## 16. Evaluation experiment structure

Suggested experiment matrix:

```text
3 labs
x 2 modes (vulnerable, corrected)
x N repeated runs
x scanner profile
+ corresponding applicable ZAP baseline runs
```

This gives both positive and negative cases and directly tests false-positive behaviour on corrected variants.

## 17. Evaluation scripts

Planned repository paths:

```text
evaluation/
  profiles/
  scripts/
  schemas/
  results/          # ignored or sample-only; do not commit secrets
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

Exact commands can use a `Makefile`, `justfile`, or Python task runner, but there should be one canonical task surface.

## 18. Research artefact preservation

Commit:

- evaluation schemas;
- scripts;
- ground-truth manifests;
- small synthetic sample outputs;
- analysis code/notebooks if used;
- final anonymised/redacted aggregate datasets suitable for dissertation reproduction.

Do not commit:

- secrets;
- live production target data;
- bearer tokens/cookies;
- uncontrolled raw dumps containing sensitive information.

## 19. Failure/validity controls

Threats to validity that engineering should actively reduce:

- scanner knows lab ground truth directly during normal detection — prohibited; ground truth is for evaluation harness, not rule decisions;
- different seeded behaviour across stacks accidentally changes difficulty — document and keep comparable categories while allowing stack-specific details;
- ZAP configuration unfairly weak/strong — pin and document settings;
- corrected mode changes unrelated endpoints — avoid through toggled behaviour and tests;
- data leakage between repeated runs — enforce reset;
- flaky timing/resource rule — use bounded deterministic profiles and repeat runs;
- manually relabelling ambiguous results after seeing scanner output — define matching/classification rules first.

## 20. Final evaluation acceptance gate

Final research data collection does not begin until:

1. all three labs have deterministic reset;
2. all ground-truth manifests are reviewed and versioned;
3. scanner profile is frozen/versioned;
4. evaluation matching logic is tested;
5. ZAP baseline configuration is pinned/documented;
6. corrected modes pass lab functional tests;
7. scanner verification suite passes;
8. evidence redaction tests pass;
9. repository commit used for evaluation is tagged or otherwise immutably recorded.
