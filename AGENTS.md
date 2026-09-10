# AGENTS.md — AntiGravity Execution Contract

## 1. Purpose

This file is the mandatory execution contract for AntiGravity and any other coding agent working in this repository. Decisions required for implementation must come from Git, not prior chat history.

## 2. Source-of-truth precedence

Use this order when instructions conflict:

1. `docs/00A-ACADEMIC-PROPOSAL-BASELINE.md`
2. `docs/00-PROJECT-CHARTER.md`
3. `docs/06-SAFETY-SECURITY-MODEL.md`
4. `docs/12-PRE-IMPLEMENTATION-HARDENING-LOCKS.md`
5. `docs/11-RED-TEAM-ATTACK-MATRIX.md`
6. `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`
7. `docs/02-TEST-CATALOGUE.md`
8. `docs/04-LABS-AND-EVALUATION.md`
9. `docs/01-ARCHITECTURE.md`
10. `docs/05-DATA-AND-REPORTING.md`
11. `docs/03-USER-JOURNEYS.md`
12. `docs/08-REQUIREMENTS-TRACEABILITY.md`
13. `docs/09-CONFIGURATION-DEFAULTS.md`
14. `docs/07-IMPLEMENTATION-PLAN.md`
15. `docs/10-REPOSITORY-AND-DELIVERY.md`
16. `docs/14-ANTIGRAVITY-HANDOFF.md`
17. implementation code/tests.

## 3. Locked mission

Build an automated REST API security testing and misconfiguration scanner for Zimbabwean e-government systems. The scanner must safely identify selected weaknesses and automatically generate reproducible, redacted security assessment reports.

Do not change the dissertation topic into a ZCHPC cloud scanner. ZCHPC is the later authorised real-world validation environment.

## 4. Evaluation model

### Stage A — controlled laboratory

Build one dissertation-specific lab on the ZCHPC-provided Linux VM:

`government-permit-service-fastapi`

It must use synthetic users/data only, vulnerable and corrected modes, deterministic reset, controlled roles and independent machine-readable ground truth.

### Stage B — authorised ZCHPC validation

Only after the P9 controlled-lab gate passes, P10 may use the scanner within the exact signed ZCHPC authorisation boundary. Operational scope must be represented by explicit local configuration and non-secret authorisation-reference metadata.

Never deliberately weaken the operational ZCHPC environment to create findings. Do not access unrelated tenants/assets or exceed approved interfaces, identities, traffic levels or time windows.

## 5. Mandatory safety invariants

1. No scan without explicit allow-listed scope.
2. Revalidate effective target/destination on every request and redirect.
3. All target traffic uses one controlled HTTP executor.
4. Hard request/rate/concurrency budgets are always present.
5. Resource-control tests use a stricter sub-budget.
6. Default profile is non-destructive.
7. Mutation tests run only on disposable synthetic lab fixtures unless a specific operational action is explicitly authorised.
8. Stop at proof-of-condition; never escalate for impact.
9. Redact credentials, tokens, cookies, API keys and configured sensitive values before persistence/export.
10. Never log resolved secrets.
11. No credential stuffing, password spraying, destructive/unrestricted fuzzing, denial-of-service, VM escape, persistence or lateral movement.
12. Imported specifications cannot expand approved scope.
13. Ambient proxy environment must not silently reroute target traffic.
14. Ground truth is invisible to ordinary scanner detection logic.
15. Operational ZCHPC evidence must be minimised and must not publish confidential infrastructure details without permission.

## 6. Implementation discipline

- Follow `docs/07-IMPLEMENTATION-PLAN.md` sequentially.
- Use the current phase issue and its exact branch/SHA.
- Do not create duplicate phase branches or PRs.
- Prefer small typed modules and deterministic behaviour.
- Rule modules may not create unrestricted HTTP clients.
- Never convert `ERROR` or `INCONCLUSIVE` into a pass.
- Do not confirm vulnerabilities from HTTP status alone.
- Do not alter lab ground truth after seeing scanner results to improve metrics.
- Do not add a second/third academic lab unless the academic baseline is explicitly amended.

## 7. Rule states

Use exactly:

`NOT_APPLICABLE`, `PASS_OBSERVED`, `CONFIRMED`, `SUSPECTED`, `INFORMATIONAL`, `INCONCLUSIVE`, `ERROR`.

Severity and confidence are separate fields.

## 8. Reporting contract

Automatic reporting is a core feature. P7/P8 must provide:

- HTML report;
- PDF report;
- canonical JSON report;
- CSV research/export data;
- findings with endpoint/service, severity, confidence, expected-versus-observed behaviour, minimal redacted evidence, OWASP/CWE mapping and remediation guidance;
- explicit limitations/inconclusive/error sections;
- provenance including scanner commit, rule version, target/profile/spec hashes where applicable and request/timing data.

## 9. Controlled lab contract

The canonical academic lab is `government-permit-service-fastapi`, implemented with FastAPI and a small relational database unless a concrete blocker is documented.

Minimum roles: `applicant-a`, `applicant-b`, `officer`, `admin`.

The lab must provide vulnerable/corrected states, synthetic fixtures, OpenAPI, deterministic seed/reset, direct functional tests and a versioned ground-truth manifest.

## 10. Research integrity

Keep three layers separate:

```text
LAB + DIRECT CONTRACT TESTS -> establish actual seeded behaviour
SCANNER                    -> produces findings without ground truth
EVALUATION HARNESS          -> compares findings with frozen ground truth
```

P9 freezes the lab ground truth, matcher, metric formulas/state treatment, scanner profile and ZAP baseline before final controlled data collection.

P10 analyses ZCHPC validation separately because complete operational ground truth may not exist.

## 11. Git/CI discipline

- Work on the current intended branch, not directly on `main`.
- `make verify` is the canonical local/CI gate once P1 creates it.
- Third-party Actions use full commit SHAs.
- Workflows use least privilege.
- Ordinary PR verification receives no privileged secrets.
- No real credentials, signed authorisation documents, real target dumps or confidential ZCHPC evidence may be committed.

## 12. Current execution boundary

Planning is reconciled. Begin **P1 only** after verifying `phase-1/foundation` equals the exact handoff SHA recorded in issue #2.

P2 may not start before P1 merges. P5 may not start before P4 safe execution is proven. P10 ZCHPC validation may not start before P9 controlled-lab validation has passed its safety and research-integrity gate.

At the end of each slice report: phase, branch, exact head SHA, PR, implemented work, verification commands/results, adversarial IDs/results, safety/research notes, blockers and exact next task.
