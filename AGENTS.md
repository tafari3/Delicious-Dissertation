# AGENTS.md — AntiGravity Execution Contract

## 1. Purpose

This file is the execution contract for AI coding agents working in this repository, including AntiGravity on the implementation VM.

Read this file and the authoritative documents under `docs/` before modifying code.

## 2. Source-of-truth precedence

When instructions conflict, use this order:

1. the approved academic proposal and its explicit research/safety boundaries;
2. `docs/00-PROJECT-CHARTER.md`;
3. `docs/02-TEST-CATALOGUE.md` for scanner rule semantics;
4. `docs/01-ARCHITECTURE.md`;
5. `docs/04-LABS-AND-EVALUATION.md` for experimental methodology;
6. `docs/05-DATA-AND-REPORTING.md`;
7. `docs/03-USER-JOURNEYS.md`;
8. `docs/06-IMPLEMENTATION-PLAN.md`;
9. implementation code/tests.

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

Follow `docs/06-IMPLEMENTATION-PLAN.md` sequentially unless an issue/PR explicitly states a narrower current phase.

At the start of work:

1. inspect repository status and current branch;
2. pull/fetch the intended branch safely;
3. read the current phase issue/requirements;
4. inspect existing implementation/tests before changing anything;
5. run the canonical verification command if the repository is already bootstrapped.

Do not create a parallel architecture or duplicate subsystem when one already exists.

## 6. Implementation discipline

### Prefer

- small modules with explicit contracts;
- typed domain models;
- deterministic behaviour;
- pure comparison/classification functions where possible;
- central safety enforcement;
- unit tests plus seeded-lab integration tests;
- versioned rule identifiers;
- structured machine-readable outputs;
- minimal dependencies.

### Avoid

- clever implicit magic;
- hidden global state;
- network calls in model constructors;
- raw HTTP clients inside rule modules;
- swallowing exceptions and returning clean/pass states;
- status-code-only vulnerability decisions;
- storing full raw responses when a small proof excerpt is sufficient;
- target-language-specific scanner logic;
- arbitrary shell execution from scan definitions;
- executing Postman scripts supplied by targets;
- overengineering.

## 7. Dependency policy

Before adding a dependency:

- confirm standard library/current dependency cannot reasonably do the job;
- choose mature, maintained packages;
- pin through the selected lockfile mechanism;
- avoid dependencies that require cloud accounts or recurring services;
- document important security-sensitive dependencies.

No LLM/API dependency is required for the scanner.

## 8. Secret policy

Secrets may enter the runtime through supported local secret references, initially environment variables or ignored local secret files.

Never commit:

- `.env` with real values;
- tokens;
- passwords;
- cookies;
- API keys;
- private certificates/keys;
- real target dumps;
- scanner evidence containing unresolved secret material.

Use synthetic fixture secrets for tests and ensure they are visibly non-production.

## 9. Rule implementation contract

Before implementing a scanner rule, read its entry in `docs/02-TEST-CATALOGUE.md`.

Every rule PR/change must include:

- stable rule ID/version;
- applicability tests;
- proof-condition tests;
- corrected/non-vulnerable negative tests;
- request-budget test;
- evidence-redaction test;
- integration proof against a corresponding vulnerable lab case;
- integration proof against corrected behaviour where the lab case exists.

Do not mark a rule complete using only mocks if the corresponding lab exists.

## 10. Classification discipline

Use the defined result semantics:

- `NOT_APPLICABLE`
- `PASS_OBSERVED`
- `CONFIRMED`
- `SUSPECTED`
- `INFORMATIONAL`
- `INCONCLUSIVE`
- `ERROR`

Never convert `ERROR`/`INCONCLUSIVE` into a pass.

Never classify a finding as `CONFIRMED` solely because an endpoint returned HTTP 2xx.

Severity and confidence are separate fields.

## 11. Laboratory discipline

Ground truth must remain independent of scanner detection logic.

The scanner must not import the ground-truth manifest during ordinary detection.

For each lab change:

- vulnerable mode direct functional test proves the seeded weakness;
- corrected mode direct functional test proves the fix;
- reset remains deterministic;
- synthetic data only;
- API description stays aligned except where an intentional inventory mismatch is itself the seeded case.

## 12. Data/evidence discipline

Persist structured, minimized, redacted evidence.

Before saving/exporting any observation:

1. remove sensitive headers;
2. redact sensitive body fields;
3. redact any runtime-known secret values;
4. truncate to configured evidence size;
5. record whether truncation occurred.

Do not persist raw unredacted exchanges “temporarily”.

## 13. Canonical verification

Once P1 establishes the task surface, `make verify` (or the repository-documented canonical equivalent) is the required local and CI gate.

It should cover at minimum:

- formatting check;
- lint;
- type/static checks where configured;
- unit tests;
- appropriate integration tests for the changed scope.

For lab/rule changes, run the relevant targeted lab integration proof in addition to generic verification when it is not already included.

## 14. Git/PR discipline

- Work on the current intended feature/phase branch, not directly on `main`, unless explicitly performing repository bootstrap.
- Keep changes scoped to the current issue/phase.
- Do not create duplicate branches/PRs for the same work.
- Do not rewrite unrelated code just for style.
- Do not commit generated secrets/results.
- Before requesting/performing merge, verify the exact branch head.
- Resolve real CI/review failures on the same PR where practical.
- Do not treat a stale successful run from an earlier head as proof for a changed head.

## 15. Documentation rule

Update documentation when a change alters:

- public CLI/UI workflow;
- rule semantics;
- architecture boundaries;
- evidence/report schema;
- lab ground truth;
- evaluation methodology;
- setup/verification commands.

Do not change research questions, core scope or prohibited capabilities through a casual documentation edit.

## 16. Anti-overengineering check

Do not introduce Kubernetes, microservices, queues, distributed workers, external DB infrastructure, SPA frontend, multi-tenancy, enterprise SSO/RBAC, LLM services or cloud deployment as default architecture.

If a current requirement can be implemented cleanly inside the documented local Python/FastAPI/SQLite architecture, implement it there.

## 17. Completion report for each execution slice

When an execution slice is complete, report concisely:

- what changed;
- files/components changed;
- acceptance tests run and result;
- relevant commit/branch/PR;
- any unresolved blocker;
- exact next phase/task.

Do not claim completion when tests are failing or required integration evidence is missing.

## 18. Current execution boundary

Until P0 is merged, do not start scanner implementation.

After P0 is merged, begin **P1 — Repository and runtime foundation** from `docs/06-IMPLEMENTATION-PLAN.md`, then continue sequentially through the phase gates.
