# Security Test Catalogue

## 1. Purpose

This catalogue defines the dissertation's bounded scanner rules. It is the implementation contract for rule modules and the evaluation contract for seeded laboratory vulnerabilities.

Every implemented rule must have a stable ID, version, prerequisites, safe procedure, proof condition, evidence schema and stop conditions.

## 2. Rule result semantics

Each rule execution returns one of:

- `NOT_APPLICABLE` — prerequisites are not present;
- `PASS_OBSERVED` — tested condition behaved as expected;
- `CONFIRMED` — rule-specific proof condition was observed;
- `SUSPECTED` — meaningful evidence exists but proof is incomplete;
- `INFORMATIONAL` — noteworthy observation without vulnerability assertion;
- `INCONCLUSIVE` — target behaviour prevented a reliable conclusion;
- `ERROR` — scanner/test execution failed.

A scan must never convert `INCONCLUSIVE` or `ERROR` into `PASS_OBSERVED`.

## 3. Common rule requirements

All rules MUST:

1. use the shared controlled HTTP executor;
2. respect global and rule-specific request budgets;
3. revalidate target scope/destination on every request and redirect;
4. minimise requests;
5. stop once the defined proof condition is met;
6. avoid destructive payloads;
7. use disposable seeded objects for write checks;
8. redact secrets before persistence;
9. record enough evidence for reproduction;
10. expose confidence separately from severity;
11. preserve uncertainty rather than forcing binary conclusions.

## 4. Authorisation rules

### AUTHZ-BOLA-001 — Cross-user object read

**Purpose:** detect Broken Object Level Authorisation where one controlled user can read a protected object owned by another controlled user.

**Prerequisites**

- two controlled identities, A and B;
- an operation containing or resolving an object identifier;
- a known object belonging to A and a known object belonging to B, supplied by controlled project/lab fixture metadata.

**Safe procedure**

1. Establish a baseline read of A's object as A.
2. Establish a baseline read of B's object as B.
3. Request B's object using A's session, changing only the object reference required by the operation.
4. Compare response status, semantic body shape and stable object/ownership markers.
5. Stop immediately if sufficient proof is observed.

**Confirmed condition**

A receives B's protected object or materially equivalent protected data without required authorisation and the response can be tied to B's object.

**Suspected condition**

A receives a successful/ambiguous response strongly resembling B's baseline, but stable object/ownership proof is unavailable.

**Non-finding examples**

- explicit 401/403 denial;
- object-not-found behaviour intentionally masking authorisation;
- objects explicitly configured as public.

**Evidence**

- endpoint/method;
- redacted identity labels;
- A baseline summary;
- B baseline summary;
- cross-user response summary;
- compared stable fields/statuses.

**Mapping:** OWASP API1:2023 Broken Object Level Authorization.

### AUTHZ-BOLA-002 — Cross-user object mutation

**Purpose:** detect object-level authorisation failure on controlled update/delete-like operations.

**Prerequisites**

- controlled disposable object owned by B;
- controlled identity A;
- operation marked safe for lab mutation;
- deterministic reset/cleanup available.

**Safe procedure**

1. Record the disposable object's known baseline state.
2. Attempt the smallest reversible mutation as A.
3. Verify resulting state using the legitimate owner or fixture interface.
4. If mutation occurred, record proof and stop.
5. Restore/reset laboratory state.

**Confirmed condition**

A changes or deletes B's controlled disposable object without required authority.

**Stop condition:** first verified unauthorized state change.

**Mapping:** OWASP API1:2023.

### AUTHZ-BFLA-001 — Low-privilege access to privileged function

**Purpose:** detect Broken Function Level Authorisation.

**Prerequisites**

- low-privilege and privileged controlled identities;
- an operation classified as privileged by specification or reproducible project/lab metadata.

**Safe procedure**

1. Exercise the operation using the legitimate privileged identity to establish expected function behaviour.
2. Exercise the same operation using the low-privilege identity with a harmless request or disposable object.
3. Compare status and observable outcome.

**Confirmed condition**

The low-privilege identity successfully performs the privileged action or obtains privileged-only output.

**Suspected condition**

The endpoint accepts the low-privilege request but the scanner cannot verify the resulting privileged side effect.

**Mapping:** OWASP API5:2023 Broken Function Level Authorization.

### AUTHZ-BFLA-002 — Anonymous access to privileged function

**Purpose:** identify privileged operations callable without authentication.

**Procedure:** repeat a safe privileged operation without authentication using a non-destructive/disposable request.

**Confirmed condition:** privileged output/action is available anonymously.

**Mapping:** OWASP API5:2023 and, where applicable, API2:2023 Broken Authentication.

### AUTHZ-BOPLA-001 — Unauthorized sensitive property read

**Purpose:** detect exposure of object properties that should not be visible to the requesting identity.

**Prerequisites**

- protected-property metadata from controlled lab/project policy;
- controlled identities/roles.

**Procedure**

1. Request an object as the permitted role and record allowed property set.
2. Request equivalent object as restricted role.
3. Compare returned field sets and protected values.

**Confirmed condition**

Restricted role receives a property explicitly marked inaccessible in the controlled test policy.

**Mapping:** OWASP API3:2023 Broken Object Property Level Authorization.

### AUTHZ-BOPLA-002 — Mass assignment / unauthorized property write

**Purpose:** detect acceptance of protected properties during create/update operations.

**Prerequisites**

- disposable object;
- candidate protected property from schema/reproducible controlled metadata;
- lab-safe write profile.

**Safe procedure**

1. Create/reset a disposable object.
2. Submit a normal permitted update as baseline.
3. Submit the same update including one protected candidate property using a safe synthetic value.
4. Independently verify whether the protected property changed.
5. Stop after first verified proof for that property and reset state.

**Confirmed condition**

A role can persist a property that policy declares non-writable for that role.

**Mapping:** OWASP API3:2023.

## 5. Authentication/session rules

### AUTHN-MISSING-001 — Protected operation accepts anonymous request

**Purpose:** identify missing authentication on operations declared/configured to require authentication.

**Prerequisites:** protected-operation metadata from specification or reproducible controlled project metadata.

**Procedure:** issue the minimal safe request without credentials and compare with authenticated baseline.

**Confirmed condition:** protected data/action is available without credentials.

**Mapping:** OWASP API2:2023 Broken Authentication.

### AUTHN-INVALID-001 — Invalid bearer/token accepted

**Purpose:** test whether clearly invalid credentials are incorrectly treated as authenticated.

**Safe procedure**

- use a syntactically harmless invalid token generated locally;
- do not attempt cryptographic token-forgery attacks;
- make one bounded protected-resource request.

**Confirmed condition:** target returns protected authenticated content equivalent to valid baseline.

**Mapping:** OWASP API2:2023.

### AUTHN-EXPIRED-001 — Expired controlled token remains valid

**Prerequisites:** lab/authorised environment provides a deterministic controlled expired token fixture.

**Procedure:** compare protected request with valid and expired controlled token.

**Confirmed condition:** expired token continues to grant protected access where expiry is expected to be enforced.

**Mapping:** OWASP API2:2023.

### AUTHN-SESSION-001 — Logout/revocation lifecycle observation

**Prerequisites:** target exposes deterministic logout/revocation flow and a controlled session.

**Safe procedure**

1. authenticate with test account;
2. prove session is valid;
3. invoke configured logout/revocation action;
4. retry one protected request with the same prior session/token.

**Confirmed condition:** revoked/logged-out session retains protected access contrary to declared lifecycle.

**Mapping:** OWASP API2:2023.

### AUTHN-INCONSISTENT-001 — Equivalent operations enforce inconsistent authentication

**Purpose:** flag sibling/equivalent operations where one requires authentication and another exposes equivalent protected behaviour anonymously.

Without explicit reproducible target metadata establishing meaningful equivalence, this rule should remain `SUSPECTED` or `INCONCLUSIVE` rather than over-claiming.

## 6. Configuration and misconfiguration rules

### CONFIG-CORS-001 — Credentialed arbitrary-origin CORS

**Procedure**

- send a bounded request/preflight with a synthetic non-target origin;
- inspect `Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials` and relevant vary/cache behaviour.

**Confirmed condition**

Target permits an arbitrary untrusted origin while allowing credentials on a protected API response in a configuration demonstrated by the test.

Broad origins on intentionally public endpoints are not automatically confirmed high-severity vulnerabilities.

### CONFIG-HEADERS-001 — Security header observations

Record presence/value observations for headers relevant to the HTTP/API surface.

Do not blindly apply browser-page header requirements to pure API responses.

Potential observations include:

- HSTS on HTTPS services;
- cache-control for sensitive responses;
- content-type correctness and `X-Content-Type-Options` where applicable;
- server/banner disclosure as informational unless evidence supports more.

### CONFIG-TLS-001 — TLS protocol/certificate observation

Safely record:

- certificate validity/hostname match;
- expiry status;
- negotiated protocol/cipher information available through ordinary client negotiation;
- obvious deprecated protocol support only if it can be tested without aggressive scanning.

This is a bounded client-side configuration observation, not a comprehensive TLS scanner.

### CONFIG-ERROR-001 — Verbose error/stack-trace leakage

Use malformed-but-bounded inputs derived from documented parameter types, not unrestricted fuzzing.

**Confirmed condition**

Error response exposes implementation-sensitive details such as stack traces, filesystem paths, raw database errors, framework internals or secrets.

Persist only the minimum redacted excerpt required to demonstrate leakage.

### CONFIG-METHOD-001 — Risky/unexpected HTTP methods

Compare documented allowed methods with safe `OPTIONS`/method behaviour and narrowly selected methods where testing is non-destructive.

Never issue destructive methods merely to see whether they work against uncontrolled objects.

### CONFIG-DOCS-001 — Exposed API documentation/interface

Check configured common documentation paths only within authorised target scope and request budget.

Exposure alone is not automatically a vulnerability. Classification depends on environment, sensitivity and whether documentation reveals non-public operations or sensitive metadata.

## 7. Inventory rules

### INVENTORY-DIFF-001 — Live operation missing from specification

Discovery MUST remain bounded. Sources may include:

- configured seed paths;
- links/paths returned by the controlled laboratory;
- documentation surfaces;
- Postman/OpenAPI comparison;
- reproducible target-specific route metadata during evaluation.

Do not implement unrestricted directory brute forcing.

### INVENTORY-DIFF-002 — Specification operation not observable on target

Record documented operations that consistently return route-not-found/unavailable behaviour under the configured base URL.

This is primarily inventory quality information, not necessarily a security vulnerability.

### INVENTORY-AUTH-001 — Specification security declaration disagrees with behaviour

Compare spec-declared authentication requirements with bounded anonymous observations.

When the specification says an operation is protected but anonymous access returns protected content, this may strengthen `AUTHN-MISSING-001` evidence.

## 8. Resource-control rules

### RESOURCE-RATE-001 — Bounded rate-limit behaviour

**Prerequisites**

- explicit enablement;
- controlled lab or written-authorisation scope;
- configured maximum requests;
- configured requests-per-second ceiling;
- operation classified safe and idempotent where possible.

**Procedure**

1. issue a small sequence of ordinary requests within the configured ceiling;
2. record status/timing/headers;
3. stop immediately if throttling is observed;
4. stop at the request ceiling whether or not throttling occurs.

Absence of observed throttling within a small safe window is generally `SUSPECTED` or `INFORMATIONAL`, not proof that no protection exists. The scanner must not increase load until a limit fails.

**Mapping:** OWASP API4:2023 Unrestricted Resource Consumption where appropriate.

### RESOURCE-SIZE-001 — Optional bounded page/limit observation

Where a documented pagination/limit parameter exists, test only small controlled values up to a safe configured maximum.

Do not request massive datasets.

## 9. Candidate mapping to OWASP API Security Top 10 2023

The dissertation does not claim comprehensive coverage of all ten categories. The locked catalogue focuses on controls that can be tested safely through the authorised API interface.

| OWASP category | Primary coverage |
|---|---|
| API1 Broken Object Level Authorization | BOLA read/mutation rules |
| API2 Broken Authentication | missing/invalid/expired/session rules |
| API3 Broken Object Property Level Authorization | property exposure and mass assignment |
| API4 Unrestricted Resource Consumption | bounded rate/size observations |
| API5 Broken Function Level Authorization | role/function differential rules |
| API6 Unrestricted Access to Sensitive Business Flows | only if a bounded scenario-specific rule is formally defined |
| API7 Server Side Request Forgery | not in current locked catalogue |
| API8 Security Misconfiguration | CORS/TLS/headers/errors/method/docs rules |
| API9 Improper Inventory Management | specification/live inventory differential rules |
| API10 Unsafe Consumption of APIs | not generically required in current scope |

Reports must never imply complete OWASP Top 10 coverage.

## 10. Rule implementation interface

Each rule module should expose a contract conceptually equivalent to:

```python
class ScanRule(Protocol):
    rule_id: str
    version: str
    category: str

    def applicability(context) -> Applicability: ...
    async def execute(context) -> RuleResult: ...
```

`context` provides controlled access to:

- inventory;
- identity manager;
- shared HTTP executor;
- rule budget;
- disposable test fixtures where permitted;
- evidence builder;
- cancellation state.

It must not expose raw database handles or unrestricted HTTP clients to rule implementations.

## 11. Rule-level automated testing requirements

Every rule requires:

1. unit tests for applicability;
2. proof-condition classification tests;
3. corrected/negative tests;
4. evidence-redaction tests;
5. request-budget tests;
6. at least one integration test against a corresponding seeded lab vulnerability before the rule is complete;
7. applicable semantic adversarial tests from `docs/11-RED-TEAM-ATTACK-MATRIX.md`.

## 12. False-positive control strategy

To minimise false positives:

- prefer controlled baseline comparisons over status-code heuristics;
- use two identities/roles when testing authorisation;
- require explicit protected-field/operation metadata for strong assertions;
- separate `CONFIRMED` from `SUSPECTED`;
- mark incomplete preconditions `INCONCLUSIVE` rather than vulnerable;
- preserve laboratory ground truth independently from scanner output;
- avoid treating documentation exposure, header absence or absent throttling as automatically severe;
- never confirm a write vulnerability from reflected input without independent state verification.

## 13. Stop conditions

The orchestrator must stop an individual rule/test when:

- proof condition is reached;
- request budget is exhausted;
- target scope/destination validation fails;
- redirect leaves allowed scope;
- target begins returning sustained service-unavailable/rate-limit responses beyond configured tolerance;
- cancellation is requested;
- a write test cannot guarantee disposable-state cleanup/reset;
- response size exceeds capture policy;
- a safety invariant is violated.

The scanner must prefer an incomplete result over unsafe continuation.

## 14. Laboratory mapping

The authoritative mapping from rule IDs to the Citizen Records, Public Health Records and Permit & Licensing seeded cases is `docs/13-LAB-EXPERIMENT-SPECIFICATION.md`.

Do not create new seeded cases merely to make current scanner output look better. Changes to headline evaluation cases require a reviewed methodology update before final collection.
