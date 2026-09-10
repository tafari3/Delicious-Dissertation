# User Journeys and Interaction Design

## 1. Primary flow

```text
Create Project
-> Register Authorised Target
-> Import API Description
-> Review Inventory
-> Configure Controlled Identities
-> Choose Scan Profile
-> Safety Preflight
-> Review Plan
-> Run Scan
-> Review Findings
-> Generate / Export Report
```

The CLI must support the same research workflow non-interactively.

## 2. Personas

- **Student researcher/operator** — configures lab and authorised ZCHPC targets, runs scans/evaluations, reviews evidence and exports reports.
- **Developer/remediator** — consumes findings, evidence and remediation guidance.
- **Supervisor/examiner/auditor** — verifies methodology, ground-truth independence, metrics, provenance and reproducibility.

## 3. Target registration

Required fields include scheme/host/port/base path, environment class, address policy, redirect policy, hard budgets and non-secret authorisation-reference metadata for non-lab targets.

The UI shows the effective scope before execution. Hard failures have no bypass button.

## 4. Identity setup

The lab uses `applicant-a`, `applicant-b`, `officer`, `admin`. ZCHPC operational validation uses only identities explicitly approved for the signed scope. Credentials are runtime secrets and are never rendered back after resolution.

## 5. Scan profiles

- `safe-read-only` — default; no intentional state mutation.
- `controlled-lab-full` — only for the synthetic disposable lab; permits narrowly defined mutation cases and deterministic cleanup/reset.
- `authorised-zchpc` — P10 only; non-destructive by default, stricter budgets, exact signed-scope matching, no seeded-production assumptions.

No profile can disable hard scope/redaction/budget invariants.

## 6. Preflight

Display and verify target scope, destination/address policy, specification status, selected rules, identity prerequisites, write/resource controls, request budgets, redaction and evidence-store health. Operational ZCHPC preflight additionally requires the local authorisation reference and explicit operational profile.

## 7. Scan runtime

Show scan state, elapsed time, current rule/operation in non-sensitive terms, request count versus maximum, finding counts, stop control and safety-stop reason. Never stream secrets/raw sensitive bodies.

## 8. Findings review

Finding detail shows state, severity, confidence, endpoint/method, rule/version, expected versus observed behaviour, minimal redacted evidence, identity labels, OWASP/CWE, remediation, safe reproduction guidance and provenance.

Do not present suspected/inconclusive results as confirmed vulnerabilities.

## 9. Automatic report generation

After a completed/reportable scan the operator can generate/export:

- HTML;
- PDF;
- JSON;
- CSV.

HTML/PDF include executive summary, scope/safety profile, findings, redacted evidence, severity/confidence, OWASP/CWE, remediation, limitations/inconclusive/error states, scan/request statistics and provenance.

## 10. Controlled laboratory evaluation journey

1. reset `government-permit-service-fastapi`;
2. verify lab version/mode/fixture version;
3. run scanner without ground-truth access;
4. store canonical findings/report;
5. run applicable pinned ZAP baseline;
6. evaluation harness reads frozen ground truth after scanner output exists;
7. compute deterministic metrics;
8. repeat frozen profiles;
9. export evaluation dataset.

## 11. ZCHPC validation journey

P10 only, after P9 gate:

1. load local authorised-ZCHPC target profile;
2. verify authorisation reference and exact configured scope;
3. run preflight with stricter non-destructive limits;
4. execute only applicable approved rules;
5. stop on any scope/instability/confidentiality concern;
6. generate redacted operational report;
7. analyse applicability/repeatability/evidence quality separately from lab accuracy.

## 12. Demonstration

The dissertation demo must execute the actual scanner against the controlled lab, generate a real report, and leave the lab resettable. It must not use hard-coded fake results. ZCHPC operational data is not required to be shown publicly in the demo.
