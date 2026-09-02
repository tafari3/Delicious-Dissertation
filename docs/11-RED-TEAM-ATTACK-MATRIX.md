# Pre-Implementation Red-Team Attack Matrix

## 1. Purpose

This document adversarially reviews the dissertation architecture before product code exists. It defines the attacks, abuse cases and failure injections that the implementation must survive before the scanner can be treated as safe, reliable or academically reproducible.

The objective is not to turn the project into an offensive framework. These attacks are directed at the **scanner, its laboratories, its local dashboard, its evidence pipeline, its evaluation methodology and its delivery system**. They are implemented as local unit/integration/acceptance tests using controlled fixtures.

A phase may not claim completion while an applicable CRITICAL or HIGH red-team case for that phase is untested or failing.

## 2. Severity model

- **CRITICAL** — could make the scanner leave authorised scope, expose secrets, execute arbitrary code, materially corrupt research evidence, or perform uncontrolled/destructive traffic.
- **HIGH** — could bypass an important safety boundary, produce materially false findings, leak sensitive material, or invalidate reproducibility.
- **MEDIUM** — could degrade evidence integrity, availability, usability or diagnostic correctness without directly defeating a hard safety boundary.
- **LOW** — defence-in-depth or robustness condition.

## 3. Scope and network-boundary attacks

### RT-NET-001 — Alternate-IP notation scope bypass — CRITICAL — P4

Attempt equivalent IP targets using IPv4 integer, octal-like, hexadecimal-like, zero-padded, IPv4-mapped IPv6 and bracketed IPv6 forms.

**Required behaviour:** parse to one canonical address representation before policy comparison. Ambiguous/non-standard representations are rejected rather than interpreted differently by different libraries.

### RT-NET-002 — DNS rebinding / answer change — CRITICAL — P4

Resolve an allowed hostname to an approved address during preflight, then make subsequent resolution return an unapproved address.

**Required behaviour:** every new connection is checked against the effective approved address policy. A resolution change outside the approved set blocks before request transmission and records a safety stop.

### RT-NET-003 — Multi-address DNS mixed-scope answer — CRITICAL — P4

Return both approved and unapproved addresses for one allowed hostname.

**Required behaviour:** the executor must not silently let the transport choose an unapproved address. Connection candidates must be validated before use.

### RT-NET-004 — Cloud/container metadata destination — CRITICAL — P4

Attempt direct or redirected access to link-local/metadata-class addresses (including IPv4 and IPv6 link-local), loopback aliases and host-internal addresses outside explicit lab scope.

**Required behaviour:** private/link-local/loopback ranges are denied by default for non-lab targets. Local laboratory ranges are allowed only when explicitly registered as lab scope. Metadata/link-local addresses remain denied unless an explicit test-only fixture exists and no real metadata service is reachable.

### RT-NET-005 — Hostname suffix confusion — CRITICAL — P4

Use names such as `allowed.example.attacker.test`, mixed case, trailing dots, Unicode/punycode variants and labels that visually resemble the approved hostname.

**Required behaviour:** canonical DNS-name equality/policy matching; no naive string-prefix/suffix matching.

### RT-NET-006 — Base-path traversal/encoding escape — CRITICAL — P4

Use `..`, `%2e`, `%2f`, double encoding, repeated slashes, backslashes and path-normalisation edge cases to escape an allowed base path.

**Required behaviour:** scope comparison occurs against a canonicalised request path using one documented normalisation policy. Ambiguous path forms that could be interpreted differently by proxy/client/server are blocked.

### RT-NET-007 — Redirect chain escape — CRITICAL — P4

Attempt same-host redirect followed by cross-host, scheme downgrade, port change, userinfo insertion, path escape or DNS answer change.

**Required behaviour:** every hop is independently validated before following; blocked hops do not transmit credentials to the redirect destination.

### RT-NET-008 — Credential forwarding on redirect — CRITICAL — P4

Attempt redirect from an authenticated endpoint to another authority.

**Required behaviour:** cross-authority redirect is blocked by policy. Authentication headers/cookies are never forwarded to an unvalidated authority.

### RT-NET-009 — Environment proxy bypass — CRITICAL — P1/P4

Set `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY` or platform-equivalent environment variables to route scanner traffic through an attacker-controlled proxy.

**Required behaviour:** scanner HTTP clients default to ignoring ambient proxy environment (`trust_env=false` or equivalent). Proxy use requires explicit reviewed configuration and must not weaken target-scope enforcement.

### RT-NET-010 — Non-HTTP transport injection — CRITICAL — P3/P4

Supply `file:`, `ftp:`, `gopher:`, `data:`, Unix-socket-like or library-specific transport URLs through target/spec/server metadata.

**Required behaviour:** only HTTP/HTTPS are accepted for network targets/spec fetches; local import files use a separate bounded local-file path, never URL transport coercion.

### RT-NET-011 — Host header / authority mismatch — HIGH — P4

Attempt to connect to one approved endpoint while sending another Host/`:authority` value.

**Required behaviour:** target authority is derived from the validated target, not arbitrary rule/user headers. Rules cannot override Host/authority in a way that changes routing.

### RT-NET-012 — Connection reuse after scope change — HIGH — P4

Change target resolution/policy after an existing keep-alive connection exists.

**Required behaviour:** connection pools cannot be used to bypass current scan/target scope. A scan uses an immutable scope snapshot, and destination validation is tied to the connection actually used.

## 4. HTTP budget and concurrency attacks

### RT-BUDGET-001 — Parallel oversubscription — CRITICAL — P4

Race multiple workers against the final remaining global/per-rule/resource budget.

**Required behaviour:** counters are atomic at the scheduling boundary; total transmitted requests never exceed the configured hard maximum.

### RT-BUDGET-002 — Retry budget bypass — HIGH — P4

Trigger retryable transport failures repeatedly.

**Required behaviour:** every attempt, including retries and redirects, consumes the relevant request budget.

### RT-BUDGET-003 — Redirect budget bypass — HIGH — P4

Use redirect chains to multiply network requests without decrementing total/rule budgets.

**Required behaviour:** each network request/hop consumes total budget; redirect count is independently capped.

### RT-BUDGET-004 — Cancellation race — HIGH — P4

Issue stop/cancel while requests are queued and running.

**Required behaviour:** cancellation prevents new scheduling immediately; already-running work is bounded and no queued work starts after stop.

### RT-BUDGET-005 — Resource-test budget inheritance bug — CRITICAL — P6

Attempt resource-control rules using the larger general scan budget.

**Required behaviour:** resource-control requests require both global budget and stricter resource sub-budget; exhaustion of either stops the rule.

### RT-BUDGET-006 — Rule exception causes unbounded retry/loop — HIGH — P5/P6

Inject deterministic parsing/comparison exceptions.

**Required behaviour:** a rule fails `ERROR`/`INCONCLUSIVE` according to contract and cannot create an uncontrolled rescheduling loop.

## 5. Specification/import attacks

### RT-SPEC-001 — Oversized specification — HIGH — P3

Supply an OpenAPI/Postman document larger than the configured import cap.

**Required behaviour:** reject before unbounded memory consumption. File and remote-import size ceilings are explicit and tested.

### RT-SPEC-002 — Deeply nested/recursive schema — HIGH — P3

Use recursive `$ref`, deep object nesting, reference cycles and pathological schema graphs.

**Required behaviour:** bounded recursion/reference traversal with cycle detection. Parsing produces warning/error rather than stack/memory exhaustion.

### RT-SPEC-003 — External-reference fetch escape — CRITICAL — P3/P4

Use `$ref` or other import references pointing to arbitrary local files, remote hosts, metadata services or out-of-scope URLs.

**Required behaviour:** external reference resolution is disabled by default. If later enabled, it uses explicit allow-listed local roots or the controlled HTTP executor and separate import budgets.

### RT-SPEC-004 — YAML unsafe object construction — CRITICAL — P3

Provide YAML tags/constructs that unsafe loaders could use for arbitrary object construction.

**Required behaviour:** safe loader only; no arbitrary Python/object construction.

### RT-SPEC-005 — Compressed/decompression bomb — HIGH — P3/P8

Submit compressed/imported content with tiny compressed size and excessive expanded size.

**Required behaviour:** compressed uploads are either unsupported or bounded by expanded-byte and entry-count ceilings before processing.

### RT-SPEC-006 — Postman script execution — CRITICAL — P3

Include pre-request/test JavaScript that attempts filesystem/network/process access.

**Required behaviour:** scripts are parsed as inert metadata or ignored; never executed.

### RT-SPEC-007 — Server URL scope poisoning — CRITICAL — P3/P4

Place unapproved servers/base URLs in OpenAPI server entries or Postman variables.

**Required behaviour:** imported server metadata never expands authorised target scope. User target policy wins.

### RT-SPEC-008 — Variable expansion injection — HIGH — P3

Use recursive/unresolved/environment-like variables to produce unexpected URLs or credentials.

**Required behaviour:** bounded deterministic variable expansion; unresolved variables remain warnings/inert values and cannot read arbitrary environment secrets.

## 6. Identity, secret and session attacks

### RT-SECRET-001 — Secret in headers/body/query/path — CRITICAL — P4/P7

Echo known fixture secrets in every evidence-bearing location.

**Required behaviour:** known runtime secret values are redacted before persistence/export/logging regardless of field name.

### RT-SECRET-002 — Encoded secret leakage — HIGH — P4/P7

Echo secrets after common reversible encodings/quoting forms used by the application under test.

**Required behaviour:** at minimum structured auth fields and exact known secret values are removed; tests document which transformed forms are and are not guaranteed. No false claim of universal secret detection.

### RT-SECRET-003 — Secret-file path traversal/symlink — CRITICAL — P4

Configure a file secret reference using traversal, symlink, device/special file or unintended world-readable path.

**Required behaviour:** secret files must be regular files; path handling is explicit; permission checks are applied where supported; no directory/device reads; error output never prints secret content.

### RT-SECRET-004 — Secret in exception/log formatting — CRITICAL — P1/P4

Cause authentication/network libraries to include request headers or URLs containing credentials in exceptions.

**Required behaviour:** exception logging uses sanitised structured summaries, not raw exception/request dumps.

### RT-ID-001 — Identity session cross-contamination — CRITICAL — P4/P5

Set cookies/tokens under identity A then execute identity B.

**Required behaviour:** isolated cookie jars/session state; no credential/header/cookie crossover.

### RT-ID-002 — Anonymous inherits authenticated state — CRITICAL — P4/P5

Execute anonymous tests after authenticated requests.

**Required behaviour:** anonymous context has a clean independent session and explicitly omits auth material.

### RT-ID-003 — Token refresh scope escape — HIGH — P4

Configure refresh/login URL outside approved target authority.

**Required behaviour:** refresh/authentication network actions are separately scope-validated through controlled execution.

## 7. Rule-engine correctness attacks

### RT-RULE-001 — HTTP 2xx false confirmation — HIGH — P5/P6

Return generic 200 responses for denied/not-found/error conditions.

**Required behaviour:** no rule confirms vulnerability from status alone; semantic proof conditions and baseline comparison are required.

### RT-RULE-002 — Error becomes pass — CRITICAL — P5/P6

Force timeout, parse failure, body truncation or comparison exception during a test.

**Required behaviour:** result is `ERROR` or `INCONCLUSIVE`; never `PASS_OBSERVED`.

### RT-RULE-003 — Reflection mistaken for object access — HIGH — P5

Echo requested object ID without returning protected object content.

**Required behaviour:** BOLA proof requires stable protected-object/ownership semantics, not mere identifier reflection.

### RT-RULE-004 — Same-length/body-shape collision — HIGH — P5

Return semantically different objects with similar status/length/schema.

**Required behaviour:** comparator uses rule-specific semantic markers where confirmation requires them; otherwise result remains suspected/inconclusive.

### RT-RULE-005 — Mass-assignment reflection without persistence — HIGH — P5

Echo protected input property in response but do not store it.

**Required behaviour:** BOPLA write confirmation requires independent read-back/state verification.

### RT-RULE-006 — Cleanup failure after mutation — HIGH — P5/P6

Cause mutation proof to succeed but cleanup/reset to fail.

**Required behaviour:** finding may remain valid, but scan records cleanup failure and safety state; additional mutation tests are stopped when safe reset cannot be guaranteed.

### RT-RULE-007 — Non-idempotent baseline repetition — HIGH — P5/P6

Use endpoints where repeated “baseline” calls mutate state.

**Required behaviour:** mutation classification is metadata-driven; read-only profile refuses operations not demonstrably safe.

## 8. Persistence and state-machine attacks

### RT-STATE-001 — Invalid transition injection — HIGH — P4

Attempt `DRAFT -> EXECUTING`, `BLOCKED -> EXECUTING`, completed-scan mutation, or recovery that skips preflight.

**Required behaviour:** transitions are centrally validated; finished scan provenance is immutable except explicitly versioned annotations.

### RT-STATE-002 — Crash during evidence persistence — HIGH — P4/P7

Simulate process failure between rule result, redaction and DB commit.

**Required behaviour:** unredacted evidence is never committed. Transactions leave an explicit incomplete/error state rather than a false completed scan.

### RT-STATE-003 — Concurrent scan budget/state collision — HIGH — P4

Run two scans against same project/target concurrently.

**Required behaviour:** budgets/state are scan-scoped; one scan cannot decrement or inherit another's counters/identities/evidence.

### RT-DB-001 — SQL/meta-character injection — HIGH — P4/P7

Put quotes/control strings/SQL-looking payloads in target-controlled fields.

**Required behaviour:** parameterised ORM/query use; data never becomes executable SQL.

### RT-DB-002 — Unbounded evidence/database growth — HIGH — P7

Return many large bodies/findings within network budget.

**Required behaviour:** per-response, per-evidence and per-scan persisted-size limits or defensible bounded derivation exist; exceeding them truncates/stops explicitly.

## 9. Dashboard/local web attacks

### RT-WEB-001 — Cross-site request forgery against localhost — CRITICAL — P8

From a malicious external webpage, attempt state-changing requests to the locally running scanner UI/API.

**Required behaviour:** state-changing browser actions require CSRF protection and origin-aware controls. CORS is not a substitute for CSRF protection.

### RT-WEB-002 — Browser DNS/localhost interaction — HIGH — P8

Attempt requests from arbitrary web origins to scanner endpoints.

**Required behaviour:** scanner binds to loopback by default; no permissive CORS; Host validation rejects unexpected authorities; remote bind requires explicit opt-in.

### RT-WEB-003 — Stored/reflected XSS via target-controlled evidence — CRITICAL — P7/P8

Return HTML/script/event-handler payloads in endpoint names, errors, headers or response excerpts, then view reports/dashboard.

**Required behaviour:** all target-controlled text is escaped by default; no unsafe HTML rendering; Content Security Policy is applied to the local UI/report where practical.

### RT-WEB-004 — Template injection — HIGH — P7/P8

Place template syntax in target-controlled strings.

**Required behaviour:** target data is always passed as data, never evaluated/compiled as template source.

### RT-WEB-005 — Path traversal in export/download — HIGH — P7/P8

Use project/report names containing traversal or reserved path characters.

**Required behaviour:** server chooses filesystem paths/IDs; user-visible names never become arbitrary filesystem paths.

## 10. Reporting/export attacks

### RT-REPORT-001 — CSV formula injection — HIGH — P7

Put values beginning with `=`, `+`, `-` or `@` in target-controlled CSV fields.

**Required behaviour:** spreadsheet-oriented CSV exports neutralise formula execution while preserving the original semantic value through documented escaping/quoting.

### RT-REPORT-002 — HTML active-content injection — CRITICAL — P7

Insert script/style/svg/event-handler/URL payloads into finding evidence.

**Required behaviour:** HTML report treats all target evidence as text/escaped data. Reports do not embed active target-controlled HTML.

### RT-REPORT-003 — Terminal/ANSI control injection — HIGH — P1/P7/P8

Return ANSI escapes, carriage returns, terminal hyperlinks or bidirectional controls in target-controlled strings shown by CLI/logs.

**Required behaviour:** CLI/log presentation sanitises dangerous control characters or renders an escaped representation. Stored canonical evidence may retain safe structured Unicode subject to size/redaction rules.

### RT-REPORT-004 — JSON/CSV schema confusion — MEDIUM — P7

Use duplicate/confusable fields, nulls, huge integers and unexpected Unicode.

**Required behaviour:** canonical typed models and report-schema validation; export failure is explicit rather than silent field loss.

## 11. Laboratory containment attacks

### RT-LAB-001 — Vulnerable lab exposed beyond loopback — CRITICAL — P2

Inspect published Docker ports/bind addresses.

**Required behaviour:** vulnerable labs publish only to `127.0.0.1` by default; no `0.0.0.0` exposure in canonical compose configuration.

### RT-LAB-002 — Excess container privilege — HIGH — P2

Inspect container privilege/capabilities/host mounts/network mode.

**Required behaviour:** no privileged containers, no host network, no Docker socket, no unnecessary host filesystem mounts; drop capabilities where practical.

### RT-LAB-003 — Lab reaches external production services — HIGH — P2

Attempt outbound calls from lab functionality.

**Required behaviour:** canonical labs have no production/external service dependencies. Where practical, Docker network design limits unnecessary egress.

### RT-LAB-004 — Vulnerable/corrected mode drift — HIGH — P2/P9

Change unrelated behaviour between modes.

**Required behaviour:** direct contract tests prove mode differences are limited to intentionally seeded cases and required supporting metadata.

### RT-LAB-005 — Ground-truth leakage into scanner runtime — HIGH — P5/P9

Make ground-truth files available to ordinary scan logic/import paths.

**Required behaviour:** scanner detector modules do not read/import ground-truth manifests. Evaluation layer alone reads them after scanner results exist.

## 12. Evaluation/research-integrity attacks

### RT-EVAL-001 — Ground truth changed after results — CRITICAL — P9/P10

Modify manifest after scanner results to improve metrics.

**Required behaviour:** every run stores exact ground-truth hash/version; mismatch invalidates comparison. Final collection freezes ground truth and matching logic.

### RT-EVAL-002 — Failed/inconvenient runs discarded — HIGH — P9/P10

Remove unstable or poor-performing runs.

**Required behaviour:** runs are retained with validity status/reason. Exclusion criteria are predeclared and machine-readable.

### RT-EVAL-003 — Finding matcher overmatches — HIGH — P9

Generate a finding with same category but wrong endpoint/fixture.

**Required behaviour:** deterministic matching uses rule + operation/fixture/ground-truth identity, not free-text similarity.

### RT-EVAL-004 — Scanner detector reads evaluation expectation — CRITICAL — P9

Attempt to import ground-truth IDs/expected states into detection decisions.

**Required behaviour:** architectural test/lint/review ensures detector packages have no dependency on evaluation ground-truth modules/files.

### RT-EVAL-005 — ZAP comparison misrepresentation — HIGH — P9/P10

Count unsupported semantic authorisation cases as ZAP false negatives.

**Required behaviour:** comparison includes an applicability/coverage dimension and distinguishes “not equivalently tested” from “tested and missed.”

## 13. Dependency, CI and repository attacks

### RT-SUPPLY-001 — GitHub Actions mutable-tag takeover — HIGH — P1

Use third-party actions pinned only to moving tags/branches.

**Required behaviour:** third-party GitHub Actions are pinned to full commit SHAs; optional comment records human-readable version.

### RT-SUPPLY-002 — Excess workflow token permissions — HIGH — P1

Inspect default `GITHUB_TOKEN` permissions.

**Required behaviour:** workflow declares least privilege, normally `contents: read`; write permissions are granted only to a specific job when genuinely required.

### RT-SUPPLY-003 — PR code exfiltrates repository secrets — CRITICAL — P1

Ensure untrusted pull-request code cannot receive privileged secrets in verification workflows.

**Required behaviour:** ordinary PR verification uses no privileged secrets. Avoid unsafe `pull_request_target` execution of PR-controlled code.

### RT-SUPPLY-004 — Unlocked dependencies — HIGH — P1

Modify upstream package versions without repository changes.

**Required behaviour:** reproducible locked Python dependencies; Node/Java labs use committed lock/pinned mechanisms appropriate to their ecosystems by P2.

### RT-SUPPLY-005 — Dependency install executes unexpected remote project hooks — MEDIUM — P1/P2

Review package/lab build process for avoidable script execution and remote downloads.

**Required behaviour:** dependencies are minimal/documented; builds are reproducible; security-sensitive build steps are explicit.

### RT-GIT-001 — Secret committed then deleted — CRITICAL — P1+

Insert a dummy canary secret, then remove it in a later commit.

**Required behaviour:** CI/local secret scanning considers the changed commit/range/history appropriate to the workflow, not only current working-tree text. Real secret exposure triggers rotation and history remediation rather than “delete and forget.”

## 14. Required red-team test suites by phase

### P1

- RT-NET-009
- RT-SECRET-004
- RT-REPORT-003 baseline sanitiser
- RT-SUPPLY-001 through RT-SUPPLY-004
- RT-GIT-001 policy/secret scanning

### P2

- RT-LAB-001 through RT-LAB-004
- dependency locking for Node/Java labs

### P3

- RT-NET-010
- RT-SPEC-001 through RT-SPEC-008

### P4

- RT-NET-001 through RT-NET-012
- RT-BUDGET-001 through RT-BUDGET-004
- RT-SECRET-001 through RT-SECRET-004
- RT-ID-001 through RT-ID-003
- RT-STATE-001 through RT-STATE-003
- RT-DB-001

### P5/P6

- RT-RULE-001 through RT-RULE-007
- RT-BUDGET-005 through RT-BUDGET-006

### P7

- RT-DB-002
- RT-REPORT-001 through RT-REPORT-004
- RT-WEB-003/004 report-side behaviour
- full secret-leak regression suite

### P8

- RT-WEB-001 through RT-WEB-005
- CLI control-character regression

### P9/P10

- RT-LAB-005
- RT-EVAL-001 through RT-EVAL-005
- final supply-chain/dependency/security review

## 15. Red-team completion rule

An attack is considered covered only when:

1. the expected safe behaviour is encoded in an automated test where technically practical;
2. the test fails when the protection is deliberately removed or a focused negative fixture proves the control is meaningful;
3. the test is included in the canonical phase verification/acceptance path;
4. the result is reproducible from a clean environment;
5. no real third-party system is required.

Documentation-only assertions are not sufficient for CRITICAL/HIGH cases once the relevant implementation phase exists.