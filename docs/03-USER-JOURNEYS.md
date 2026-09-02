# User Journeys and Interaction Design

## 1. Product interaction principle

The scanner is a local research/security tool. The interface should make safe configuration obvious and prevent a user from casually starting an uncontrolled scan.

The primary interaction sequence is:

```text
Create Project
  -> Register Authorised Target
  -> Import API Description
  -> Review Inventory
  -> Configure Controlled Identities
  -> Choose Scan Profile
  -> Safety Preflight
  -> Review Execution Plan
  -> Run Scan
  -> Review Findings/Evidence
  -> Export Report
```

The CLI must support the same conceptual flow for reproducible experiments.

## 2. Personas

### 2.1 Student researcher / scanner operator

Primary user during development and dissertation evaluation.

Needs to:

- configure lab targets;
- run deterministic scans;
- inspect why findings were created;
- repeat experiments;
- export evaluation data;
- compare scanner and ZAP outcomes.

### 2.2 Developer/remediator

Secondary report consumer.

Needs to:

- understand which endpoint is affected;
- see concise redacted evidence;
- understand expected vs observed behaviour;
- see OWASP/CWE mapping;
- reproduce the condition safely;
- understand remediation direction.

### 2.3 Supervisor/examiner/auditor

Secondary review persona.

Needs to:

- understand scanner scope and limitations;
- verify methodology;
- see ground truth independent of scanner output;
- reproduce experiments;
- inspect metrics and evidence provenance.

## 3. Journey J1 — First-time local setup

### Goal

Bring the repository up on a clean machine/VM and verify that the artefact and labs are reproducible.

### Flow

1. Clone repository.
2. Run documented environment/bootstrap command.
3. Run project verification command.
4. Start local application.
5. Start laboratories.
6. Open dashboard/CLI health status.
7. Confirm scanner version, database status and lab reachability.

### Acceptance

A clean documented environment can reach a ready state without manually editing source code or seeding database rows by hand.

## 4. Journey J2 — Create a scan project

### Goal

Create a durable container for target, specification, identities, scans and reports.

### Dashboard fields

- project name;
- optional research label/notes;
- target environment classification;
- optional authorisation-reference metadata.

### Guardrails

- no credentials entered into project notes;
- no scan starts from project creation;
- project remains `DRAFT` until target and preflight requirements are satisfied.

## 5. Journey J3 — Register and authorise target

### Goal

Explicitly define exactly what host/base path may be scanned.

### Required configuration

- scheme;
- hostname/IP;
- port when non-default;
- optional base path;
- environment classification;
- allowed redirect policy;
- request-rate ceiling;
- total request budget;
- resource-test budget;
- written-authorisation reference metadata for non-lab targets where applicable.

### UI behaviour

The interface displays the **effective allowed scope** in a compact, human-readable form before saving.

Example conceptual display:

```text
Allowed target:
https://localhost:8101/api/*

Redirects:
same host + scheme only

General ceiling:
5 req/s, 500 total

Resource-control ceiling:
2 req/s, 20 requests
```

Numbers above are examples only; production defaults must be defined and tested in implementation.

### Blocking states

- malformed target;
- wildcard scope broader than supported safety policy;
- missing ceilings;
- redirect configuration that can escape target;
- unsupported scheme.

## 6. Journey J4 — Import OpenAPI/Postman description

### Goal

Build a specification-assisted operation inventory.

### Flow

1. Choose OpenAPI or Postman import.
2. Upload/select local file or configured authorised URL if supported.
3. Parse without executing embedded scripts.
4. Show import summary:
   - format/version;
   - number of paths/operations;
   - authentication schemes detected;
   - warnings/unsupported constructs;
   - hash/provenance.
5. User accepts import into project.

### Important behaviour

A successful parse does not mean the specification is assumed correct. The UI should state that it is a **testing aid**, not ground truth.

## 7. Journey J5 — Review endpoint inventory

### Goal

Allow the operator to see exactly what the scanner thinks it can test.

### Inventory table

Recommended fields:

- method;
- path;
- operation ID/tag;
- documented source;
- declared authentication;
- candidate object-ID parameters;
- candidate write properties;
- enabled/disabled for scan;
- warnings.

### Operator controls

The operator may:

- exclude operations from the project scan plan;
- label operations as public/protected where explicit test metadata is needed;
- associate lab fixture metadata;
- identify privileged operations for deterministic BFLA evaluation.

Manual annotations must be recorded as project/test metadata so they are reproducible.

## 8. Journey J6 — Configure controlled identities

### Goal

Provide isolated test contexts for differential authorisation checks.

### Identity metadata

- friendly label (`user-a`, `user-b`, `officer`, `admin`);
- role label;
- authentication type;
- secret source/reference;
- optional owned-object fixture references for lab evaluation.

### Secret handling

The dashboard must not display stored bearer tokens after entry. Prefer environment/secret-file injection for automated evaluation.

Persist metadata such as `identity_label=user-a`; do not persist token values into evidence.

### Validation

Optional identity-validation request may confirm the credential works against a configured benign endpoint. The validation request must use the normal HTTP safety executor.

## 9. Journey J7 — Select scan profile

### Minimum profiles

#### Safe Read-Only

Default profile.

Includes:

- read-based authorisation rules;
- authentication observations;
- configuration checks;
- inventory checks;
- no write mutation tests;
- resource-control tests off unless separately enabled.

#### Controlled Lab Full

For the project's disposable local laboratories.

Includes:

- Safe Read-Only rules;
- disposable BOLA mutation tests;
- mass-assignment tests;
- bounded rate/resource observations;
- deterministic reset/cleanup.

#### Custom

Explicit selection of rule groups while still enforcing global safety invariants.

No UI mode may disable target allow-listing, redaction or hard request ceilings.

## 10. Journey J8 — Safety preflight

### Goal

Block unsafe or incomplete scans before any test catalogue execution.

### Preflight checklist displayed to operator

- target is allow-listed;
- DNS/connection target remains in scope;
- HTTPS/TLS status observed where applicable;
- specification parsed or absence acknowledged;
- selected operations count;
- identity prerequisites satisfied;
- selected rules count;
- write tests enabled/disabled;
- disposable fixtures available for write tests;
- general request budget;
- resource-test request budget;
- redaction configured;
- database/evidence store healthy.

### Result

`READY` only when all mandatory checks pass.

If blocked, UI must show actionable reasons; it must not provide a bypass button for hard invariants.

## 11. Journey J9 — Review execution plan

Before starting, show:

- target;
- scanner/rule version;
- operations selected;
- rule groups;
- identity pairings;
- maximum request budget;
- whether writes are possible;
- whether resource-control testing is enabled;
- estimated test count when calculable.

The plan can be exported/recorded as part of scan provenance.

## 12. Journey J10 — Execute scan

### Runtime view

Display:

- scan state;
- elapsed time;
- current rule/operation in non-sensitive terms;
- completed/planned rule executions;
- request count / maximum budget;
- finding count by state/severity;
- stop button;
- safety-stop reason if triggered.

Do not stream raw bearer tokens or full sensitive request bodies into the browser console/log view.

### Cancellation

Stopping a scan must:

- signal cooperative cancellation;
- prevent new test requests;
- perform registered disposable-lab cleanup where safe;
- mark scan `STOPPED`;
- retain already-redacted evidence/provenance.

## 13. Journey J11 — Review findings

### Findings list filters

- status: confirmed/suspected/informational;
- severity;
- OWASP category;
- rule ID;
- endpoint/method;
- scan ID.

### Finding detail view

Must show:

1. title;
2. status/severity/confidence;
3. endpoint and method;
4. rule ID/version;
5. why the rule ran;
6. expected secure behaviour;
7. observed behaviour;
8. minimal redacted evidence;
9. identity/role labels without credentials;
10. OWASP/CWE mapping;
11. remediation note;
12. reproduction guidance;
13. provenance/timestamp.

### Important wording rule

The UI must not represent `suspected` or `inconclusive` observations as confirmed vulnerabilities.

## 14. Journey J12 — Export report

### Minimum export formats

- JSON — canonical machine-readable output;
- CSV — evaluation/tabular finding data;
- HTML — human-readable report.

PDF is optional if it can be generated reliably from the HTML report without adding disproportionate complexity.

### Report structure

1. project/scan metadata;
2. scope and safety profile;
3. executive summary;
4. findings summary;
5. detailed findings and redacted evidence;
6. OWASP mapping;
7. limitations/inconclusive tests;
8. request/scan statistics;
9. reproducibility/provenance metadata.

## 15. Journey J13 — Laboratory evaluation run

### Goal

Run a deterministic research experiment against known ground truth.

### Flow

1. Start/reset selected lab.
2. Verify lab health and ground-truth manifest version.
3. Load lab project fixture.
4. Run scanner under named evaluation profile.
5. Store canonical scanner result.
6. Run OWASP ZAP baseline under documented baseline configuration where applicable.
7. Normalize baseline results into evaluation schema.
8. Compare both against independently defined ground truth.
9. Calculate metrics.
10. Repeat configured runs.
11. Export evaluation dataset and summary.

This journey must be executable through CLI/scripts without clicking through the dashboard.

## 16. Journey J14 — Demonstration mode

A dissertation demonstration should be possible using one command or a short documented sequence that:

- resets the three labs;
- starts required services;
- runs a representative scanner profile;
- produces findings;
- opens or points to the local dashboard/report;
- leaves the environment in a reproducible state.

Do not hard-code a fake demonstration result. The demo must execute the actual scanner.

## 17. Error journeys

### Target leaves scope

- immediately block request;
- safety-stop scan if during execution;
- record non-secret reason;
- do not follow redirect.

### Identity invalid

- mark dependent rules not applicable/inconclusive;
- do not repeatedly retry authentication indefinitely;
- show which identity label failed without exposing credential.

### Specification parse failure

- show parse errors;
- retain original hash/name metadata where safe;
- allow correction/re-import;
- do not silently continue as though import succeeded.

### Target unstable/unavailable

- bounded retry for idempotent request only;
- stop/mark incomplete once tolerance is exceeded;
- do not treat service errors as vulnerability proof.

### Cleanup failure after lab write test

- stop further mutation rules against that fixture;
- flag cleanup failure;
- require lab reset before next controlled write sequence.
