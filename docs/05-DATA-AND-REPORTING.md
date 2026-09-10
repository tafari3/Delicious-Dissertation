# Data Model, Evidence and Automatic Reporting

## 1. Objective

Support reproducible scans and dissertation evaluation without storing secrets or uncontrolled raw traffic. SQLite is the default local store.

## 2. Core entities

`Project`, `Target`, `Specification`, `InventoryOperation`, `IdentityMetadata`, `ScanProfile`, `Scan`, `RuleExecution`, `Evidence`, `Finding`, `EvaluationRun`.

A completed `Scan` preserves scanner commit/version, rule catalogue version, target/scope/profile snapshot, spec hash where present, non-secret identity metadata, timestamps, request counts and outcome.

## 3. Secret model

Secrets come from runtime environment or bounded local secret files. Database/config metadata stores references, never credential values. Never commit signed authorisation documents, real ZCHPC credentials or sensitive operational dumps.

## 4. Evidence model

Evidence is structured JSON first. Persist only the minimum material needed for proof. Redact before persistence/export:

- Authorization / Proxy-Authorization;
- Cookie / Set-Cookie;
- API keys;
- password/token/secret/session fields;
- exact runtime-known secret values;
- locally configured sensitive fields.

Apply response-capture, excerpt and per-scan persistence limits. Record truncation explicitly.

## 5. Finding model

A finding contains:

- rule ID/version;
- state;
- severity and confidence;
- endpoint/service and method where applicable;
- title/explanation;
- expected behaviour;
- observed behaviour;
- minimal redacted evidence;
- OWASP/CWE mapping where appropriate;
- remediation guidance;
- safe reproduction note;
- timestamps/provenance.

## 6. Automatic report contract

Automatic report generation is a required scanner capability after a scan becomes reportable.

### HTML

Human-readable report with executive summary, scope/safety profile, findings summary/detail, redacted evidence, severity/confidence, OWASP/CWE, remediation, limitations/inconclusive/error outcomes, request/timing statistics and provenance.

### PDF

Required human-readable export generated from the canonical report model/HTML without introducing active target-controlled content. PDF generation failure is explicit; it must not silently produce a partial report.

### JSON

Canonical machine-readable report with committed schema.

### CSV

Research/tabular exports for findings, rule executions and evaluation records. Neutralise spreadsheet formula injection in target-controlled cells.

## 7. Output security

- escape target-controlled HTML/template content;
- neutralise CSV formula prefixes;
- sanitise terminal control sequences;
- generate filesystem paths from controlled IDs/sanitised slugs;
- never export secrets;
- operational ZCHPC reports must support a restricted/confidential handling mode so public research artefacts do not disclose protected infrastructure details.

## 8. Evaluation records

Controlled lab `EvaluationRun` stores lab/version/mode/fixture version, ground-truth hash, matcher version, scanner scan ID, ZAP applicability/result, metrics and validity reason.

ZCHPC validation records use a separate environment class and do not pretend to contain complete ground truth. They record target-profile version, non-secret authorisation reference, applicability, repeatability, evidence quality, findings and operational constraints.

## 9. Auditability

A reviewer must be able to identify which rule/version produced a finding, against which target/spec/profile, what redacted evidence supported it, how many requests were used, what report version was generated, and—only for controlled lab evaluation—which frozen ground-truth case the evaluation matched.
