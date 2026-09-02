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
3. revalidate target scope on every request and redirect;
4. minimise requests;
5. stop once the defined proof condition is met;
6. avoid destructive payloads;
7. use disposable seeded objects for write checks;
8. redact secrets before persistence;
9. record enough evidence for reproduction;
10. expose confidence separately from severity.

## 4. Authorisation rules

### AUTHZ-BOLA-001 — Cross-user object read

**Purpose:** detect Broken Object Level Authorisation where one controlled user can read an object owned by another controlled user.

**Prerequisites**

- two controlled identities, A and B;
- an operation containing or resolving an object identifier;
- a known object belonging to A and a known object belonging to B, preferably from lab/fixture metadata.

**Safe procedure**

1. Establish a baseline read of A's object as A.
2. Establish a baseline read of B's object as B.
3. Request B's object using A's session, changing only the object reference required by the operation.
4. Compare response status, semantic body shape and stable object/ownership markers.
5. Stop immediately if sufficient proof is observed.

**Confirmed condition**

A receives B's protected object or materially equivalent protected data without an authorisation denial and the response can be tied to B's object.

**Suspected condition**

A receives a successful/ambiguous response strongly resembling B's baseline, but stable object/ownership proof is unavailable.

**Non-finding examples**

- explicit 401/403 denial;
- object-not-found behaviour intentionally masking authorisation;
- public objects declared public in ground truth/test metadata.

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
- reset/cleanup available.

**Safe procedure**

1. Record the disposable object's known baseline state.
2. Attempt the smallest reversible mutation as A.
3. Verify the resulting state using the legitimate owner or fixture interface.
4. If mutation occurred, record proof and stop.
5. Restore/reset the laboratory state.

**Confirmed condition**

A changes or deletes B's controlled disposable object without required authority.

**Stop condition:** first verified unauthorized state change.

**Mapping:** OWASP API1:2023.

### AUTHZ-BFLA-001 — Low-privilege access to privileged function

**Purpose:** detect Broken Function Level Authorisation.

**Prerequisites**

- low-privilege and privileged controlled identities;
- an operation classified as privileged by specification, lab metadata or configured policy.

**Safe procedure**

1. Exercise the operation using the legitimate privileged identity to establish expected route/function behaviour.
2. Exercise the same operation using the low-privilege identity with a harmless request or disposable object.
3. Compare status and observable outcome.

**Confirmed condition**

The low-privilege identity successfully performs the privileged action or obtains privileged-only output.

**Suspected condition**

The endpoint accepts the low-privilege request but the scanner cannot verify the resulting privileged side effect.

**Mapping:** OWASP API5:2023 Broken Function Level Authorization.

### AUTHZ-BFLA-002 — Anonymous access to privileged function

**Purpose:** identify privileged operations that are callable without authentication.

**Procedure:** repeat a safe privileged operation without authentication using a non-destructive/disposable request.

**Confirmed condition:** privileged output/action is available anonymously.

**Mapping:** OWASP API5:2023 and, where applicable, API2:2023 Broken Authentication.

### AUTHZ-BOPLA-001 — Unauthorized sensitive property read

**Purpose:** detect excessive exposure of object properties that should not be visible to the requesting identity.

**Prerequisites**

- property sensitivity metadata from lab/ground truth or configured policy;
- controlled identities/roles.

**Procedure**

1. Request an object as the permitted role and record allowed property set.
2. Request equivalent object as restricted role.
3. Compare returned field sets and sensitive values.

**Confirmed condition**

Restricted role receives a property explicitly marked inaccessible in test metadata/ground truth.

**Mapping:** OWASP API3:2023 Broken Object Property Level Authorization.

### AUTHZ-BOPLA-002 — Mass assignment / unauthorized property write

**Purpose:** detect acceptance of protected properties during create/update operations.

**Prerequisites**

- disposable object;
- a candidate protected property from schema/ground truth/configuration;
- lab-safe write profile.

**Safe procedure**

1. Create/reset a disposable object.
2. Submit a normal permitted update as baseline.
3. Submit the same update including one candidate protected property using a safe synthetic value.
4. Verify whether that protected property changed.
5. Stop after first verified proof for that property and reset state.

**Confirmed condition**

A role can set a property that policy/ground truth declares non-writable for that role.

**Mapping:** OWASP API3:2023.

## 5. Authentication/session rules

### AUTHN-MISSING-001 — Protected operation accepts anonymous request

**Purpose:** identify missing authentication on operations declared or inferred to require authentication.

**Prerequisites:** protected-operation metadata from spec/ground truth/configuration.

**Procedure:** issue the minimal safe request without credentials and compare with authenticated baseline.

**Confirmed condition:** protected data/action is available without credentials.

**Mapping:** OWASP API2:2023 Broken Authentication.

### AUTHN-INVALID-001 — Invalid bearer/token accepted

**Purpose:** test whether clearly invalid credentials are incorrectly treated as authenticated.

**Safe procedure**

- use a syntactically harmless invalid token generated locally;
- do not attempt token forgery aimed at bypassing cryptographic verification;
- make one bounded protected-resource request.

**Confirmed condition:** target returns protected authenticated content equivalent to valid baseline.

**Mapping:** OWASP API2:2023.

### AUTHN-EXPIRED-001 — Expired controlled token remains valid

**Prerequisites:** lab/authorised environment provides a controlled expired token or deterministic token expiry fixture.

**Procedure:** compare protected request with valid and expired controlled token.

**Confirmed condition:** expired token continues to grant protected access where expiry is expected to be enforced.

**Mapping:** OWASP API2:2023.

### AUTHN-SESSION-001 — Logout/revocation lifecycle observation

**Prerequisites:** target exposes a deterministic logout/revocation flow and a controlled session.

**Safe procedure**

1. authenticate with test account;
2. prove session is valid;
3. invoke configured logout/revocation action;
4. retry one protected request with the same prior session/token.

**Confirmed condition:** revoked/logged-out session retains protected access contrary to target's declared lifecycle.

**Mapping:** OWASP API2:2023.

### AUTHN-INCONSISTENT-001 — Equivalent operations enforce inconsistent authentication

**Purpose:** flag an inventory pair where one equivalent/sibling operation requires authentication and another exposes equivalent protected data anonymously.

This rule may be `SUSPECTED` without explicit target metadata because business equivalence is difficult to infer safely.

## 6. Configuration and misconfiguration rules

### CONFIG-CORS-001 — Credentialed arbitrary-origin CORS

**Purpose:** detect a high-risk CORS combination observable through preflight/response headers.

**Procedure**

- send a bounded request/preflight with a synthetic non-target origin;
- inspect `Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials` and relevant vary/cache behaviour.

**Confirmed condition**

Target reflects/permits an arbitrary untrusted origin while allowing credentials on a protected API response in a configuration demonstrated by the test.

**Suspected/informational**

Broad origins on public endpoints without credential exposure should not be automatically classified as confirmed high severity.

### CONFIG-HEADERS-001 — Security header observations

Record presence/value observations for headers relevant to the HTTP/API surface.

Do not blindly apply browser-page header requirements to pure API responses. Findings should distinguish applicable from informational controls.

Potential observations include:

- HSTS on HTTPS services;
- cache-control for sensitive responses;
- content-type correctness and `X-Content-Type-Options` where applicable;
- server/banner disclosure as informational unless evidence supports a stronger claim.

### CONFIG-TLS-001 — TLS protocol/certificate observation

Safely record:

- certificate validity/hostname match;
- expiry status;
- negotiated protocol/cipher information available through ordinary client negotiation;
- obvious deprecated protocol support only if it can be tested without aggressive scanning.

This dissertation rule is a bounded client-side configuration check, not a full TLS scanner.

### CONFIG-ERROR-001 — Verbose error/stack-trace leakage

**Procedure**

Use malformed-but-bounded inputs derived from documented parameter types, not unrestricted fuzzing.

**Confirmed condition**

Error response exposes implementation-sensitive details such as stack traces, filesystem paths, raw database errors, framework internals or secrets.

**Evidence:** persist only the minimum redacted excerpt required to demonstrate leakage.

### CONFIG-METHOD-001 — Risky/unexpected HTTP methods

**Procedure**

Compare documented allowed methods with safe `OPTIONS`/method behaviour and narrowly selected methods where testing is non-destructive.

Never issue destructive methods merely to see whether they work against uncontrolled objects.

**Finding examples**

- privileged method unexpectedly enabled on a disposable lab resource;
- method advertised that contradicts configured policy;
- informational `Allow` method inventory.

### CONFIG-DOCS-001 — Exposed API documentation/interface

Check configured common documentation paths only when they remain within the authorised target and request budget.

Possible observations:

- Swagger/OpenAPI documents;
- Swagger UI/ReDoc-like interfaces;
- Postman or API explorer artefacts exposed by the target.

Exposure is not automatically a vulnerability. Classification depends on environment, sensitivity and whether documentation reveals non-public operations or sensitive metadata.

## 7. Inventory rules

### INVENTORY-DIFF-001 — Live operation missing from specification

**Purpose:** identify an observed/declared live endpoint-operation that is not represented in the imported specification.

Discovery MUST remain bounded. Sources may include:

- configured seed paths;
- links/paths returned by the controlled laboratory;
- documentation surfaces;
- Postman/OpenAPI comparison;
- target-specific known route metadata during evaluation.

Do not implement unrestricted directory brute forcing.

### INVENTORY-DIFF-002 — Specification operation not observable on target

Record documented operations that consistently return route-not-found/unavailable behaviour under the configured base URL.

This is primarily inventory quality information, not necessarily a security vulnerability.

### INVENTORY-AUTH-001 — Specification security declaration disagrees with behaviour

Compare spec-declared authentication requirements with bounded anonymous observations.

When the specification says an operation is protected but anonymous access returns protected content, this may feed `AUTHN-MISSING-001` as stronger evidence.

## 8. Resource-control rules

### RESOURCE-RATE-001 — Bounded rate-limit behaviour

**Purpose:** observe whether a configured sensitive operation exhibits an application-side rate-control response within a conservative test ceiling.

**Prerequisites**

- explicit enablement;
- laboratory or written-authorisation scope;
- configured maximum requests;
- configured requests-per-second ceiling;
- operation classified safe and idempotent where possible.

**Procedure**

1. issue a small sequence of ordinary requests within the configured ceiling;
2. record status/timing/headers;
3. stop immediately if throttling is observed;
4. stop at the request ceiling whether or not throttling occurs.

**Result semantics**

Absence of observed throttling within a small safe window is generally `SUSPECTED` or `INFORMATIONAL`, not proof that no protection exists. The scanner must not increase load until a limit fails.

**Mapping:** OWASP API4:2023 Unrestricted Resource Consumption where appropriate.

## 9. Optional API4 bounded response-size observation

### RESOURCE-SIZE-001 — Unbounded page/limit parameter observation

Where a documented pagination/limit parameter exists, test only small controlled values up to a safe configured maximum.

Flag evidence that the service ignores declared bounds or allows unusually large controlled page sizes only when this can be demonstrated safely.

Do not request massive datasets.

## 10. Candidate mapping to OWASP API Security Top 10 2023

The dissertation does not need to claim comprehensive coverage of all ten categories. The locked catalogue focuses on safely testable black-box controls.

| OWASP category | Primary coverage in this project |
|---|---|
| API1 Broken Object Level Authorization | BOLA read/mutation rules |
| API2 Broken Authentication | missing/invalid/expired/session rules |
| API3 Broken Object Property Level Authorization | property exposure and mass assignment |
| API4 Unrestricted Resource Consumption | bounded rate/size observations |
| API5 Broken Function Level Authorization | role/function differential rules |
| API6 Unrestricted Access to Sensitive Business Flows | only if a bounded scenario-specific rule is later defined; not generic automation by default |
| API7 Server Side Request Forgery | not in the current locked proposal catalogue unless formally added |
| API8 Security Misconfiguration | CORS/TLS/headers/errors/method/docs rules |
| API9 Improper Inventory Management | specification/live inventory differential rules |
| API10 Unsafe Consumption of APIs | not generically testable from this scanner boundary and not required by the current proposal |

The report must never imply complete OWASP Top 10 coverage when the scanner implements only the defined subset.

## 11. Rule implementation interface

Each rule module should expose a contract conceptually equivalent to:

```python
class ScanRule(Protocol):
    rule_id: str
    version: str
    category: str

    def applicability(context) -> Applicability: ...
    async def execute(context) -> RuleResult: ...
```

`context` must provide controlled access to:

- inventory;
- identity manager;
- shared HTTP executor;
- rule budget;
- disposable test fixtures where permitted;
- evidence builder;
- cancellation state.

It must not expose raw database handles or an unrestricted HTTP client to rule implementations.

## 12. Rule-level automated testing requirements

Every rule requires:

1. unit tests for applicability;
2. unit tests for proof-condition classification;
3. negative tests demonstrating no finding for corrected behaviour;
4. evidence-redaction tests;
5. request-budget tests;
6. at least one integration test against the corresponding seeded lab vulnerability before the rule is considered complete.

## 13. False-positive control strategy

To minimise false positives:

- prefer controlled baseline comparisons over status-code heuristics;
- use two identities/roles when testing authorisation;
- require explicit sensitive/protected field metadata for strong property-level assertions;
- separate `confirmed` from `suspected`;
- mark incomplete preconditions as `inconclusive` rather than vulnerable;
- preserve lab ground truth independently from scanner output;
- avoid interpreting documentation exposure, headers or absent throttling as automatically critical.

## 14. Stop conditions

The orchestrator must stop an individual rule/test when:

- proof condition is reached;
- request budget is exhausted;
- target scope validation fails;
- redirect leaves allowed scope;
- target begins returning sustained service-unavailable/rate-limit responses beyond configured tolerance;
- cancellation is requested;
- a write test cannot guarantee disposable-state cleanup;
- response size exceeds capture policy;
- safety invariant is violated.

The scanner must prefer an incomplete result over unsafe continuation.
