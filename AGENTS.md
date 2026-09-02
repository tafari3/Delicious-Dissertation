# AGENTS.md — AntiGravity Execution Contract

## 1. Purpose

This file is the execution contract for AI coding agents working in this repository, including AntiGravity on the implementation VM.

Read this file and the authoritative documents under `docs/` before modifying code.

## 2. Source-of-truth precedence

When instructions conflict, use this order:

1. the approved academic proposal and its explicit research/safety boundaries;
2. `docs/00-PROJECT-CHARTER.md`;
3. `docs/06-SAFETY-SECURITY-MODEL.md` for hard safety constraints;
4. `docs/12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md` for mandatory controls introduced by adversarial review;
5. `docs/11-RED-TEAM-ATTACK-MATRIX.md` for adversarial acceptance cases;
6. `docs/02-TEST-CATALOGUE.md` for scanner rule semantics;
7. `docs/04-LABS-AND-EVALUATION.md` for experimental methodology;
8. `docs/01-ARCHITECTURE.md`;
9. `docs/05-DATA-AND-REPORTING.md`;
10. `docs/03-USER-JOURNEYS.md`;
11. `docs/08-REQUIREMENTS-TRACEABILITY.md`;
12. `docs/09-CONFIGURATION-DEFAULTS.md` for initial operational defaults;
13. `docs/07-IMPLEMENTATION-PLAN.md`;
14. `docs/10-REPOSITORY-AND-DELIVERY.md`;
15. implementation code/tests.

If code and documentation disagree, do not silently redefine the requirement in code. Fix the implementation or explicitly update the design in the same reviewed change when the proposal permits it.

## 3. Core mission

Build an autonomous, cross-platform, black-box REST API security scanner that safely tests the bounded catalogue defined in this repository and produces reproducible, redacted, OWASP-aligned evidence for synthetic Zimbabwean fintech and e-government laboratory scenarios.

Do not turn this into a general exploitation framework or an enterprise SaaS platform.

## 4. Mandatory safety invariants

These must never be bypassed for convenience:

1. No scan without explicit target allow-list/scope validation.
2. Revalidate scope on every request and redirect.
3. All network traffic goes through the single controlled HTTP executor.
4. Hard request/rate ceilings are always present.
5. Resource-control tests use a stricter independent budget.
6. Default profile is non-destructive/read-only.
7. Write tests run only against explicitly controlled disposable fixtures with cleanup/reset.
8. Stop at proof-of-condition; do not escalate into extraction or disruption.
9. Credentials/tokens/cookies/API keys are redacted before persistence/export.
10. Never log resolved secret values.
11. Do not implement credential stuffing, password spraying, destructive/unrestricted fuzzing or DoS testing.
12. Never point automated evaluation at real Zimbabwean fintech/government systems.
13. Imported specifications cannot expand authorised network scope.
14. Ambient proxy environment must not reroute scanner target traffic by default.
15. Vulnerable laboratories bind to loopback by default and must not be exposed as canonical public services.

If a requested implementation would break one of these, stop that change and preserve the invariant.

## 5. Work mode

Follow `docs/07-IMPLEMENTATION-PLAN.md` sequentially unless an issue/PR explicitly states a narrower current phase.

At the start of work:

1. inspect repository status and current branch;
2. pull/fetch the intended branch safely;
3. read the current phase issue/requirements;
4. read the relevant phase entries in `docs/11-RED-TEAM-ATTACK-MATRIX.md` and `docs/12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md`;
5. inspect existing implementation/tests before changing anything;
6. run the canonical verification command if the repository is already bootstrapped.

Do not create a parallel architecture or duplicate subsystem when one already exists.

## 6. Red-team completion rule

A phase is not complete merely because its happy-path acceptance tests pass.

For the current phase:

- every applicable **CRITICAL** and **HIGH** red-team case must have an automated test where technically practical;
- a protection must be shown to be meaningful through a focused negative/adversarial fixture, not only by asserting implementation structure;
- applicable tests must run in the canonical verification/phase acceptance path;
- unresolved CRITICAL/HIGH red-team failures block merge;
- MEDIUM/LOW cases may be deferred only with an explicit issue/rationale and only if no higher-level safety/research requirement is weakened.

Do not “pass” an attack case by weakening its expected safe behaviour.

## 7. Implementation discipline

Prefer small modules with explicit contracts, typed domain models, deterministic behaviour, central safety enforcement, unit tests plus seeded-lab integration tests, versioned rule identifiers, structured outputs and minimal dependencies.

Avoid hidden global state, raw HTTP clients inside rule modules, status-code-only vulnerability decisions, swallowing errors into pass states, target-language-specific scanner logic, arbitrary shell execution from scan definitions, executing Postman scripts supplied by targets, and needless overengineering.

## 8. Dependency and supply-chain policy

Before adding a dependency:

- confirm the standard library/current dependencies cannot reasonably do the job;
- choose mature maintained packages;
- pin through the selected lockfile mechanism;
- avoid cloud accounts or recurring services;
- document important security-sensitive dependencies.

Additionally:

- third-party GitHub Actions must be pinned to full commit SHAs;
- workflows must declare least-privilege token permissions;
- ordinary pull-request verification must not expose privileged secrets to PR-controlled code;
- scanner Python dependencies are locked from P1;
- Node/Java laboratory dependencies are locked/pinned from P2;
- P1 establishes repository secret scanning suitable for detecting secrets introduced in the changed commit/range.

No LLM/API dependency is required for the scanner.

## 9. Secret policy

Secrets may enter the runtime through supported local secret references, initially environment variables or ignored local secret files.

Never commit real `.env` values, tokens, passwords, cookies, API keys, private keys/certificates, real target dumps or unresolved secret-bearing scanner evidence.

Use synthetic fixture credentials for tests and make them visibly non-production.

If a real secret is ever committed, deleting it from the current file is not enough: rotate/remediate the secret and address repository history/exposure as appropriate.

## 10. Network/scope implementation rule

When P3/P4 network functionality is implemented, AntiGravity must follow the locked network policy rather than improvising permissive URL handling.

At minimum:

- only HTTP/HTTPS target transports;
- canonical host/IP/port/path policy;
- no naive string-prefix/suffix scope checks;
- actual connection destination validation;
- DNS rebinding/mixed-address tests;
- redirect revalidation before transmission;
- no credential forwarding to an unvalidated authority;
- ambient proxy environment ignored by default;
- imported OpenAPI/Postman server metadata cannot authorise scope;
- retries and redirects consume hard budgets;
- global/rule/resource budgets cannot oversubscribe under concurrency.

## 11. Rule implementation contract

Before implementing a scanner rule, read its entry in `docs/02-TEST-CATALOGUE.md` and relevant red-team rule cases.

Every rule implementation must include:

- stable rule ID/version;
- applicability/prerequisite logic;
- deterministic request plan;
- safe payload policy;
- request budget;
- proof and suspected/inconclusive conditions where applicable;
- explicit stop condition;
- evidence builder;
- OWASP/CWE mapping;
- positive vulnerable test;
- corrected/negative test;
- request-budget/safety test;
- redaction test;
- seeded-lab integration proof where the lab case exists;
- applicable semantic false-confirmation/adversarial tests.

Do not mark a rule complete using only mocks when the corresponding lab exists. Do not classify a finding as confirmed solely because an endpoint returned HTTP 2xx.

## 12. Result semantics

Use exactly the defined rule states:

- `NOT_APPLICABLE`
- `PASS_OBSERVED`
- `CONFIRMED`
- `SUSPECTED`
- `INFORMATIONAL`
- `INCONCLUSIVE`
- `ERROR`

Never convert `ERROR` or `INCONCLUSIVE` into a pass. Severity and confidence are separate fields.

## 13. Laboratory discipline

Ground truth remains independent of scanner detection logic. The scanner must not import ground-truth manifests during ordinary detection.

For each lab change:

- vulnerable mode direct functional test proves the seeded weakness;
- corrected mode direct functional test proves the correction;
- reset remains deterministic;
- synthetic data only;
- API description stays aligned except where an intentional inventory mismatch is the seeded case;
- canonical ports publish to loopback only;
- no privileged container, host networking, Docker socket or unnecessary host mount;
- no production service dependency.

Do not change ground truth after seeing scanner results merely to improve metrics.

## 14. Data/evidence/reporting discipline

Persist structured, minimised, redacted evidence. Before saving/exporting any observation:

1. remove sensitive headers;
2. redact sensitive body fields;
3. redact runtime-known secret values;
4. truncate to configured evidence size;
5. record whether truncation occurred.

Do not persist raw unredacted exchanges “temporarily”.

Target-controlled data must be treated as hostile when rendered:

- HTML/dashboard output is escaped text, never active target HTML;
- CSV spreadsheet exports neutralise formula execution;
- CLI/log output sanitises dangerous terminal control sequences;
- export paths come from server-controlled identifiers/sanitised names, never raw traversal-capable target/user strings.

## 15. Local dashboard discipline

The local web/API surface:

- binds to loopback by default;
- does not enable permissive/wildcard CORS;
- validates expected Host/authority values;
- protects state-changing browser actions against CSRF;
- never renders resolved secrets;
- escapes target-controlled output.

Remote binding is explicit non-default behaviour and must not silently become the standard configuration.

## 16. Canonical verification

Once P1 establishes the task surface, `make verify` (or the repository-documented canonical equivalent) is the required local and CI gate.

It should cover formatting, lint, type/static checks, unit tests, safety tests, applicable red-team tests and appropriate integration tests. Lab/rule changes must also run relevant seeded-lab integration proof when not already covered.

## 17. Git/PR discipline

- Work on the current intended feature/phase branch, not directly on `main`, unless explicitly bootstrapping an empty repository.
- Keep changes scoped to the current phase.
- Do not create duplicate branches/PRs for the same work.
- Do not rewrite unrelated code merely for style.
- Do not commit generated secrets/results.
- Before merge, verify the exact branch head and fresh checks for that head.
- Resolve real CI/review/red-team failures on the same PR where practical.
- Do not treat stale successful runs from an earlier head as proof for a changed head.

## 18. Documentation rule

Update documentation when behaviour changes public CLI/UI workflows, rule semantics, architecture boundaries, evidence/report schemas, lab ground truth, evaluation methodology, security controls or setup/verification commands.

Do not change research questions, core scope, red-team expected safe behaviour or prohibited capabilities through a casual implementation edit.

## 19. Anti-overengineering check

Do not introduce Kubernetes, microservices, queues, distributed workers, external database infrastructure, SPA frontend, multi-tenancy, enterprise SSO/RBAC, LLM services or cloud deployment as default architecture.

If a requirement can be implemented cleanly inside the documented local Python/FastAPI/SQLite architecture, implement it there.

## 20. Completion report for each execution slice

Report:

- what changed;
- files/components changed;
- acceptance and red-team tests and results;
- branch and exact commit SHA;
- relevant PR;
- unresolved blockers/deferred lower-severity attack cases;
- exact next phase/task.

Never claim completion while required tests are failing or integration/red-team evidence is missing.

## 21. Current execution boundary

Phase 0 is merged. A pre-implementation red-team hardening review has been added before P1 implementation.

After that hardening review is merged and the canonical P1 branch is fast-forwarded to the resulting `main`, begin **P1 — Repository/runtime foundation** on the existing P1 branch/issue.

Do not start P5 authorisation-rule implementation before P4 controlled HTTP execution, scope enforcement, identity/session foundations and their applicable red-team gates exist and pass.