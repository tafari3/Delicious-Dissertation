# Data Model, Evidence and Reporting

## 1. Objective

The data layer must support reproducible scans and dissertation evaluation without storing secrets or uncontrolled raw traffic.

The canonical store is SQLite for local-first operation. SQLAlchemy migrations must be used from the first implementation phase.

## 2. Core entities

### Project

Fields conceptually include:

- `id`;
- `name`;
- `description/notes`;
- `environment_class`;
- `authorisation_reference` (metadata only);
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

The original spec may be stored locally where safe, but secrets embedded in source documents must be rejected/redacted according to ingestion policy.

### InventoryOperation

- `id`;
- `project/specification_id`;
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
- other deterministic safety parameters.

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
- hash if useful for integrity/deduplication;
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
- lab ID/version/mode;
- ground-truth hash;
- scanner scan ID;
- optional ZAP run reference;
- metrics;
- validity state/reason;
- timestamps.

### GroundTruthCase

Prefer ground truth as version-controlled YAML/JSON manifests in lab directories. The evaluation harness may ingest a snapshot into the database, but the authoritative source remains the version-controlled manifest.

## 3. Secret storage model

Supported initial secret sources should stay simple:

- environment variables;
- ignored local `.env` file for development/labs;
- explicit local secret file with restrictive permissions where needed.

Do not build a custom secrets vault.

Database fields should store only a reference such as:

```text
SECRET_SOURCE=env
SECRET_REF=MOBILE_MONEY_USER_A_TOKEN
```

Never echo the resolved value into logs, evidence, exception messages or UI responses.

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

Case-insensitive configurable sensitive names should include patterns for:

- password/passwd;
- token/access_token/refresh_token/id_token;
- api_key/apikey;
- secret/client_secret;
- session/session_id;
- authorization.

### Token-like value redaction

Where feasible, the redactor should also detect values known to the runtime secret registry and replace occurrences even if they appear under an unexpected key.

### Redaction marker

Use a consistent marker such as:

```text
[REDACTED]
```

Do not include hashes of credentials as an alternative because stable hashes can still create unnecessary sensitive correlation material.

## 5. Evidence minimisation

Persist the minimum material needed to prove the condition.

Examples:

### BOLA evidence

Prefer:

```json
{
  "request": {
    "method": "GET",
    "path": "/wallets/<object-b>",
    "identity": "customer-a"
  },
  "comparison": {
    "owner_baseline_identity": "customer-b",
    "cross_user_status": 200,
    "stable_fields_matching": ["wallet_id", "owner_fixture"]
  },
  "response_excerpt": {
    "wallet_id": "wallet-b",
    "owner_fixture": "customer-b"
  }
}
```

rather than the full wallet response.

### Error-leak evidence

Persist only the small redacted lines/fields proving a stack trace or database error, not the full server response if unnecessary.

## 6. Evidence size controls

The HTTP executor/evidence builder must enforce:

- maximum response body capture size;
- maximum persisted excerpt size;
- truncation flag;
- binary response exclusion unless a rule specifically needs metadata only.

The scanner is not a traffic archive.

## 7. Finding fingerprinting

A stable fingerprint can help repeated-run comparison.

Recommended input dimensions:

```text
rule_id + method + normalized_path + relevant fixture/property identifier
```

Do not include secrets, raw response values or timestamps.

Fingerprints are for matching/deduplication and evaluation; they must not hide distinct affected operations.

## 8. Severity model

Initial qualitative scale:

- `critical`;
- `high`;
- `medium`;
- `low`;
- `info`.

Severity assignment should be rule-default + bounded context adjustments, not a complex CVSS implementation unless dissertation requirements later demand it.

Examples:

- proven cross-user access to sensitive financial/personal object: typically high;
- low-privilege privileged mutation: high/critical depending on controlled scenario impact;
- verbose framework stack trace: medium/low depending on exposed content;
- documentation exposure: informational/low unless sensitive non-public operations/details are exposed.

Document every automatic adjustment.

## 9. Confidence model

Suggested ordinal values:

- `high` — direct rule proof condition with stable semantic confirmation;
- `medium` — strong differential evidence with one missing semantic confirmation;
- `low` — heuristic/informational observation.

`confirmed` findings should normally require high or explicitly justified medium confidence. Confidence must not be inferred purely from HTTP status.

## 10. Canonical JSON report

JSON is the authoritative export format because evaluation and reproducibility depend on machine-readable output.

Top-level conceptual schema:

```json
{
  "schema_version": "1",
  "scanner": {},
  "project": {},
  "scope": {},
  "scan": {},
  "summary": {},
  "findings": [],
  "inconclusive": [],
  "statistics": {},
  "provenance": {}
}
```

A JSON Schema should be committed and used in tests.

## 11. CSV outputs

CSV is intended for analysis, not full evidence.

Recommended tables:

- `findings.csv`;
- `rule_executions.csv`;
- `evaluation_runs.csv`;
- `evaluation_matches.csv`.

Do not flatten secret-bearing raw traffic into CSV.

## 12. HTML report

The human-readable report should contain:

### Cover/metadata

- project;
- target label;
- scan ID/time;
- scanner version;
- profile;
- scope summary.

### Executive summary

- counts by finding state and severity;
- concise statement of scope and limitations;
- safety profile/request counts.

### Findings

For each finding:

- title;
- status/severity/confidence;
- endpoint;
- OWASP/CWE mapping;
- expected vs observed behaviour;
- minimal redacted evidence;
- remediation;
- reproduction notes.

### Limitations and inconclusive results

This section is mandatory. A report that hides tests that could not be concluded is academically weaker and operationally misleading.

### Provenance

- scanner commit;
- rule catalogue version;
- spec hash;
- target/lab version if available;
- scan profile;
- timing/request stats.

## 13. OWASP mapping presentation

Reports must state that the scanner covers a **selected subset** of OWASP API Security Top 10 2023 categories. It must not render an unimplemented category as “secure”.

Recommended mapping table fields:

- OWASP category;
- rules executed;
- confirmed findings;
- suspected/informational findings;
- not tested/not in scope note.

## 14. Reproduction instructions

For each confirmed finding, include safe reproduction guidance that references:

- controlled identity label;
- method/path;
- fixture/object label;
- minimal expected request variation;
- observed outcome;
- safety note where writes are involved.

Do not export live credentials in reproduction commands.

## 15. Auditability

A reviewer should be able to answer:

- which rule generated this finding?
- which rule version?
- which target/spec/profile was used?
- what evidence proved it?
- was evidence redacted before storage?
- how many requests did the rule use?
- could the finding be reproduced against the same lab state?

If the data model cannot answer these questions, it is incomplete.
