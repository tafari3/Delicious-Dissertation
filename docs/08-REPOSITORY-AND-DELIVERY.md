# Repository Structure and Delivery Model

## 1. Objective

The repository is the execution contract shared between planning in ChatGPT and implementation on the AntiGravity VM. It must make the intended architecture, implementation order and acceptance state obvious from version-controlled files.

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
│   ├── 07-IMPLEMENTATION-ROADMAP.md
│   └── 08-REPOSITORY-AND-DELIVERY.md
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

The exact package names may be refined in P1, but the separation of concerns should remain.

## 3. Authoritative documents

When requirements conflict, use this precedence:

1. approved academic proposal;
2. `docs/00-PROJECT-CHARTER.md` for locked engineering scope;
3. `docs/06-SAFETY-SECURITY-MODEL.md` for safety constraints;
4. `docs/02-TEST-CATALOGUE.md` for rule semantics;
5. `docs/04-LABS-AND-EVALUATION.md` for research evaluation;
6. `docs/01-ARCHITECTURE.md` and `docs/05-DATA-AND-REPORTING.md` for design;
7. `docs/07-IMPLEMENTATION-ROADMAP.md` for implementation order;
8. `AGENTS.md` for agent execution procedure.

An implementation shortcut must not override a higher-level source of truth.

## 4. Branching model

Keep the workflow simple:

- `main` is the integrated, reproducible state;
- use one short-lived branch per coherent implementation phase/slice;
- open a PR back to `main`;
- do not create multiple competing branches for the same active slice;
- update the existing branch/PR when fixing findings from that slice.

Suggested branch format:

```text
phase-1/foundation
phase-2/labs
phase-3/inventory
phase-4/safe-executor
phase-5/authorisation-rules
...
```

## 5. Commit model

Commits should be understandable and scoped. Examples:

```text
feat: add target scope preflight
feat: implement BOLA cross-user read rule
test: add corrected-mode BOLA negative case
docs: record evaluation matching contract
fix: redact cookie values before persistence
```

Do not mix unrelated refactors with research-semantic changes in one commit.

## 6. Pull request contract

Every implementation PR should state:

- phase/slice being delivered;
- acceptance criteria;
- files/components changed;
- verification commands run;
- safety implications;
- research/evaluation implications;
- known limitations;
- exact head commit being reviewed when relevant.

A PR is not complete because code compiles. It is complete when the phase-specific acceptance gate is evidenced.

## 7. CI model

The initial CI workflow should run on pushes/PRs and eventually contain these gates as they become available:

```text
format check
lint
type check
unit tests
safety tests
integration tests
lab contract tests
report/schema tests
```

Do not make Docker-heavy evaluation runs mandatory on every trivial documentation PR if that creates unnecessary cost or fragility. Full cross-stack evaluation belongs in dedicated acceptance/evaluation workflows once implemented.

## 8. Stable local command surface

AntiGravity should expose stable high-level commands so implementation does not depend on remembering tool-specific invocations.

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

The implementation may use `uv`, `ruff`, `mypy`, `pytest`, Maven/Gradle and npm internally, but operators should have a small documented command surface.

## 9. Environment contract

The VM must not require repository secrets.

Commit:

- `.env.example` containing variable names and harmless examples;
- fixture credentials only when they are exclusively synthetic local-lab values and clearly designated as such, otherwise provide them at runtime;
- documented ports and service names.

Never commit real tokens, passwords, API keys, authorisation letters or real target credentials.

## 10. Generated output policy

Evaluation outputs, databases, reports and temporary evidence should go into ignored runtime/output paths unless a specific sanitised research artefact is intentionally committed.

Recommended ignored paths:

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

Final dissertation datasets committed to Git must first be checked for secret/personal-data absence.

## 11. Issue/epic model

After P0 is merged, create one issue/epic per implementation phase. Each issue contains:

- objective;
- dependencies;
- deliverables;
- acceptance checklist;
- verification commands;
- non-goals.

Do not pre-create hundreds of micro-issues. AntiGravity should work from the active phase issue and split only when a real independent dependency appears.

## 12. Definition of ready for an implementation phase

A phase is ready when:

- its preceding dependencies are merged/passing;
- relevant design docs are clear enough to implement without guessing research semantics;
- acceptance tests can be described before coding;
- no unresolved scope conflict exists.

## 13. Definition of done for an implementation phase

A phase is done when:

- implementation is complete for the stated slice;
- required automated tests exist and pass;
- safety requirements are satisfied;
- docs are updated if behaviour changed;
- CI passes at the PR head;
- the acceptance command/proof is reproducible;
- no placeholder claims are presented as working features.

## 14. AntiGravity handoff model

The VM should clone/pull the repository, read `AGENTS.md`, identify the active phase, inspect the authoritative documents relevant to that phase, implement on the existing phase branch, run verification, and push the exact tested state.

ChatGPT remains the planning/review control surface. GitHub remains the durable source of truth. AntiGravity is the execution environment.

The implementation must never depend on conversational context that is absent from the repository. If a decision matters to future execution, record it in Git.