# Data Model, Evidence and Reporting

## 1. Objective

The data layer must support reproducible scans and dissertation evaluation without storing secrets or uncontrolled raw traffic.

The canonical store is SQLite for local-first operation. SQLAlchemy migrations must be used from the first implementation phase.

## 2. Core entities

### Project

Conceptual fields:

- `id`;
- `name`;
- `description/notes`;
- `environment_class`;
- `authorisation_reference` metadata only;
- timestamps.

### Target

- `id`;
- `project_id`;
- scheme;
- hostname;
- port;
- base path;
- scope policy;
- redirect policy;
- general rate ceiling;
- total request budget;
- resource-test budget;
- timestamps.

### Specification

- `id`;
- `project_id`;
- format/type;
- original file name/source label;
- content hash;
- parser version;
- import warnings;
- normalized metadata;
- timestamps.

The original specification may be stored locally where safe, but embedded secrets must be rejected/redacted according to ingestion policy.

### InventoryOperation

- `id`;
- project/specification reference;
- method;
- path template;
- operation ID/tag;
- parameters/schema metadata;
- declared security metadata;
- source;
- enabled flag;
- reproducible manual annotations;
- inventory status.

### IdentityMetadata

- `id`;
- `project_id`;
- label;
- role;
- auth type;
- secret reference type/name;
- fixture metadata;
- active flag.

No token/password/API-key value is stored in this table.

### ScanProfile

- name/version;
- enabled rule IDs/categories;
- write policy;
- resource-test policy;
- request/rate budgets;
- deterministic safety parameters.

### Scan

- `id`;
- project/target IDs;
- state;
- scanner version/commit;
- rule catalogue version;
- specification hash;
- profile snapshot;
- target/scope snapshot;
- identity metadata snapshot without secrets;
- start/end timestamps;
- request counts;
- safety-stop reason;
- error summary;
- provenance metadata.

### RuleExecution

One record per rule-operation/fixture execution where appropriate:

- `id`;
- `scan_id`;
- rule ID/version;
- operation reference;
- identity labels;
- result state;
- confidence;
- request count;
- timing;
- reason/applicability metadata;
- evidence references.

### Evidence

- `id`;
- `scan_id`;
- `rule_execution_id`;
- type;
- redacted structured content;
- optional integrity/deduplication hash;
- capture timestamp;
- truncation indicator.

Evidence should be structured JSON first, not arbitrary text blobs only.

### Finding

- `id`;
- `scan_id`;
- stable finding fingerprint where practical;
- rule ID/version;
- status (`confirmed`, `suspected`, `informational`);
- severity;
- confidence;
- endpoint/method;
- title;
- explanation;
- expected behaviour;
- observed behaviour;
- remediation;
- OWASP mapping;
- CWE mapping;
- evidence references;
- timestamps.

### EvaluationRun

- run ID;
- scanner commit/version;
- rule catalogue version;
- lab ID/version/mode;
- fixture version;
- ground-truth hash;
- matcher version;
- scanner scan ID;
- optional ZAP run reference/applicability metadata;
- metrics;
- validity state/reason;
- timestamps.

### GroundTruthCase

Ground truth is authored as version-controlled YAML/JSON manifests in lab directories. The evaluation harness may ingest a snapshot after scanner output exists, but detector packages must not read/import these manifests.

## 3. Secret storage model

Initial supported secret sources:

- environment variables;
- ignored local `.env` file for development/labs;
- explicit local secret file with restrictive permissions where needed.

Do not build a custom secrets vault.

Database fields store only references such as:

```text
SECRET_SOURCE=env
SECRET_REF=LAB_CITIZEN_RECORDS_CITIZEN_A_TOKEN
```

Never echo resolved values into logs, evidence, exception messages or UI responses.

## 4. Redaction model

Redaction happens before persistence.

### Header redaction

At minimum replace values for:

- `Authorization`;
- `Proxy-Authorization`;
- `Cookie`;
- `Set-Cookie`;
- `X-API-Key` and configurable API-key header names.

### Body-field redaction

Case-insensitive configurable sensitive names should cover patterns for:

- password/passwd;
- token/access_token/refresh_token/id_token;
- api_key/apikey;
- secret/client_secret;
- session/session_id;
- authorization.

### Runtime secret-value redaction

Where feasible, the redactor should also remove exact values known to the runtime secret registry even if they appear under an unexpected field name.

### Redaction marker

Use a consistent marker such as:

```text
[REDACTED]
```

Do not store hashes of credentials as substitutes.

## 5. Evidence minimisation

Persist the minimum material required to support the conclusion.

### BOLA evidence example

Prefer:

```json
{
  "request": {
    "method": "GET",
    "path": "/api/v1/citizens/<citizen-b>",
    "identity": "citizen-a"
  },
  "comparison": {
    "owner_baseline_identity": "citizen-b",
    "cross_user_status": 200,
    "stable_fields_matching": ["citizen_id", "record_fixture"]
  },
  "response_excerpt": {
    "citizen_id": "citizen-b",
    "record_fixture": "citizen-profile-b"
  }
}
```

rather than the complete synthetic citizen response.

### Error-leak evidence

Persist only the small redacted lines/fields proving a stack trace, framework path or database error, not the complete response where unnecessary.

## 6. Evidence size controls

The HTTP executor/evidence builder must enforce:

- maximum response body capture size;
- maximum persisted excerpt size;
- per-scan persisted-size bound or defensible derivation;
- truncation flag;
- binary response exclusion unless a rule specifically needs metadata only.

The scanner is not a traffic archive.

## 7. Finding fingerprinting

A stable fingerprint can support repeated-run comparison.

Recommended input dimensions:

```text
rule_id + method + normalized_path + relevant fixture/property identifier
```

Do not include secrets, raw protected values or timestamps.

## 8. Severity model

Initial scale:

```text
critical | high | medium | low | info
```

Severity assignment should be rule-default plus bounded context adjustments, not a complex CVSS implementation unless later academic requirements demand it.

Examples:

- proven cross-user access to a protected synthetic citizen/health/permit record: typically high;
- low-privilege privileged mutation: high/critical depending on controlled scenario impact;
- verbose framework stack trace: medium/low depending on exposed content;
- documentation exposure: informational/low unless non-public operations/details are exposed.

Document automatic adjustments.

## 9. Confidence model

Suggested ordinal values:

- `high` — direct rule proof with stable semantic confirmation;
- `medium` — strong differential evidence with one missing semantic confirmation;
- `low` — heuristic/informational observation.

`confirmed` findings normally require high or explicitly justified medium confidence. Confidence must not be inferred purely from HTTP status.

## 10. Canonical JSON report

JSON is the authoritative export format for evaluation and reproducibility.

Conceptual schema:

```json
{
  "schema_version": "1",
  "scanner": {},
  "project": {},
  "scope": {},
  "scan": {},
  "summary": {},
  "findings": [],
  "rule_executions": [],
  "inconclusive": [],
  "statistics": {},
  "provenance": {}
}
```

Commit and test a JSON Schema.

## 11. CSV outputs

CSV is intended for analysis, not full raw evidence.

Recommended tables:

- `findings.csv`;
- `rule_executions.csv`;
- `evaluation_runs.csv`;
- `evaluation_matches.csv`.

Neutralise spreadsheet formula execution in target-controlled fields. Do not flatten secret-bearing raw traffic into CSV.

## 12. HTML report

Required structure:

1. project/scan metadata;
2. scope and safety profile;
3. executive summary;
4. findings summary;
5. detailed findings and redacted evidence;
6. OWASP mapping;
7. limitations/inconclusive/error states;
8. request/scan statistics;
9. reproducibility/provenance metadata.

All target-controlled text is escaped. Reports never embed active target HTML/script/SVG/template content.

## 13. OWASP mapping presentation

Reports must state that the scanner covers a **selected subset** of OWASP API Security Top 10 2023 categories. An unimplemented category is `not covered`, never `secure`.

## 14. Reproduction instructions

For each confirmed finding, include safe reproduction guidance referencing:

- controlled identity label;
- method/path;
- fixture/object label;
- minimal request variation;
- observed outcome;
- safety note where writes are involved.

Do not export live credentials.

## 15. Evaluation reporting

Evaluation outputs must include:

- predeclared case ID;
- matcher version;
- expected rule/operation/fixture dimensions;
- scanner result state;
- TP/FP/FN/TN classification where defensible;
- ZAP applicability state and normalized result where relevant;
- validity state/reason;
- all provenance fields required by `docs/04-LABS-AND-EVALUATION.md`.

Unexpected findings outside headline case tuples remain visible rather than being discarded.

## 16. Auditability

A reviewer should be able to answer:

- which rule generated this finding?
- which rule version?
- which target/spec/profile was used?
- what evidence proved it?
- was evidence redacted before storage?
- how many requests did the rule use?
- could the finding be reproduced against the same lab state?
- which frozen ground-truth case did evaluation match it to, if any?
- which scanner/lab/matcher versions produced the metric?

If the data model cannot answer these questions, it is incomplete.
