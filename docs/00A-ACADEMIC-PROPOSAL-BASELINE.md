# Academic Proposal Baseline

## 1. Status

This is the repository-local implementation baseline for the final proposal.

**Project title:** *Automated API Security Testing and Misconfiguration Scanner for Zimbabwean E-Government Systems: A Laboratory-Based Evaluation*

The title and central topic are locked. ZCHPC is an evaluation context, not a replacement project topic.

## 2. Aim

To design, implement and evaluate an automated API security testing and misconfiguration scanner for Zimbabwean e-government systems that identifies selected API security weaknesses and automatically generates reproducible security assessment reports, using a synthetic laboratory application for controlled validation and an authorised ZCHPC cloud environment for subsequent real-world validation.

## 3. Technical objectives

1. Design and implement a modular REST API security scanner with target allow-listing, request limits and secret redaction.
2. Implement automated checks for selected OWASP API risks, including BOLA, BFLA, BOPLA, authentication/session, security misconfiguration and inventory weaknesses.
3. Build a synthetic Government Permit and Service Application API on the ZCHPC-provided Linux VM with vulnerable and corrected states and independent ground truth.
4. Automatically generate redacted HTML/PDF and machine-readable JSON/CSV reports containing findings, evidence, severity, OWASP/CWE classification and remediation guidance.
5. Evaluate scanner accuracy, repeatability and report quality against ground truth and an applicable OWASP ZAP baseline, then validate the proven scanner within the authorised ZCHPC cloud scope.

## 4. Research questions

- **RQ1:** Which selected API authorisation, authentication, configuration and inventory weaknesses can the scanner detect reliably in the controlled laboratory?
- **RQ2:** How accurately does the scanner identify seeded weaknesses when compared with independent ground truth and an applicable OWASP ZAP baseline?
- **RQ3:** How consistently can the scanner generate redacted, reproducible and actionable security reports from its findings?
- **RQ4:** After successful laboratory validation, how applicable and repeatable is the scanner within the formally authorised ZCHPC cloud scope?

## 5. Controlled laboratory

The academic accuracy experiment uses one small e-government test application built specifically for this dissertation:

**Synthetic Government Permit and Service Application API**

Canonical engineering ID: `government-permit-service-fastapi`.

The lab runs on the Linux VM already provided by ZCHPC and uses synthetic data only. It is not a replica of a named government system.

Minimum roles: Applicant, Officer and Administrator; engineering fixtures also use two applicants so cross-user authorisation can be tested.

The lab must have:

- vulnerable and corrected states;
- deterministic seed/reset;
- synthetic users, records, documents and transactions;
- OpenAPI description;
- direct functional tests independent of scanner logic;
- a machine-readable ground-truth manifest authored before final detector tuning/evaluation.

## 6. Automatic reporting

After every completed scan the artefact must be able to generate:

- human-readable HTML;
- human-readable PDF;
- canonical JSON;
- CSV analysis/export data.

Findings include affected endpoint/service, severity, confidence, expected versus observed behaviour, minimal redacted evidence, OWASP/CWE mapping where appropriate and remediation guidance. NIST/ISO references are contextual only and are not compliance determinations.

## 7. Controlled evaluation

The lab is the source of quantitative accuracy claims. The evaluation records TP/FP/FN and TN/FPR only where the negative-unit denominator is defensible, plus precision, recall, F1, scan time, request count, errors/inconclusive outcomes and repeated-run/report reproducibility.

OWASP ZAP is a general-purpose baseline only for cases where an equivalent observation is practical. Unsupported multi-identity semantics are coverage differences, not automatic ZAP false negatives.

## 8. Authorised ZCHPC validation

A later real-world validation stage is part of the approved project. It starts only after the scanner passes the controlled laboratory evaluation.

The researcher has signed ZCHPC authorisation for the project. The implementation must still constrain every operational run to the exact approved assets, interfaces, accounts, traffic levels and time windows represented in local scope configuration/authorisation-reference metadata.

The scanner uses a restricted non-destructive profile. It does not deliberately introduce weaknesses into operational ZCHPC infrastructure.

Permitted observations depend on the signed scope and may include authorised API/service exposure, approved authentication/access-control behaviour, TLS/HTTP security configuration, documentation exposure, service inventory differences and other safe externally observable deployment misconfigurations.

Explicitly excluded unless separately and specifically authorised: VM escape, hypervisor exploitation, denial-of-service, lateral movement, unrelated tenants/assets, persistence and destructive fuzzing.

Operational ZCHPC results are analysed separately from lab accuracy because complete operational ground truth may not exist.

## 9. Scope boundaries

Current dissertation scope excludes additional academic labs/stacks, comprehensive GraphQL/SOAP/gRPC testing, source-code/static analysis, malware analysis, full hypervisor assessment, generic exploit chaining and unrestricted penetration testing.

Fintech, mobile-money, healthcare and additional e-government/commercial environments are future work only.

## 10. Research-integrity lock

Ground truth, matching logic, metric formulas/state treatment and the final lab scanner profile must be frozen before final controlled data collection. Failed or inconvenient runs are retained with validity reasons.

No repository document, issue, UI or implementation may silently reintroduce the former three-lab requirement or make ZCHPC merely optional hosting.
