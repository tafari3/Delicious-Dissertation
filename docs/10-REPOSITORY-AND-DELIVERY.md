# Repository Structure and Delivery Model

## 1. Objective

GitHub is the durable execution contract between planning/review in ChatGPT and implementation on the AntiGravity VM. The repository must contain every decision that AntiGravity needs to implement the project without relying on undocumented conversational context.

## 2. Target repository layout

```text
Delicious-Dissertation/
├── README.md
├── AGENTS.md
├── pyproject.toml
├── Makefile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── .github/
│   └── workflows/
│       └── verify.yml
├── docs/
│   ├── 00-PROJECT-CHARTER.md
│   ├── 01-ARCHITECTURE.md
│   ├── 02-TEST-CATALOGUE.md
│   ├── 03-USER-JOURNEYS.md
│   ├── 04-LABS-AND-EVALUATION.md
│   ├── 05-DATA-AND-REPORTING.md
│   ├── 06-SAFETY-SECURITY-MODEL.md
│   ├── 07-IMPLEMENTATION-PLAN.md
│   ├── 08-REQUIREMENTS-TRACEABILITY.md
│   ├── 09-CONFIGURATION-DEFAULTS.md
│   ├── 10-REPOSITORY-AND-DELIVERY.md
│   ├── 11-RED-TEAM-ATTACK-MATRIX.md
│   └── 12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md
├── src/
│   └── delicious_scanner/
│       ├── app/
│       ├── cli/
│       ├── config/
│       ├── domain/
│       ├── inventory/
│       ├── identities/
│       ├── execution/
│       ├── rules/
│       │   ├── authorisation/
│       │   ├── authentication/
│       │   ├── configuration/
│       │   ├── inventory/
│       │   └── resource_control/
│       ├── evidence/
│       ├── reporting/
│       ├── persistence/
│       └── evaluation/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── safety/
│   ├── red_team/
│   └── acceptance/
├── labs/
│   ├── mobile-money-fastapi/
│   ├── revenue-express/
│   └── citizen-services-spring/
├── evaluation/
│   ├── profiles/
│   ├── schemas/
│   └── outputs/
├── scripts/
└── migrations/
```

P1 may refine package names, but must preserve these separation-of-concern boundaries unless a documented reason exists.

## 3. Authoritative documents

When requirements conflict, use this precedence:

1. approved academic proposal;
2. `docs/00-PROJECT-CHARTER.md` — locked engineering/research scope;
3. `docs/06-SAFETY-SECURITY-MODEL.md` — hard safety constraints;
4. `docs/12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md` — mandatory controls produced by adversarial review;
5. `docs/11-RED-TEAM-ATTACK-MATRIX.md` — adversarial acceptance catalogue;
6. `docs/02-TEST-CATALOGUE.md` — scanner rule semantics;
7. `docs/04-LABS-AND-EVALUATION.md` — research evaluation methodology;
8. `docs/01-ARCHITECTURE.md` and `docs/05-DATA-AND-REPORTING.md` — system/data design;
9. `docs/03-USER-JOURNEYS.md` — operator behaviour;
10. `docs/09-CONFIGURATION-DEFAULTS.md` — initial operational defaults;
11. `docs/07-IMPLEMENTATION-PLAN.md` — implementation order/phase gates;
12. `docs/08-REQUIREMENTS-TRACEABILITY.md` — proposal mapping;
13. `AGENTS.md` — agent execution procedure.

An implementation shortcut must not override a higher-level source of truth.

## 4. Branching model

Keep the workflow simple:

- `main` is the integrated reproducible state;
- use one short-lived branch per coherent phase/slice;
- open a PR back to `main`;
- do not create competing branches/PRs for the same active slice;
- fix review/CI/red-team findings on the existing branch where practical.

Suggested branch names:

```text
phase-1/foundation
phase-2/labs-ground-truth
phase-3/spec-inventory
phase-4/safe-execution
phase-5/authorisation
phase-6/remaining-rules
phase-7/reporting
phase-8/operator-ui
phase-9/evaluation
phase-10/final-validation
```

Planning/red-team branches may exist only long enough to strengthen the source of truth before implementation; they are not parallel product implementation branches.

## 5. Commit model

Commits should be understandable and scoped. Do not combine unrelated refactors with research-semantic or ground-truth changes.

## 6. Pull request contract

Every implementation PR should state:

- phase/slice;
- objective;
- acceptance criteria;
- files/components changed;
- verification commands/results;
- applicable red-team attack IDs and results;
- safety implications;
- research/evaluation implications;
- known limitations/deferred lower-severity cases;
- exact head under review when relevant.

A PR is complete only when the phase-specific acceptance gate and applicable CRITICAL/HIGH red-team gates are evidenced.

## 7. CI model

The initial CI workflow should add these gates as they become available:

```text
format check
lint
type check
unit tests
safety tests
red-team tests
integration tests
lab contract tests
report/schema tests
secret scan
```

CI itself is part of the security boundary:

- third-party actions use full commit-SHA pins;
- workflow permissions are explicitly least privilege;
- normal PR verification does not expose privileged secrets to PR-controlled code;
- avoid unsafe execution of untrusted code via privileged `pull_request_target` patterns.

Do not require full Docker-heavy cross-stack evaluation for every documentation-only change. Full scanner/lab evaluation belongs in dedicated acceptance/evaluation workflows once implemented.

## 8. Stable local command surface

Preferred contract:

```text
make bootstrap
make format
make lint
make typecheck
make test
make verify
make app
make labs-up
make labs-down
make labs-reset
make evaluate
```

`make verify` should include all cheap/normal gates applicable to the current phase, including safety/red-team tests once implemented. Dedicated heavier acceptance/evaluation commands may supplement it.

The implementation may use `uv`, Ruff, mypy/pyright, pytest, npm, Maven/Gradle and Docker internally.

## 9. Environment contract

The VM must not require secrets committed to Git.

Commit harmless examples, service ports and secret reference names. Never commit real tokens, passwords, API keys, cookies/session material, production credentials, private keys, sensitive authorisation documents or real target dumps.

Ambient proxy environment must not silently reroute target-facing scanner traffic. Explicit proxy support is not an initial requirement.

## 10. Generated output policy

Runtime databases, reports and evaluation outputs should be ignored unless a specific sanitised research artefact is intentionally committed.

Recommended ignored paths/patterns:

```text
.env
*.db
.data/
reports/
evaluation/outputs/runtime/
coverage/
.pytest_cache/
__pycache__/
```

Final research datasets committed to Git must first pass secret/personal-data checks.

## 11. Issue model

After P0 merge:

- create one parent implementation tracker where useful;
- create one issue each for P1–P10;
- include objective, dependencies, deliverables, acceptance checklist, verification and non-goals;
- add applicable red-team attack IDs/gates to the phase issue;
- create smaller issues only when a real independent slice/dependency appears.

Do not pre-create hundreds of micro-issues.

## 12. Definition of ready

A phase is ready when preceding dependencies are merged/passing, relevant design docs are clear, acceptance tests can be described before coding, applicable adversarial tests are identified, and no unresolved scope/safety conflict exists.

## 13. Definition of done

A phase is done when the stated implementation is complete, required automated tests pass, safety requirements hold, applicable CRITICAL/HIGH red-team cases pass, documentation is updated, CI passes at the exact PR head, acceptance proof is reproducible, and no placeholder is represented as working functionality.

## 14. AntiGravity handoff model

```text
clone/pull repository
  -> read AGENTS.md
  -> identify active phase issue/branch
  -> read relevant authoritative docs
  -> read relevant red-team attack/hardening requirements
  -> inspect current implementation/tests
  -> implement the smallest complete slice
  -> run canonical verification
  -> run phase-specific adversarial + runtime/lab proof
  -> commit/push exact tested state
  -> report what changed, proof, blocker and next task
```

ChatGPT is the planning/review control surface. GitHub is the durable source of truth. AntiGravity is the execution environment.

If a decision matters to future execution, record it in Git rather than relying on chat memory.

## 15. Red-team change management

The attack matrix is expected to evolve when implementation reveals a genuinely new attack surface. Add new adversarial cases when a new feature creates a new trust boundary.

Do not delete or weaken an existing expected-safe behaviour simply because it is difficult to implement. A change to a CRITICAL/HIGH expected-safe behaviour requires explicit reviewed justification and an equivalent or stronger control.