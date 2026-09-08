# AntiGravity VM Handoff

## 1. Purpose

This is the no-chat-context handoff for implementing the dissertation on the AntiGravity-connected VM. An implementation agent should be able to start from this repository alone, identify the active phase, implement it, prove it and continue through the documented roadmap without depending on undocumented conversation history.

## 2. Current boundary

The repository is intentionally planning-first. Product implementation starts at:

**P1 — Repository and runtime foundation**

Canonical active branch:

```text
phase-1/foundation
```

Canonical active issue:

```text
#2 — P1 — Repository and runtime foundation
```

Before the first implementation change, compare the branch head to the exact handoff SHA recorded in issue #2. If they differ, stop and reconcile rather than implementing from a stale branch.

## 3. First boot sequence

On the VM:

```bash
git clone https://github.com/tafari3/Delicious-Dissertation.git
cd Delicious-Dissertation
git fetch --all --prune
git checkout phase-1/foundation
git status
git rev-parse HEAD
```

Then read, in order:

```text
README.md
docs/00A-ACADEMIC-PROPOSAL-BASELINE.md
docs/00-PROJECT-CHARTER.md
AGENTS.md
docs/06-SAFETY-SECURITY-MODEL.md
docs/12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md
docs/11-RED-TEAM-ATTACK-MATRIX.md
docs/13-LAB-EXPERIMENT-SPECIFICATION.md
docs/07-IMPLEMENTATION-PLAN.md
active GitHub phase issue
```

Read the additional architecture/data/journey/config documents relevant to the active phase before coding.

## 4. VM/system assumptions

Do not assume a special proprietary runtime beyond the normal development tools that the active phase establishes or documents.

P1 should leave the repository able to report missing system prerequisites clearly. The intended local tooling includes:

- Git;
- Python 3.12+;
- `uv` as the preferred Python dependency workflow unless a documented blocker requires another approach;
- Docker Engine and Docker Compose v2 for later laboratory phases;
- standard build tools required by locked dependencies.

Node.js and Java build/runtime dependencies are introduced and pinned in P2 when their laboratories become active. Do not make P1 unnecessarily install or implement the laboratory applications.

## 5. No-chat-context rule

If a decision matters to implementation, it must exist in GitHub documentation, an issue, a PR or code/tests. Do not guess from the repository name, stale Git history, prior chat assumptions or an older proposal.

The current academic baseline is e-government only:

- Citizen Records laboratory;
- Public Health Records laboratory;
- Permit & Licensing laboratory;
- synthetic data only;
- fintech future work only;
- optional authorised ZCHPC hosting of the student's own laboratory only.

## 6. Phase execution loop

For each phase P1 through P10:

1. Verify all predecessor phases are merged and passing.
2. Read the phase issue and authoritative documents.
3. Identify the exact acceptance criteria and applicable CRITICAL/HIGH adversarial cases before coding.
4. Create/use only the canonical branch for that phase; do not create competing duplicate branches.
5. Inspect existing code/tests and implement the smallest complete slice consistent with the architecture.
6. Add positive, corrected/negative, safety and adversarial tests required by the phase.
7. Run the canonical verification gate and phase-specific integration/evaluation checks.
8. Fix failures on the same branch; do not weaken expected behaviour to make tests pass.
9. Update docs/config examples when implementation changes an externally relevant contract.
10. Commit/push the exact tested state.
11. Open or update the single phase PR with objective, evidence, tests, exact head SHA and unresolved lower-severity deferrals.
12. Merge only when the exact head is green and the phase definition of done is satisfied, if the VM identity has permission to merge. If merge permission is unavailable, leave the PR ready and report that single external blocker rather than starting the next phase from an unmerged state.
13. Start the next phase from the new integrated `main`, never from an unmerged or stale predecessor branch.

## 7. P1 exact objective

P1 creates the installable, reproducible development/runtime foundation only. It does **not** implement security detection rules or laboratories.

Required P1 outputs include:

- `pyproject.toml`;
- reproducible Python lockfile;
- `src/delicious_scanner/` package;
- FastAPI application with `/health`;
- Typer CLI with version/health functionality;
- SQLAlchemy 2.x + migration framework + SQLite baseline;
- structured secret-safe logging baseline;
- pytest;
- Ruff formatting/linting;
- mypy or pyright;
- root Docker Compose skeleton;
- `.env.example` and `.gitignore`;
- `.github/workflows/verify.yml`;
- stable Makefile command surface;
- SHA-pinned third-party Actions;
- least-privilege workflow permissions;
- PR-safe verification without privileged secrets;
- repository secret-scanning gate;
- terminal/control-sequence sanitisation baseline;
- documented future HTTP-client contract with ambient proxy environment disabled by default.

Required command surface after P1:

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
```

`make verify` is the local and CI gate for normal phase verification once established.

## 8. P2 boundary

Only after P1 is merged:

- build `citizen-records-fastapi`;
- build `public-health-express`;
- build `permit-licensing-spring`;
- implement deterministic seed/reset and vulnerable/corrected modes;
- create machine-readable ground-truth manifests from `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`;
- prove ground truth with direct lab tests independent of scanner detection logic.

Do not use scanner output to decide what the lab ground truth should say.

## 9. Safety stop conditions for the implementation agent

Stop the current change and surface a blocker when:

- a request would weaken target allow-listing or request ceilings;
- a proposed feature requires real government/ZCHPC production scanning;
- a test requires real personal/health/financial data;
- a dependency introduces an unnecessary cloud/LLM/remote service requirement;
- a phase would bypass a predecessor safety layer;
- CRITICAL/HIGH adversarial tests fail;
- ground truth would need to be changed merely because scanner results are inconvenient;
- an unreviewed change would alter research questions, lab scenarios, metric formulas or dissertation scope.

## 10. Research-integrity rule

Keep three layers distinct:

```text
LAB SERVICE + DIRECT CONTRACT TESTS
        -> define actual seeded behaviour

SCANNER
        -> produces findings without reading ground truth

EVALUATION HARNESS
        -> after scan, reads findings + frozen ground truth and computes matches/metrics
```

Detector code must not import/read ground-truth manifests. Evaluation matching must be deterministic and versioned.

## 11. Definition of autonomous success

The repository is ready for autonomous execution when an agent can:

- clone from a clean VM;
- identify current phase and exact starting commit;
- implement without asking for missing product-scope decisions already covered by the docs;
- run deterministic verification;
- prove phase-specific safety/adversarial requirements;
- create a reviewable PR with exact evidence;
- continue sequentially after integration without relying on chat memory.

Human/supervisor input is still required for genuine academic scope changes, ethics/authorisation decisions, or external permissions such as access to a ZCHPC resource. These are not implementation ambiguities to be guessed by an agent.

## 12. Completion report format

At the end of every execution slice, report:

```text
Phase/slice:
Branch:
Head SHA:
PR:
Implemented:
Files/components changed:
Verification commands:
Verification results:
Adversarial IDs proven:
Safety/research-integrity notes:
Deferred MEDIUM/LOW cases with rationale:
Blockers:
Exact next task:
```

Never report a phase complete while mandatory checks are failing, required runtime/lab integration evidence is missing, or the exact tested commit is not identified.
