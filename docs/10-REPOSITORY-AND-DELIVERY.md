# Repository Structure and Delivery Model

## 1. Objective

GitHub is the durable execution contract between academic/planning review and implementation on the AntiGravity VM. The repository must contain every decision needed to implement the project without relying on undocumented conversational context.

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
│   ├── 00A-ACADEMIC-PROPOSAL-BASELINE.md
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
│   ├── 12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md
│   ├── 13-LAB-EXPERIMENT-SPECIFICATION.md
│   └── 14-ANTIGRAVITY-HANDOFF.md
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
│   ├── citizen-records-fastapi/
│   ├── public-health-express/
│   └── permit-licensing-spring/
├── evaluation/
│   ├── profiles/
│   ├── schemas/
│   └── outputs/
├── scripts/
└── migrations/
```

P1 may refine package names but must preserve separation-of-concern boundaries unless a documented reason exists.

## 3. Authoritative documents

When requirements conflict, use the precedence defined in `AGENTS.md`. The academic proposal baseline, charter and safety/research-integrity contracts always outrank implementation convenience.

## 4. Branching model

Keep the workflow simple:

- `main` is the integrated reproducible state;
- use one short-lived branch per coherent phase/slice;
- open a PR back to `main`;
- do not create competing branches/PRs for the same active slice;
- fix review/CI/adversarial findings on the existing branch where practical.

Canonical implementation branch names:

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

Planning branches may exist only long enough to strengthen the source of truth before implementation; they are not parallel implementation branches.

## 5. Commit model

Commits should be understandable and scoped. Do not combine unrelated refactors with research-semantic or ground-truth changes.

Ground-truth, matcher, metric or lab-mode changes require especially explicit commit/PR descriptions because they can affect research validity.

## 6. Pull request contract

Every implementation PR should state:

- phase/slice;
- objective;
- acceptance criteria;
- files/components changed;
- verification commands/results;
- applicable adversarial attack IDs and results;
- safety implications;
- research/evaluation implications;
- known limitations/deferred lower-severity cases;
- exact head SHA under review.

A PR is complete only when the phase-specific acceptance gate and applicable CRITICAL/HIGH adversarial gates are evidenced on the exact head.

## 7. CI model

The initial CI workflow should add these gates as they become available:

```text
format check
lint
type check
unit tests
safety tests
adversarial tests
integration tests
lab contract tests
report/schema tests
secret scan
```

CI is part of the security boundary:

- third-party Actions use full commit-SHA pins;
- workflow permissions are explicitly least privilege;
- normal PR verification does not expose privileged secrets to PR-controlled code;
- avoid unsafe `pull_request_target` execution of untrusted PR code.

Do not require full Docker-heavy cross-stack evaluation for documentation-only changes. Full scanner/lab evaluation belongs in dedicated acceptance/evaluation workflows once implemented.

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

`make verify` should include all cheap/normal gates applicable to the current phase, including safety/adversarial tests once implemented. Dedicated heavier acceptance/evaluation commands may supplement it.

## 9. Environment contract

The VM must not require secrets committed to Git.

Commit harmless examples, service ports and secret reference names. Never commit real tokens, passwords, API keys, cookies/session material, production credentials, private keys, sensitive authorisation documents or real target dumps.

Ambient proxy environment must not silently reroute target-facing scanner traffic. Explicit proxy support is not an initial requirement.

Local/container execution is canonical. A ZCHPC deployment, if authorised later, is an optional deployment profile for the student's own labs and cannot become an undocumented completion dependency.

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

Final research datasets committed to Git must first pass secret/personal-data checks and contain synthetic/redacted information only.

## 11. Issue model

- maintain one issue per phase P1-P10;
- each issue identifies dependencies, deliverables, acceptance checklist, verification and non-goals;
- applicable adversarial attack IDs are part of the phase gate;
- create smaller issues only when a real independent slice/dependency appears;
- keep phase issues aligned with the current e-government scope and lab IDs.

Do not pre-create hundreds of speculative tasks.

## 12. Definition of ready

A phase is ready when:

- predecessor dependencies are merged/passing;
- relevant design documents are clear;
- the branch starts from the exact integrated predecessor commit;
- acceptance tests can be described before coding;
- applicable adversarial tests are identified;
- no unresolved academic-scope, safety or research-integrity conflict exists.

## 13. Definition of done

A phase is done when the stated implementation is complete, required automated tests pass, safety requirements hold, applicable CRITICAL/HIGH adversarial cases pass, documentation is updated, CI passes at the exact PR head, acceptance proof is reproducible, and no placeholder is represented as working functionality.

## 14. AntiGravity handoff model

The detailed no-context VM procedure is `docs/14-ANTIGRAVITY-HANDOFF.md`.

Conceptually:

```text
clone/fetch repository
  -> read academic baseline + AGENTS.md
  -> identify active phase issue/branch and exact handoff SHA
  -> read relevant docs + adversarial requirements
  -> inspect current implementation/tests
  -> implement smallest complete phase slice
  -> run canonical verification
  -> run phase-specific adversarial + runtime/lab proof
  -> commit/push exact tested state
  -> open/update phase PR
  -> integrate only when exact head is green
  -> begin next phase from integrated main
```

GitHub is the durable source of truth. If a decision matters to future execution, record it in Git rather than relying on chat memory.

## 15. Scope-change management

Do not silently reintroduce older proposal scope from Git history.

A change to research questions, current e-government-only evaluation, lab scenarios, ZCHPC boundary, fintech future-work status, metric definitions or CRITICAL/HIGH expected-safe behaviour requires an explicit reviewed change to the relevant authoritative documents and phase issues before code follows it.

## 16. Adversarial change management

The attack matrix may evolve when implementation reveals a genuinely new trust boundary. Add new adversarial cases when a feature creates a new attack surface.

Do not delete or weaken an existing expected-safe behaviour merely because it is difficult to implement. A change to a CRITICAL/HIGH expected-safe behaviour requires explicit reviewed justification and an equivalent or stronger control.
