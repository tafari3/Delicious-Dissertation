# Security Test Catalogue

## 1. Purpose

This is the bounded rule contract for the dissertation scanner. Every implemented rule requires a stable ID/version, prerequisites, safe request plan, proof/inconclusive conditions, request budget, evidence schema and stop condition.

## 2. Result states

`NOT_APPLICABLE`, `PASS_OBSERVED`, `CONFIRMED`, `SUSPECTED`, `INFORMATIONAL`, `INCONCLUSIVE`, `ERROR`.

`ERROR` and `INCONCLUSIVE` are never converted to passes.

## 3. Common requirements

Every rule must use the controlled HTTP executor, stay in explicit scope, consume hard budgets, stop at proof, avoid destructive payloads, use disposable lab fixtures for writes, redact before persistence, and record reproducible evidence. A 2xx status alone is never proof.

## 4. Authorisation rules

- `AUTHZ-BOLA-001` — controlled cross-user object read.
- `AUTHZ-BOLA-002` — controlled cross-user mutation on disposable lab object.
- `AUTHZ-BFLA-001` — low-privilege access to privileged operation.
- `AUTHZ-BFLA-002` — anonymous access to privileged operation.
- `AUTHZ-BOPLA-001` — protected property visible to restricted identity.
- `AUTHZ-BOPLA-002` — protected property/mass-assignment write, confirmed only by independent read-back.

## 5. Authentication/session rules

- `AUTHN-MISSING-001`
- `AUTHN-INVALID-001`
- `AUTHN-EXPIRED-001` when deterministic fixture exists
- `AUTHN-SESSION-001` when deterministic revoke/logout fixture exists
- `AUTHN-INCONSISTENT-001`

No credential stuffing, password spraying or token-forgery attack framework.

## 6. Configuration rules

- `CONFIG-CORS-001`
- `CONFIG-HEADERS-001`
- `CONFIG-TLS-001`
- `CONFIG-ERROR-001`
- `CONFIG-METHOD-001`
- `CONFIG-DOCS-001`

These are bounded externally observable checks. Do not treat every missing browser header or exposed documentation surface as automatically severe.

## 7. Inventory rules

- `INVENTORY-DIFF-001` — observed route missing from supplied spec using bounded known sources.
- `INVENTORY-DIFF-002` — supplied operation not observable.
- `INVENTORY-AUTH-001` — declared authentication disagrees with observed protected behaviour.

No unrestricted directory brute forcing.

## 8. Resource-control rules

- `RESOURCE-RATE-001` — small explicitly enabled rate-control observation under a strict sub-budget.
- `RESOURCE-SIZE-001` — optional bounded pagination/size observation.

Absence of throttling within the safe window is not proof that protection is absent. Never escalate into stress or denial-of-service testing.

## 9. OWASP focus

The current catalogue principally covers OWASP API Security Top 10 2023 API1, API2, API3, API4 (bounded observation), API5, API8 and API9. Unimplemented categories are reported as `not covered`, never `secure`.

## 10. Controlled lab mapping

The authoritative positive/negative cases are in `docs/13-LAB-EXPERIMENT-SPECIFICATION.md` for the single `government-permit-service-fastapi` lab.

The scanner may be applied later to the authorised ZCHPC environment only with the P10 operational profile. Lab-specific mutation cases do not automatically become permissible operational tests.
