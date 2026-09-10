# AntiGravity VM Handoff

## 1. Purpose

This is the no-chat-context execution handoff for the Linux VM already provided by ZCHPC. The repository is the source of truth.

## 2. Current execution boundary

Start at **P1 — Repository and runtime foundation** on the existing branch:

`phase-1/foundation`

Before the first implementation change:

1. fetch/prune;
2. check out `phase-1/foundation`;
3. read issue #2;
4. verify `git rev-parse HEAD` equals the exact handoff SHA recorded in issue #2;
5. verify that SHA is the reconciled integrated `main` commit;
6. stop and reconcile if either check fails.

Do not create a competing P1 branch.

## 3. First read order

Read:

1. `README.md`
2. `docs/00A-ACADEMIC-PROPOSAL-BASELINE.md`
3. `docs/00-PROJECT-CHARTER.md`
4. `AGENTS.md`
5. `docs/06-SAFETY-SECURITY-MODEL.md`
6. `docs/12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md`
7. `docs/11-RED-TEAM-ATTACK-MATRIX.md`
8. `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`
9. `docs/07-IMPLEMENTATION-PLAN.md`
10. active phase issue and relevant architecture/reporting/config documents.

## 4. Final project shape

The topic is unchanged: **Automated API Security Testing and Misconfiguration Scanner for Zimbabwean E-Government Systems: A Laboratory-Based Evaluation**.

The current dissertation does **not** require three labs.

- P2 builds one `government-permit-service-fastapi` synthetic lab on this Linux VM.
- P7 makes HTML/PDF/JSON/CSV automatic reporting a core feature.
- P9 proves scanner accuracy/repeatability against frozen lab ground truth and applicable ZAP.
- P10 performs later real-world validation against the actual ZCHPC cloud only within the existing signed authorisation and only after P9 passes.

Fintech/mobile-money/healthcare/additional government labs are future work.

## 5. VM assumptions

P1 may assume ordinary Linux development only. Establish or report prerequisites rather than assuming they exist:

- Git;
- Python 3.12+;
- preferred `uv` Python workflow unless blocked;
- Docker Engine + Compose v2 for the lab where permitted;
- standard build tools required by locked dependencies.

Do not add Node/Java lab runtimes: the former three-stack model is superseded by the single FastAPI research lab.

## 6. Phase loop

For each phase:

1. verify predecessor is merged and current branch starts from integrated `main`;
2. read phase issue and applicable source-of-truth docs;
3. identify acceptance/adversarial gates before coding;
4. implement the smallest complete slice;
5. add positive, corrected/negative, safety and adversarial tests;
6. run `make verify` plus phase-specific integration/evaluation proof;
7. fix failures without weakening expected behaviour;
8. update docs/config when external behaviour changes;
9. commit/push exact tested state;
10. open/update the one phase PR;
11. merge only when exact head is green and phase definition of done is satisfied;
12. start the next phase from new integrated `main`.

## 7. P1 objective

P1 establishes installable scanner/application foundations only: Python package, FastAPI health, Typer CLI, SQLAlchemy/migrations/SQLite, safe logging, tests/lint/typecheck, Makefile, Compose skeleton, CI/supply-chain hardening, secret scanning and documented future controlled HTTP client contract.

Do not implement the lab or detector rules prematurely.

## 8. P2 boundary

After P1 merges, build only:

`labs/government-permit-service-fastapi/`

with the roles, operations, seeded cases, vulnerable/corrected modes, deterministic reset, OpenAPI and ground truth in `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`.

Scanner output never establishes ground truth.

## 9. P7 reporting boundary

A reportable scan must generate HTML and PDF human-readable reports plus JSON and CSV machine-readable outputs. Report generation must use redacted/minimised durable findings and must not expose secrets or active target-controlled content.

## 10. P9 research gate

P9 completes controlled quantitative evaluation. Freeze methodology inputs before final collection and retain all runs with validity reasons. Do not proceed to ZCHPC operational validation while P9 safety/research-integrity gates are failing.

## 11. P10 ZCHPC boundary

P10 uses a local, non-committed `authorised-zchpc` profile reflecting the signed scope. Real hosts/IPs/credentials/authorisation documents/confidential operational data do not belong in Git.

Operational scanning is non-destructive by default. Lab mutation permissions do not transfer. Do not seed vulnerabilities into ZCHPC, access unrelated tenants/assets, attempt VM escape/hypervisor exploitation, DoS/stress, persistence, lateral movement or destructive fuzzing.

If the signed operational scope is ambiguous for a requested action, stop that action and require scope clarification instead of guessing.

## 12. Completion report

At the end of every slice report:

```text
Phase/slice:
Branch:
Head SHA:
PR:
Implemented:
Verification commands/results:
Adversarial IDs/results:
Safety/research notes:
Deferred lower-severity cases:
Blockers:
Exact next task:
```

Never claim completion while mandatory checks, runtime/lab proof or exact-head evidence are missing.
