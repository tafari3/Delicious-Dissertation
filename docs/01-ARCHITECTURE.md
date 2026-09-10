# Scanner Architecture

## 1. Objective

Build the smallest auditable architecture that supports safe, reproducible API security testing, automatic reporting, controlled laboratory evaluation and later authorised ZCHPC validation.

## 2. Technology defaults

Scanner/runtime:

- Python 3.12+
- `httpx` controlled HTTP execution
- Pydantic typed configuration/models
- SQLAlchemy 2.x + SQLite
- FastAPI local application surface
- Typer CLI
- lightweight server-rendered dashboard
- pytest + Ruff + type checking

Controlled lab:

- `government-permit-service-fastapi`
- Python/FastAPI
- small relational database
- Docker/Compose where permitted on the provided Linux VM

## 3. Component model

```text
CLI / Local Dashboard
        |
Project + Target + Authorisation Metadata
        |
Safety / Scope Preflight
        |
Spec + Endpoint Inventory
        |
Deterministic Scan Planner
        |
Identity/Session Manager + Rule Modules
        |
Controlled HTTP Executor
        |
Authorised Target
        |
Evidence Extraction -> Redaction -> Classification -> SQLite
        |
Automatic Report Engine
        +--> HTML
        +--> PDF
        +--> JSON
        +--> CSV
```

Evaluation layer:

```text
Synthetic Lab + Direct Contract Tests -> Frozen Ground Truth
Scanner -> Findings
Evaluation Harness -> deterministic matching/metrics
OWASP ZAP -> applicability-aware comparison
```

P10 adds a separate `authorised-zchpc` target profile. It uses the same scanner architecture but a more restrictive non-destructive policy and no lab ground truth.

## 4. Core domains

**Project** — durable container for target, scope, spec, identities, scan profiles, scans/findings and authorisation-reference metadata.

**Target** — scheme/host/port/base path, environment class (`lab` or `authorised-zchpc`), approved address policy, budgets and non-secret authorisation reference.

**Identity** — anonymous and controlled named roles; credentials are runtime secrets only.

**InventoryOperation** — method/path/parameters/schema/security/source/documented status and reproducible annotations.

**Rule** — stable ID/version, applicability, request plan, proof/inconclusive conditions, evidence schema, stop conditions, OWASP/CWE and remediation.

**Scan** — immutable completed snapshot of scanner commit, target/scope/profile/spec/rule versions, non-secret identity metadata, timing, counts and outcomes.

## 5. Controlled HTTP executor

All target traffic goes through one executor enforcing:

- allow-list and destination validation;
- redirect revalidation;
- timeouts;
- rate/concurrency/total request ceilings;
- per-rule and resource sub-budgets;
- response capture limits;
- safe retry policy;
- cancellation;
- correlation/provenance;
- ambient proxy environment ignored by default.

No rule may create an unrestricted target-facing HTTP client.

## 6. Identity and differential testing

Sessions/cookie jars are isolated per identity. The lab provides `applicant-a`, `applicant-b`, `officer` and `admin` fixtures so BOLA/BFLA/BOPLA and authentication rules can use deterministic relationships.

## 7. Evidence and reporting

Raw material may exist transiently in memory. Persistence occurs only after rule-specific extraction, secret redaction and size minimisation.

Automatic reports are not optional. HTML/PDF are the human-readable artefacts; JSON is canonical machine-readable output; CSV supports research analysis.

## 8. Controlled laboratory deployment

The synthetic permit/service API and scanner may run on the same ZCHPC-provided Linux VM using loopback/isolated container networking. Separate VMs are not a dissertation requirement.

The lab is intentionally small and contains no real government data or dependency on production services.

## 9. Authorised ZCHPC validation architecture

After P9 passes, P10 configures the actual authorised ZCHPC target separately from the lab. Exact hosts/assets and credentials remain local/runtime configuration and are not committed.

The same preflight/executor/redaction/reporting path is mandatory. Operational scans default to read-only/non-destructive checks. Any state-changing operational action requires explicit correspondence with the signed scope and a separately reviewed test step.

## 10. Invariants

1. scanner detection never reads ground truth;
2. operational ZCHPC validation never uses deliberately seeded production weaknesses;
3. lab and ZCHPC results remain separate datasets;
4. report generation uses the same durable finding model for both;
5. confidential operational details are excluded from public/repository artefacts.
