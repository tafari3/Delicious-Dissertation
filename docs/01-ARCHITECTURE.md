# Scanner and Evaluation Architecture

## 1. Objective

Build the smallest auditable architecture that supports safe, reproducible API security testing, automatic reporting, controlled XCP-ng/Xen Orchestra cloud evaluation and later authorised ZCHPC validation.

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

Synthetic application lab:

- `government-permit-service-fastapi`
- Python/FastAPI
- small relational database
- Docker/Compose where useful

Controlled cloud:

- XCP-ng as the hypervisor;
- Xen Orchestra as management/orchestration;
- Linux VMs for scanner and synthetic target;
- database/supporting service on a separate VM where resources permit;
- management and service/test networks separated wherever the available lab infrastructure permits.

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
XCP-ng controlled cloud
        |
Xen Orchestra management
        |
+-------------------+------------------------+
|                                            |
Scanner VM                            Synthetic E-Gov API VM
                                             |
                                      Database/support service

Direct application/configuration proof -> Frozen Ground Truth
Scanner                              -> Findings
Evaluation Harness                   -> deterministic matching/metrics
OWASP ZAP                            -> applicability-aware comparison
```

The diagram is logical, not a claim that Xen Orchestra is the hypervisor or that the database must always occupy a dedicated VM. Resource-constrained deployments may consolidate supporting services if the change is documented and does not invalidate a controlled case.

P10 adds a separate `authorised-zchpc` target profile. It uses the same scanner architecture but a more restrictive non-destructive policy and no assumption of complete operational ground truth.

## 4. Core domains

**Project** — durable container for target, scope, spec, identities, scan profiles, scans/findings and authorisation-reference metadata.

**Target** — scheme/host/port/base path, environment class (`controlled-cloud` or `authorised-zchpc`), approved address policy, budgets and non-secret authorisation reference.

**Identity** — anonymous and controlled named roles; credentials are runtime secrets only.

**InventoryOperation** — method/path/parameters/schema/security/source/documented status and reproducible annotations.

**Rule** — stable ID/version, applicability, request plan, proof/inconclusive conditions, evidence schema, stop conditions, OWASP/CWE and remediation.

**ControlledCloudCase** — stable case ID, expected secure/insecure state, affected logical asset/network/operation, direct proof procedure and scanner mapping where applicable.

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

## 8. Controlled replica-cloud deployment

Stage 1 is not a single standalone Linux-VM experiment. The synthetic application is deployed inside a small XCP-ng/Xen Orchestra research cloud created for the dissertation.

Minimum logical separation:

```text
Management plane/network
  - XCP-ng management
  - Xen Orchestra

Service/test network
  - Scanner VM
  - Synthetic e-government API VM
  - Database/support service where separately provisioned
```

The exact addressing, VLANs, storage repositories and host capacity are environment-specific and must be recorded from the actual lab rather than invented in source control.

The replica cloud may deliberately contain bounded, reversible configuration weaknesses with independent expected secure states. Examples include wrong network reachability, exposed services, service binding, TLS/certificate configuration and lab-only permission/segmentation cases. Scanner evaluation stops at proof-of-condition; no destructive hypervisor testing is introduced.

## 9. Independent ground truth

Application ground truth is established by direct functional tests. Deployment/cloud ground truth is established by direct configuration/reachability checks defined before final scanner data collection.

Scanner detector code cannot read controlled ground-truth manifests. The evaluation harness receives scanner output only after a scan completes and performs deterministic matching against frozen case identifiers/dimensions.

## 10. Authorised ZCHPC validation architecture

After P9 passes, P10 configures the actual authorised ZCHPC target separately from the controlled replica. Exact hosts/assets and credentials remain local/runtime configuration and are not committed.

The same preflight/executor/redaction/reporting path is mandatory. Operational scans default to read-only/non-destructive checks. Any state-changing operational action requires explicit correspondence with the signed scope and a separately reviewed test step.

## 11. Invariants

1. scanner detection never reads ground truth;
2. XCP-ng is the hypervisor; Xen Orchestra is management/orchestration;
3. operational ZCHPC validation never uses deliberately seeded production weaknesses;
4. controlled-cloud and ZCHPC results remain separate datasets;
5. report generation uses the same durable finding model for both;
6. confidential operational details are excluded from public/repository artefacts;
7. cloud/deployment cases remain bounded and do not turn the dissertation into unrestricted infrastructure penetration testing.
