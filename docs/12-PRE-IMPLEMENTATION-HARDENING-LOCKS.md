# Pre-Implementation Hardening Locks

## 1. Purpose

This document records design decisions that became necessary after the red-team review in `11-RED-TEAM-ATTACK-MATRIX.md`. These are not optional implementation suggestions. They are locked safety, robustness and research-integrity requirements unless changed in a reviewed PR that explains why an equivalent or stronger control is used.

The goal is to remove ambiguity before AntiGravity implements P1 onward.

## 2. Network and scope locks

### 2.1 Canonical URL policy

The implementation must have one canonical URL/scope-normalisation module used by preflight, the HTTP executor, redirects and remote specification imports.

It must:

- accept only `http` and `https` for network targets;
- reject URL userinfo;
- canonicalise DNS names case-insensitively and account for trailing-dot/punycode representation consistently;
- canonicalise IPv4/IPv6 using a standard IP-address parser;
- reject ambiguous/non-standard numeric IP representations rather than attempting permissive interpretation;
- normalise scheme/default port explicitly;
- apply one documented base-path normalisation policy before scope comparison;
- reject path forms whose interpretation is ambiguous between client/proxy/server;
- validate redirect targets before any redirected request is sent.

Scope must never be implemented using naive string prefix/suffix tests.

### 2.2 Address-class policy

For non-lab targets, loopback, link-local, multicast, unspecified and private/internal address classes are denied by default unless the exact address/range is explicitly authorised under a reviewed non-production target policy.

For dissertation laboratories, only the explicitly registered loopback/Docker-local target addresses are permitted.

Known metadata/link-local destinations remain denied by default even when local scanning is enabled.

### 2.3 DNS binding policy

A hostname allow-list is not sufficient by itself. The executor must validate the actual connection destination against the scan's immutable approved address policy.

DNS changes to an address outside that policy produce a blocking safety stop.

### 2.4 Ambient proxy policy

Scanner HTTP clients must ignore `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY` and equivalent environment proxy settings by default.

Explicit proxy support is out of initial scope. If later added, proxy configuration must be deliberate and must not weaken destination validation.

### 2.5 Authority/header policy

Rule modules may not independently set or override `Host`/`:authority` to route traffic somewhere other than the validated target.

Cross-authority redirects are blocked by default and credentials are never forwarded to an unvalidated authority.

## 3. Import/parser locks

### 3.1 Safe loaders only

YAML parsing must use a safe loader with no arbitrary object construction.

### 3.2 External references disabled by default

OpenAPI/Postman external references must not cause arbitrary local-file or network retrieval.

Initial implementation should resolve only references contained within the imported document/package. Remote external `$ref` resolution is disabled unless a later reviewed requirement adds a separately bounded resolver.

### 3.3 Parser resource ceilings

P3 must define and test explicit ceilings for:

- imported file bytes;
- expanded/decompressed bytes if compressed inputs are ever supported;
- recursion/reference depth;
- total resolved references/nodes where useful;
- parser execution failure/timeout behaviour where practical.

A pathological document must fail explicitly without unbounded memory, recursion or network activity.

### 3.4 Postman scripts inert

Pre-request scripts and test scripts are never executed by the scanner.

### 3.5 Imported target metadata cannot authorise scope

OpenAPI `servers`, Postman hosts/variables or other imported metadata may propose candidate endpoints but never expand the operator-approved target scope.

## 4. HTTP execution and budget locks

### 4.1 Atomic scheduling budgets

Global, rule and resource-control budgets are decremented/reserved atomically before scheduling/transmission so parallel workers cannot oversubscribe them.

Retries and redirect hops count as network requests against the relevant budgets.

### 4.2 Immutable scan scope/profile snapshots

Once a scan begins, its effective target scope, safety profile, budgets, rule catalogue version and non-secret identity metadata are immutable execution snapshots.

Changing project configuration does not retroactively alter an active scan.

### 4.3 Cancellation

Cancellation prevents new requests from being scheduled immediately. Queued work must not start after cancellation is observed.

### 4.4 No raw-client escape hatch

Only the central executor may create/use target-facing HTTP clients. Rule packages must not receive raw transport constructors.

## 5. Secret and identity locks

### 5.1 Session isolation

Every controlled identity, including anonymous, has an isolated HTTP session/cookie jar. No auth headers, cookies or refresh state may cross identity boundaries.

### 5.2 Secret-file safety

File-based secret references must resolve to regular files through a bounded explicit path policy. Directory traversal, device/special files and unsafe symlink behaviour are rejected.

Where supported, warn/block on obviously unsafe file permissions.

### 5.3 Sanitised exceptions

Raw request/response objects and raw library exceptions must not be written directly to logs when they may include credentials, cookies, URLs with sensitive query values or bodies.

Logging uses structured sanitised exception summaries.

### 5.4 Redaction claim boundary

The scanner guarantees removal of configured sensitive fields/headers and exact known runtime secret values before persistence/export. It must not claim that every arbitrary encoded/transformed secret can always be detected.

## 6. Local dashboard locks

### 6.1 Loopback bind

The scanner web/API surface binds to `127.0.0.1` by default. Remote binding is an explicit non-default operator action.

### 6.2 Host validation

The local web application validates expected Host/authority values and does not blindly trust arbitrary host headers.

### 6.3 No permissive CORS

The scanner dashboard/API does not enable wildcard/permissive CORS.

### 6.4 CSRF protection

State-changing browser actions require CSRF protection and appropriate Origin/Referer validation strategy. CORS is not considered sufficient CSRF defence.

### 6.5 Output escaping

Target-controlled values are always rendered as escaped text in dashboard and reports. No target response, endpoint name, error message or header is treated as trusted HTML/template source.

A restrictive local Content Security Policy should be used where compatible with the minimal server-rendered UI.

## 7. CLI/log presentation locks

Target-controlled strings presented in terminal/log output must be sanitised for dangerous control sequences, including ANSI escape/control characters and line-control abuse.

Canonical structured evidence may preserve normal Unicode text after redaction/minimisation, but operator-facing terminal output must not allow target content to manipulate terminal presentation.

## 8. Reporting locks

### 8.1 HTML

HTML reports must escape all target-controlled values and must not embed active HTML/SVG/script content from evidence.

### 8.2 CSV

CSV intended for spreadsheet use must neutralise formula execution for target-controlled values beginning with spreadsheet formula prefixes while preserving the semantic value in a documented way.

### 8.3 Filesystem paths

Export file paths are generated from server-controlled identifiers/sanitised slugs, not arbitrary user/target names. Path traversal components are never accepted as filesystem destinations.

### 8.4 Schema validation

Canonical JSON reports and evaluation datasets are validated against committed schemas before being treated as successful exports.

## 9. Laboratory containment locks

Canonical vulnerable labs must:

- publish ports to loopback only;
- never run privileged;
- not use host networking;
- not mount the Docker socket;
- avoid unnecessary host filesystem mounts;
- use synthetic credentials/data only;
- have no production service dependencies;
- use locked dependency mechanisms appropriate to Python/Node/Java;
- expose deterministic health/version/mode metadata;
- keep vulnerable/corrected modes semantically aligned except for seeded cases and required supporting metadata.

Where practical, container capabilities and unnecessary egress should be reduced.

## 10. Research-integrity locks

### 10.1 Ground truth separation

Ordinary scanner detection packages must not import/read ground-truth manifests. Only the evaluation layer may read them, after scanner output is produced.

### 10.2 Immutable comparison provenance

Every evaluation run records:

- scanner commit;
- rule catalogue version;
- lab version/mode;
- ground-truth manifest hash;
- matching-logic version/commit;
- specification hash;
- scan profile;
- validity status/reason.

### 10.3 Freeze before final collection

Before final P10 data collection, freeze ground-truth manifests, matching rules and metric formulas. A later methodological change invalidates/restarts affected experiment sets and is documented.

### 10.4 Retain inconvenient runs

Failed/flaky/poor runs are retained with explicit validity/exclusion reason. They are not silently deleted from the experiment record.

## 11. CI and supply-chain locks

### 11.1 GitHub Actions pinning

Third-party GitHub Actions must be pinned to full commit SHAs, not mutable branch/tag references. A comment may record the human-readable release version.

### 11.2 Workflow permissions

Workflows declare least-privilege permissions explicitly. Normal verification should require only read access unless a specific job demonstrably needs more.

### 11.3 Untrusted PR execution

Verification of PR-controlled code must not expose privileged repository secrets. Avoid unsafe use of `pull_request_target` with checkout/execution of untrusted PR code.

### 11.4 Dependency locks

P1 establishes a committed lock for scanner Python dependencies. P2 establishes committed lock/pinned dependency mechanisms for Node and Java labs.

### 11.5 Secret scanning

P1 must add a local/CI secret-scanning gate appropriate for the repository. The policy must consider secrets introduced in the commit/range, not only whether they are present in the final working tree.

Real secret exposure requires rotation/remediation; deleting the current file alone is not considered sufficient.

## 12. Phase-gate additions

### P1 additions

Must establish:

- safe secret-aware structured logging;
- terminal-control sanitisation baseline;
- dependency lock;
- SHA-pinned/least-privilege CI actions;
- secret scanning;
- no ambient proxy assumption in future HTTP configuration contract.

### P2 additions

Must pass lab containment and dependency-lock tests.

### P3 additions

Must pass parser/import adversarial suite before inventory is considered complete.

### P4 additions

Must pass all scope/DNS/redirect/budget/session/state adversarial tests before any vulnerability rule work begins.

### P5/P6 additions

Must pass semantic false-confirmation, cleanup-failure and error-to-pass adversarial tests.

### P7 additions

Must pass full secret-leak, report injection, CSV formula, evidence-size and schema tests.

### P8 additions

Must pass local-dashboard CSRF/Host/CORS/XSS/path tests and CLI control-sequence tests.

### P9/P10 additions

Must pass research-integrity attacks, ground-truth separation, run-retention and final provenance/freeze checks.

## 13. What remains after this review

No new product phase is required. The P1–P10 sequence remains correct.

The change is that the existing phases now have an explicit adversarial acceptance layer. AntiGravity should implement the project on the same roadmap, but it must treat `11-RED-TEAM-ATTACK-MATRIX.md` and this document as mandatory acceptance requirements for the relevant phase.

The first execution boundary remains **P1 — Repository and runtime foundation**, but P1 is not complete until its newly applicable red-team controls are proven.