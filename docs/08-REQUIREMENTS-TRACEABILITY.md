# Proposal-to-Implementation Traceability

## 1. Purpose

Map the final proposal directly to engineering and evidence. `docs/00A-ACADEMIC-PROPOSAL-BASELINE.md` is the academic implementation baseline.

## 2. Technical-objective traceability

| Final proposal objective | Engineering location | Required proof |
|---|---|---|
| 1. Modular REST API scanner with allow-listing, request limits and secret redaction | P1/P4, architecture, safety model | hard preflight, controlled executor, budget and redaction tests |
| 2. Selected OWASP-aligned BOLA/BFLA/BOPLA, auth/session, misconfiguration and inventory checks | `docs/02-TEST-CATALOGUE.md`, P5/P6 | positive/corrected lab integration and semantic adversarial tests |
| 3. Synthetic Government Permit and Service Application API on the ZCHPC-provided Linux VM | P2, `labs/government-permit-service-fastapi/`, `docs/13-*` | deterministic synthetic fixtures, vulnerable/corrected modes, direct tests and frozen ground truth |
| 4. Automatic HTML/PDF + JSON/CSV reports | P7/P8, reporting layer | schema-valid exports with redacted evidence, severity, OWASP/CWE and remediation |
| 5. Ground-truth/ZAP evaluation then authorised ZCHPC validation | P9/P10 | controlled accuracy dataset plus separate authorised operational validation record |

## 3. Research-question traceability

### RQ1 — reliably detectable selected weaknesses in the controlled lab

Evidence: rule applicability/state counts, seeded positive/corrected cases, errors/inconclusive outcomes and category coverage in `government-permit-service-fastapi`.

### RQ2 — accuracy against independent ground truth and applicable ZAP

Evidence: deterministic TP/FP/FN/(defensible TN), precision, recall, F1 and applicability-aware ZAP comparison from P9.

### RQ3 — consistency and actionability of reports

Evidence: repeated HTML/PDF/JSON/CSV generation, stable finding fingerprints, evidence/provenance consistency, report schema validation and examiner review of remediation content.

### RQ4 — applicability/repeatability in the authorised ZCHPC cloud scope

Evidence: P10 preflight/scope proof, safe operational runs, applicability by rule family, repeated observations where permitted, redacted report quality and documented operational limitations.

ZCHPC does not automatically provide complete ground truth; P10 evidence therefore does not manufacture recall/FN/FPR claims without an independent denominator.

## 4. Controlled-lab traceability

| Commitment | Engineering contract |
|---|---|
| one academic lab | `government-permit-service-fastapi` |
| representative e-government workflow | synthetic permit/service application, not a named ministry replica |
| controlled identities | `applicant-a`, `applicant-b`, `officer`, `admin` |
| vulnerable/corrected states | deterministic mode switch/build profile with paired direct tests |
| independent ground truth | versioned manifest read only by evaluation layer |
| synthetic data only | fixture review/tests; no production dependencies |
| report generation | every reportable scan can export HTML/PDF/JSON/CSV |

## 5. ZCHPC validation traceability

| Commitment | Mechanism/evidence |
|---|---|
| signed authorisation exists | non-secret local reference metadata; signed document itself is not committed |
| exact approved scope only | `authorised-zchpc` profile + immutable allow-list/address policy |
| non-destructive by default | operational profile and mutation-block tests |
| no deliberate production weaknesses | policy + P10 gate |
| no unrelated tenants/assets | destination/scope validation + `RT-ZCHPC-*` tests |
| confidential evidence protected | redaction/minimisation + restricted report handling |
| operational analysis separate from lab accuracy | distinct environment/dataset type in evaluation model |

## 6. Safety traceability

Hard commitments include explicit scope, central execution, atomic budgets, isolated identities, proof-of-condition stopping, redaction before persistence/export, no credential attacks, no destructive fuzzing/DoS/VM escape/lateral movement and no scanner access to controlled-lab ground truth.

## 7. Delimitations

Not completion requirements: three technology stacks, extra government labs, fintech/mobile-money/healthcare labs, full hypervisor assessment, SAST, comprehensive GraphQL/SOAP/gRPC, unrestricted penetration testing, exploit chaining, production SaaS or LLM services.

## 8. Final release checklist

- [ ] every implemented rule maps to a versioned catalogue entry;
- [ ] every headline controlled case maps to a frozen ground-truth ID;
- [ ] paired positive/corrected cases exist where applicable;
- [ ] reportable scans generate redacted HTML/PDF/JSON/CSV;
- [ ] controlled lab matcher/formulas/state treatment were frozen before final collection;
- [ ] ZAP version/configuration/applicability rules are recorded;
- [ ] all failed/inconvenient controlled runs carry validity reasons;
- [ ] P10 operational profile matches signed scope before traffic;
- [ ] ZCHPC conclusions remain limited to the authorised validation;
- [ ] no real credentials, authorisation documents or confidential operational data are committed.
