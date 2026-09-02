# AGENTS.md — AntiGravity Execution Contract

## 1. Purpose

This file is the execution contract for AI coding agents working in this repository, including AntiGravity on the implementation VM.

Read this file and the authoritative documents under `docs/` before modifying code.

## 2. Source-of-truth precedence

When instructions conflict, use this order:

1. the approved academic proposal and its explicit research/safety boundaries;
2. `docs/00-PROJECT-CHARTER.md`;
3. `docs/06-SAFETY-SECURITY-MODEL.md` for hard safety constraints;
4. `docs/02-TEST-CATALOGUE.md` for scanner rule semantics;
5. `docs/04-LABS-AND-EVALUATION.md` for experimental methodology;
6. `docs/01-ARCHITECTURE.md`;
7. `docs/05-DATA-AND-REPORTING.md`;
8. `docs/03-USER-JOURNEYS.md`;
9. `docs/09-CONFIGURATION-DEFAULTS.md` for initial operational defaults;
10. `docs/07-IMPLEMENTATION-ROADMAP.md`;
11. `docs/08-REPOSITORY-AND-DELIVERY.md`;
12. implementation code/tests.

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

If a requested implementation would break one of these, stop that change and preserve the invariant.

## 5. Work mode

Follow `docs/07-IMPLEMENTATION-ROADMAP.md` sequentially unless an issue/PR explicitly states a narrower current phase.

At the start of work:

1. inspect repository status and current branch;
2. pull/fetch the intended branch safely;
3. read the current phase issue/requirements;
4. inspect existing implementation/tests before changing anything;
5. run the canonical verification command if the repository is already bootstrapped.

Do not create a parallel architecture or duplicate subsystem when one already exists.

## 6. Implementation discipline

Prefer small modules with explicit contracts, typed domain models, deterministic behaviour, central safety enforcement, unit tests plus seeded-lab integration tests, versioned rule identifiers, structured outputs and minimal dependencies.

Avoid hidden global state, raw HTTP clients inside rule modules, status-code-only vulnerability decisions, swallowing errors into pass states, target-language-specific scanner logic, arbitrary shell execution from scan definitions, executing Postman scripts supplied by targets, and needless overengineering.

## 7. Dependency policy

Before adding a dependency:

- confirm the standard library/current dependencies cannot reasonably do the job;
- choose mature maintained packages;
- pin through the selected lockfile mechanism;
- avoid cloud accounts or recurring services;
- document important security-sensitive dependencies.

No LLM/API dependency is required for the scanner.

## 8. Secret policy

Secrets may enter the runtime through supported local secret references, initially environment variables or ignored local secret files.

Never commit real `.env` values, tokens, passwords, cookies, API keys, private keys/certificates, real target dumps or unresolved secret-bearing scanner evidence.

Use synthetic fixture credentials for tests and make them visibly non-production.

## 9. Rule implementation contract

Before implementing a scanner rule, read its entry in `docs/02-TEST-CATALOGUE.md`.

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
- seeded-lab integration proof where the lab case exists.

Do not mark a rule complete using only mocks when the corresponding lab exists. Do not classify a finding as confirmed solely because an endpoint returned HTTP 2xx.

## 10. Result semantics

Use exactly the defined rule states:

- `NOT_APPLICABLE`
- `PASS_OBSERVED`
- `CONFIRMED`
- `SUSPECTED`
- `INFORMATIONAL`
- `INCONCLUSIVE`
- `ERROR`

Never convert `ERROR` or `INCONCLUSIVE` into a pass. Severity and confidence are separate fields.

## 11. Laboratory discipline

Ground truth remains independent of scanner detection logic. The scanner must not import ground-truth manifests during ordinary detection.

For each lab change:

- vulnerable mode direct functional test proves the seeded weakness;
- corrected mode direct functional test proves the correction;
- reset remains deterministic;
- synthetic data only;
- API description stays aligned except where an intentional inventory mismatch is the seeded case.

Do not change ground truth after seeing scanner results merely to improve metrics.

## 12. Data/evidence discipline

Persist structured, minimised, redacted evidence. Before saving/exporting any observation:

1. remove sensitive headers;
2. redact sensitive body fields;
3. redact runtime-known secret values;
4. truncate to configured evidence size;
5. record whether truncation occurred.

Do not persist raw unredacted exchanges “temporarily”.

## 13. Canonical verification

Once P1 establishes the task surface, `make verify` (or the repository-documented canonical equivalent) is the required local and CI gate.

It should cover formatting, lint, type/static checks, unit tests, safety tests and appropriate integration tests. Lab/rule changes must also run relevant seeded-lab integration proof when not already covered.

## 14. Git/PR discipline

- Work on the current intended feature/phase branch, not directly on `main`, unless explicitly bootstrapping an empty repository.
- Keep changes scoped to the current phase.
- Do not create duplicate branches/PRs for the same work.
- Do not rewrite unrelated code merely for style.
- Do not commit generated secrets/results.
- Before merge, verify the exact branch head and fresh checks for that head.
- Resolve real CI/review failures on the same PR where practical.
- Do not treat stale successful runs from an earlier head as proof for a changed head.

## 15. Documentation rule

Update documentation when behaviour changes public CLI/UI workflows, rule semantics, architecture boundaries, evidence/report schemas, lab ground truth, evaluation methodology or setup/verification commands.

Do not change research questions, core scope or prohibited capabilities through a casual implementation edit.

## 16. Anti-overengineering check

Do not introduce Kubernetes, microservices, queues, distributed workers, external database infrastructure, SPA frontend, multi-tenancy, enterprise SSO/RBAC, LLM services or cloud deployment as default architecture.

If a requirement can be implemented cleanly inside the documented local Python/FastAPI/SQLite architecture, implement it there.

## 17. Completion report for each execution slice

Report:

- what changed;
- files/components changed;
- acceptance tests and results;
- branch and exact commit SHA;
- relevant PR;
- unresolved blockers;
- exact next phase/task.

Never claim completion while required tests are failing or integration evidence is missing.

## 18. Current execution boundary

Until Phase 0 is merged, do not start scanner implementation.

After Phase 0 merges, begin **P1 — Repository/runtime foundation** from exact `main` unless a newer active phase issue/branch explicitly defines a narrower boundary.

Do not start P5 vulnerability-rule implementation before P4 controlled HTTP execution, scope enforcement and identity/session foundations exist and pass their safety gates.