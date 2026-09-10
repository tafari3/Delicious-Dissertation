# Pre-Implementation Red-Team Attack Matrix

## 1. Purpose

This catalogue defines adversarial acceptance cases against the scanner, controlled lab, dashboard, evidence/reporting, evaluation and later authorised ZCHPC validation. Tests are defensive and use controlled fixtures; they do not authorise offensive activity against third parties.

A phase cannot close while an applicable CRITICAL/HIGH case is untested or failing.

## 2. Scope/network cases

| ID | Sev | Phase | Required safe behaviour |
|---|---|---|---|
| RT-NET-001 | CRITICAL | P4 | canonical IP parsing blocks alternate-notation scope bypass |
| RT-NET-002 | CRITICAL | P4 | DNS answer changes outside approved addresses block before transmission |
| RT-NET-003 | CRITICAL | P4 | mixed approved/unapproved DNS answers cannot route to unapproved address |
| RT-NET-004 | CRITICAL | P4 | metadata/link-local/internal classes outside explicit scope are blocked |
| RT-NET-005 | CRITICAL | P4 | hostname case/trailing-dot/IDN confusion cannot bypass equality policy |
| RT-NET-006 | CRITICAL | P4 | path normalisation/encoding cannot escape approved base path |
| RT-NET-007 | CRITICAL | P4 | every redirect hop is independently validated |
| RT-NET-008 | CRITICAL | P4 | credentials never follow to unvalidated authority |
| RT-NET-009 | CRITICAL | P1/P4 | ambient proxy variables cannot silently reroute target traffic |
| RT-NET-010 | CRITICAL | P3/P4 | only HTTP/HTTPS target transports accepted |
| RT-NET-011 | HIGH | P4 | arbitrary Host/authority override cannot change routing |
| RT-NET-012 | HIGH | P4 | connection reuse cannot bypass immutable scan scope |

## 3. Budget/concurrency cases

| ID | Sev | Phase | Required safe behaviour |
|---|---|---|---|
| RT-BUDGET-001 | CRITICAL | P4 | atomic reservation prevents parallel oversubscription |
| RT-BUDGET-002 | HIGH | P4 | retries consume budgets |
| RT-BUDGET-003 | HIGH | P4 | redirect hops consume budgets |
| RT-BUDGET-004 | HIGH | P4 | cancellation prevents new queued work |
| RT-BUDGET-005 | CRITICAL | P6 | resource rules cannot borrow the larger general budget |
| RT-BUDGET-006 | HIGH | P5/P6 | exceptions cannot create unbounded retry/reschedule loops |

## 4. Import/specification cases

| ID | Sev | Phase | Required safe behaviour |
|---|---|---|---|
| RT-SPEC-001 | HIGH | P3 | oversized import bounded/rejected |
| RT-SPEC-002 | HIGH | P3 | recursive/deep schema traversal bounded with cycle detection |
| RT-SPEC-003 | CRITICAL | P3/P4 | external references cannot fetch arbitrary files/network destinations |
| RT-SPEC-004 | CRITICAL | P3 | safe YAML loader only |
| RT-SPEC-005 | HIGH | P3/P8 | expanded/decompressed content bounded or unsupported |
| RT-SPEC-006 | CRITICAL | P3 | Postman scripts remain inert |
| RT-SPEC-007 | CRITICAL | P3/P4 | imported server URLs cannot expand operator-approved scope |
| RT-SPEC-008 | HIGH | P3 | variable expansion cannot read secrets/create uncontrolled targets |

## 5. Secret/identity cases

| ID | Sev | Phase | Required safe behaviour |
|---|---|---|---|
| RT-SECRET-001 | CRITICAL | P4/P7 | runtime-known secrets removed from evidence/export/logging |
| RT-SECRET-002 | HIGH | P4/P7 | structured/exact known secret leakage is removed; claim boundary documented |
| RT-SECRET-003 | CRITICAL | P4 | file-secret traversal/symlink/device abuse blocked |
| RT-SECRET-004 | CRITICAL | P1/P4 | exception/log formatting never dumps secret-bearing raw requests |
| RT-ID-001 | CRITICAL | P4/P5 | identity sessions/cookies do not cross-contaminate |
| RT-ID-002 | CRITICAL | P4/P5 | anonymous context inherits no authentication state |
| RT-ID-003 | HIGH | P4 | login/refresh network action is scope-validated |

## 6. Rule correctness cases

| ID | Sev | Phase | Required safe behaviour |
|---|---|---|---|
| RT-RULE-001 | HIGH | P5/P6 | HTTP 2xx alone cannot confirm vulnerability |
| RT-RULE-002 | CRITICAL | P5/P6 | timeout/parse/comparison errors become ERROR/INCONCLUSIVE, never pass |
| RT-RULE-003 | HIGH | P5 | reflected ID alone cannot prove BOLA |
| RT-RULE-004 | HIGH | P5 | same status/length/schema cannot substitute for semantic proof |
| RT-RULE-005 | HIGH | P5 | BOPLA write requires independent persistence read-back |
| RT-RULE-006 | HIGH | P5/P6 | cleanup/reset failure stops further unsafe mutations |
| RT-RULE-007 | HIGH | P5/P6 | non-idempotent operations are not silently treated read-only |

## 7. State/database cases

| ID | Sev | Phase | Required safe behaviour |
|---|---|---|---|
| RT-STATE-001 | HIGH | P4 | invalid lifecycle transitions blocked |
| RT-STATE-002 | HIGH | P4/P7 | crash cannot persist unredacted evidence or false completion |
| RT-STATE-003 | HIGH | P4 | concurrent scans isolate budgets/state/identities/evidence |
| RT-DB-001 | HIGH | P4/P7 | target-controlled text remains parameterised data |
| RT-DB-002 | HIGH | P7 | evidence/database growth is explicitly bounded |

## 8. Dashboard/report cases

| ID | Sev | Phase | Required safe behaviour |
|---|---|---|---|
| RT-WEB-001 | CRITICAL | P8 | CSRF/origin controls protect state changes |
| RT-WEB-002 | HIGH | P8 | loopback/Host/CORS policy prevents arbitrary-origin abuse |
| RT-WEB-003 | CRITICAL | P7/P8 | target-controlled evidence cannot execute script/HTML |
| RT-WEB-004 | HIGH | P7/P8 | target template syntax is inert data |
| RT-WEB-005 | HIGH | P7/P8 | export/download traversal blocked |
| RT-REPORT-001 | HIGH | P7 | CSV formula injection neutralised |
| RT-REPORT-002 | CRITICAL | P7 | HTML/PDF source treats target content as escaped data |
| RT-REPORT-003 | HIGH | P1/P7/P8 | terminal/control sequences cannot manipulate operator output |
| RT-REPORT-004 | MEDIUM | P7 | typed JSON/CSV/report schema edge cases fail explicitly |

## 9. Controlled-lab cases

| ID | Sev | Phase | Required safe behaviour |
|---|---|---|---|
| RT-LAB-001 | CRITICAL | P2 | vulnerable lab is not publicly exposed by canonical config |
| RT-LAB-002 | HIGH | P2 | no privileged container/host network/Docker socket/unneeded host mount |
| RT-LAB-003 | HIGH | P2 | canonical lab has no production/external service dependency |
| RT-LAB-004 | HIGH | P2/P9 | vulnerable/corrected modes differ only by seeded cases/supporting metadata |
| RT-LAB-005 | HIGH | P5/P9 | ordinary scanner detector code cannot read ground truth |

## 10. Evaluation/research-integrity cases

| ID | Sev | Phase | Required safe behaviour |
|---|---|---|---|
| RT-EVAL-001 | CRITICAL | P9/P10 | ground-truth/version changes invalidate affected controlled comparisons |
| RT-EVAL-002 | HIGH | P9/P10 | failed/inconvenient runs retained with validity reason |
| RT-EVAL-003 | HIGH | P9 | matcher cannot overmatch wrong endpoint/fixture/category-only result |
| RT-EVAL-004 | CRITICAL | P9 | detector cannot consume evaluation expectations |
| RT-EVAL-005 | HIGH | P9/P10 | ZAP comparison distinguishes unsupported coverage from tested-and-missed |

## 11. Supply-chain/repository cases

| ID | Sev | Phase | Required safe behaviour |
|---|---|---|---|
| RT-SUPPLY-001 | HIGH | P1 | third-party Actions pinned to full SHAs |
| RT-SUPPLY-002 | HIGH | P1 | explicit least-privilege workflow permissions |
| RT-SUPPLY-003 | CRITICAL | P1 | ordinary PR code receives no privileged secrets |
| RT-SUPPLY-004 | HIGH | P1/P2 | scanner/lab dependencies reproducibly locked |
| RT-SUPPLY-005 | MEDIUM | P1/P2 | avoid/document unnecessary install-time remote hooks |
| RT-GIT-001 | CRITICAL | P1+ | secret scanning covers introduced commit/range, not only final tree |

## 12. ZCHPC operational-validation cases

These are P10 defensive gates and do not grant any permission beyond the signed authorisation.

| ID | Sev | Required safe behaviour |
|---|---|---|
| RT-ZCHPC-001 | CRITICAL | local operational profile mismatches signed approved scope -> BLOCK before traffic |
| RT-ZCHPC-002 | CRITICAL | controlled-lab mutation/resource profile applied to operational target -> BLOCK |
| RT-ZCHPC-003 | CRITICAL | redirect/discovery/target expansion toward unrelated asset or tenant -> BLOCK before transmission |
| RT-ZCHPC-004 | HIGH | confidential operational evidence cannot enter public Git/research export unsanitised |
| RT-ZCHPC-005 | HIGH | target instability or operational budget threshold triggers stop; no escalation |
| RT-ZCHPC-006 | HIGH | report/evaluation must not present limited validation as full cloud ground truth/certification |

## 13. Phase attack sets

- **P1:** RT-NET-009, RT-SECRET-004, RT-REPORT-003, RT-SUPPLY-001..004, RT-GIT-001.
- **P2:** RT-LAB-001..004 plus dependency locking.
- **P3:** RT-NET-010, RT-SPEC-001..008.
- **P4:** RT-NET-001..012, RT-BUDGET-001..004, RT-SECRET-001..004, RT-ID-001..003, RT-STATE-001..003, RT-DB-001.
- **P5/P6:** RT-RULE-001..007, RT-BUDGET-005..006.
- **P7:** RT-DB-002, RT-REPORT-001..004, report-side RT-WEB-003/004, full secret regression.
- **P8:** RT-WEB-001..005 and terminal regression.
- **P9:** RT-LAB-005, RT-EVAL-001..005.
- **P10:** applicable prior regressions + RT-ZCHPC-001..006 + final research-integrity/supply-chain review.

An attack is covered only when the expected safe behaviour is reproducibly tested where technically practical; documentation alone is insufficient for applicable CRITICAL/HIGH controls once that phase exists.
