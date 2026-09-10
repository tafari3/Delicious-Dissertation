# Repository Structure and Delivery Model

## 1. Objective

GitHub is the durable implementation contract between proposal review and AntiGravity on the ZCHPC-provided Linux VM.

## 2. Target repository layout

```text
Delicious-Dissertation/
├── README.md
├── AGENTS.md
├── pyproject.toml
├── Makefile
├── docker-compose.yml
├── docs/
├── src/delicious_scanner/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── safety/
│   ├── red_team/
│   └── acceptance/
├── labs/
│   └── government-permit-service-fastapi/
│       └── ground-truth/
├── evaluation/
│   ├── profiles/
│   ├── schemas/
│   ├── analysis/
│   └── outputs/
├── reports/              # runtime/ignored
├── migrations/
├── scripts/
└── .github/workflows/
```

Do not commit local ZCHPC target details, credentials, signed authorisation documents or confidential operational reports.

## 3. Branch model

`main` is integrated reproducible state. Use one coherent branch/PR per phase or genuine slice.

Canonical phase names:

```text
phase-1/foundation
phase-2/lab-ground-truth
phase-3/spec-inventory
phase-4/safe-execution
phase-5/authorisation
phase-6/remaining-rules
phase-7/reporting
phase-8/operator-ui
phase-9/evaluation
phase-10/zchpc-validation
```

## 4. PR contract

Every implementation PR records phase/slice, objective, acceptance criteria, files/components changed, commands/results, applicable adversarial IDs, safety/research implications, exact head SHA and remaining lower-severity deferrals.

A phase is not done until the exact head passes its required gates.

## 5. CI and command surface

CI grows with phases and includes format/lint/type/unit/safety/adversarial/integration/lab/report/schema/secret checks as applicable.

Third-party Actions use full SHA pins; workflow permissions are least privilege; normal PR verification receives no privileged secrets.

Preferred local commands:

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

## 6. Generated output policy

Ignore ordinary runtime DBs, reports and evaluation outputs. Commit only intentionally sanitised research artefacts after secret/personal/confidential-data checks.

Recommended ignored paths include `.env`, `*.db`, `.data/`, `reports/`, `evaluation/outputs/runtime/`, `.local/zchpc/`, caches and coverage output.

## 7. ZCHPC operational delivery rule

P10 operational profiles/configuration live outside Git. Repository code may define schemas and safe examples, but not real hosts, IPs, credentials, tokens, confidential tenant/resource names or signed documents.

A sanitised P10 summary may be committed only after confirming it contains no protected infrastructure detail.

## 8. Scope-change management

A change to topic, one-lab model, ZCHPC validation boundary, research questions, metric semantics or CRITICAL/HIGH expected-safe behaviour requires a reviewed source-of-truth change before implementation follows it.

Do not reintroduce the former three-lab implementation model from Git history.
