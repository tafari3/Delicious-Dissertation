# Pre-Implementation Hardening Locks

## 1. Purpose

Mandatory design responses to the adversarial review. Equivalent or stronger controls may replace an implementation detail only through a reviewed change.

## 2. Network/scope locks

- one canonical URL/scope-normalisation module;
- HTTP/HTTPS targets only;
- reject URL userinfo and ambiguous address/path forms;
- canonical DNS/IP/port/base-path comparison;
- validate actual connection destination against immutable scan scope;
- revalidate every redirect before transmission;
- imported spec metadata never authorises new scope;
- target HTTP clients ignore ambient proxy environment by default;
- rule modules cannot override Host/authority to reroute traffic.

## 3. Parser/import locks

- safe YAML loading only;
- Postman scripts inert;
- external references disabled by default;
- explicit import/recursion/expanded-content ceilings;
- imported servers/variables cannot widen scope or read arbitrary runtime secrets.

## 4. HTTP/budget locks

Global, rule and resource budgets are atomically reserved before scheduling. Retries/redirect hops count. Active scans use immutable scope/profile/rule/non-secret identity snapshots. Cancellation prevents new scheduling. No raw-client escape hatch exists for rule modules.

## 5. Secret/identity locks

Each identity, including anonymous, has an isolated session/cookie jar. Secret-file references use bounded regular-file policy. Logging uses sanitised summaries. Redaction guarantees configured structured fields/headers and exact runtime-known secret values; it does not claim universal detection of every transformed secret.

## 6. Local dashboard/report locks

- loopback bind by default;
- Host validation;
- no permissive wildcard CORS;
- CSRF protection for browser state changes;
- target-controlled content escaped;
- HTML/PDF cannot embed active target content;
- CSV formula prefixes neutralised;
- terminal control text sanitised;
- export paths generated from controlled IDs/slugs;
- JSON/evaluation schemas validated.

## 7. Controlled-lab locks

Only one academic lab is required: `government-permit-service-fastapi`.

Canonical vulnerable lab configuration:

- synthetic credentials/data only;
- deterministic vulnerable/corrected modes;
- deterministic health/version/fixture metadata;
- direct tests independent of scanner output;
- ground truth invisible to scanner detector code;
- loopback/controlled-local exposure;
- no privileged container, host networking, Docker socket or unnecessary host mount;
- no production/external dependency;
- reproducibly locked dependencies.

## 8. Research-integrity locks

Every controlled evaluation records scanner commit, rule catalogue version, lab/mode/fixture version, ground-truth hash, matcher version, spec hash/profile and validity reason.

Before final P9 controlled collection freeze ground truth, matcher, metric formulas/state treatment, scanner profile and ZAP version/configuration. Failed/poor/flaky runs are retained with reasons.

## 9. ZCHPC operational locks

P10 starts only after P9 passes.

- signed project authorisation exists, but exact operational scope must still be represented locally and pass preflight;
- real hosts/IPs/credentials/authorisation documents remain outside Git;
- operational profile is non-destructive by default and stricter than lab profile;
- controlled-lab mutation/resource permissions never inherit into ZCHPC runs;
- no deliberate production weakness seeding;
- no unrelated tenant/asset discovery or access;
- no hypervisor exploitation, VM escape, DoS/stress, persistence or lateral movement;
- confidential operational evidence is minimised and restricted;
- a limited operational validation is never reported as full-cloud certification/complete ground truth;
- any action not clearly covered by signed scope is blocked pending scope clarification.

## 10. CI/supply-chain locks

Third-party Actions use full commit SHAs; workflows declare least privilege; untrusted PR verification receives no privileged secrets; P1/P2 dependencies are reproducibly locked; secret scanning considers introduced commit/range content.

## 11. Phase additions

- P1 establishes logging, sanitisation, dependency/CI/secret foundations.
- P2 proves one-lab containment and independent ground truth.
- P3 proves safe import.
- P4 proves all execution/scope/session/budget invariants.
- P5/P6 prove semantic false-confirmation resistance.
- P7 proves automatic HTML/PDF/JSON/CSV reporting safety.
- P8 proves local-dashboard/CLI safety.
- P9 proves controlled research integrity.
- P10 proves operational-scope enforcement and safe ZCHPC validation.
