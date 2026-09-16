# Academic Proposal Baseline

## 1. Status

This is the repository-local implementation baseline for the final proposal.

**Project title:** *Automated API Security Testing and Misconfiguration Scanner for Zimbabwean E-Government Systems: A Cloud-Based Evaluation*

The title and central topic are locked. The scanner is the research artefact. The cloud is the evaluation context, not a replacement project topic.

The evaluation has two stages: a controlled XCP-ng/Xen Orchestra replica cloud with known ground truth, followed by validation inside the authorised ZCHPC cloud scope.

## 2. Aim

To design, implement and evaluate an automated API security testing and misconfiguration scanner for Zimbabwean e-government systems that identifies selected API security weaknesses and automatically generates reproducible security assessment reports, using a controlled XCP-ng/Xen Orchestra cloud laboratory for ground-truth evaluation and the authorised ZCHPC cloud environment for subsequent real-world validation.

## 3. Technical objectives

1. Design and implement a modular REST API security scanner with target allow-listing, request limits and secret redaction.
2. Implement automated checks for selected OWASP API risks, including BOLA, BFLA, BOPLA, authentication/session, security misconfiguration and inventory weaknesses.
3. Deploy the synthetic e-government API and scanner in a controlled XCP-ng/Xen Orchestra cloud laboratory for staged security evaluation.
4. Automatically generate redacted HTML/PDF and machine-readable JSON/CSV reports containing findings, evidence, severity, OWASP/CWE classification and remediation guidance.
5. Evaluate scanner accuracy, repeatability and report quality against independent ground truth and an applicable OWASP ZAP baseline, then validate the proven scanner within the authorised ZCHPC cloud assessment scope.

## 4. Research questions

- **RQ1:** Which selected API authorisation, authentication, configuration, inventory and bounded deployment weaknesses can the scanner detect reliably in the controlled cloud laboratory?
- **RQ2:** How accurately does the scanner identify predeclared seeded weaknesses when compared with independent ground truth and an applicable OWASP ZAP baseline?
- **RQ3:** How consistently can the scanner generate redacted, reproducible and actionable security reports from its findings?
- **RQ4:** After successful controlled-cloud validation, how applicable and repeatable is the scanner within the formally authorised ZCHPC cloud scope?

## 5. Stage 1 — controlled replica cloud

The controlled experiment uses a small XCP-ng cloud managed through Xen Orchestra. XCP-ng is the hypervisor; Xen Orchestra is the management/orchestration layer. Xen Orchestra may run as a VM/appliance or another approved management node according to the available lab resources.

The lab is designed to resemble the relevant ZCHPC virtualisation pattern at an architectural level without claiming to duplicate production exactly.

Minimum logical roles are:

- controlled XCP-ng host;
- Xen Orchestra management/orchestration service;
- scanner VM;
- synthetic e-government API VM;
- database/supporting service on a separate VM where resources permit, otherwise colocated with the API VM.

Management access should be separated from the service/test network wherever the available infrastructure permits.

### Synthetic Government Permit and Service Application API

Canonical engineering ID: `government-permit-service-fastapi`.

The application uses synthetic data only. It is not a replica of a named government system.

Minimum application roles: Applicant, Officer and Administrator; engineering fixtures use two applicants so cross-user authorisation can be tested.

The lab must have:

- vulnerable and corrected states;
- deterministic seed/reset;
- synthetic users, records, document metadata and application states;
- OpenAPI description;
- direct functional tests independent of scanner logic;
- a machine-readable ground-truth manifest authored before final detector tuning/evaluation.

### Selected controlled deployment/cloud cases

The replica may also deliberately seed bounded, reversible deployment weaknesses whose expected secure state is known independently of scanner output, for example:

- unnecessary exposed services/ports;
- incorrect firewall or network-reachability rules;
- management service exposure to the wrong network;
- database reachability from an unauthorised lab subnet;
- insecure service binding;
- selected TLS/certificate configuration weaknesses;
- poor VM/network segmentation;
- inappropriate lab-only role/permission configuration where it can be tested safely;
- backup/snapshot exposure only where an isolated lab case is available and non-destructive.

No VM escape, destructive hypervisor exploitation or denial-of-service is part of the controlled experiment.

## 6. Independent ground truth

Ground truth is predeclared and independent of scanner detector logic. Each controlled case receives a stable case ID, expected secure state and vulnerable/corrected proof procedure before final data collection.

Direct application tests and/or direct replica-cloud configuration checks prove the intended state without using scanner findings. The evaluation harness may compare scanner output to the frozen ground truth only after scanner execution.

## 7. Automatic reporting

After every completed scan the artefact must be able to generate:

- human-readable HTML;
- human-readable PDF;
- canonical JSON;
- CSV analysis/export data.

Findings include affected endpoint/service, severity, confidence, expected versus observed behaviour, minimal redacted evidence, OWASP/CWE mapping where appropriate and remediation guidance. NIST/ISO references are contextual only and are not compliance determinations.

## 8. Controlled evaluation

The controlled replica cloud is the source of quantitative accuracy claims. The evaluation records TP/FP/FN and TN/FPR only where the negative-unit denominator is defensible, plus precision, recall, F1, scan time, request count, errors/inconclusive outcomes and repeated-run/report reproducibility.

OWASP ZAP is a general-purpose baseline only for cases where an equivalent observation is practical. Unsupported multi-identity semantics are coverage differences, not automatic ZAP false negatives.

Before final controlled data collection, freeze the ground truth, matching logic, metric/state treatment, lab version, scanner profile and ZAP configuration. Repeat the final frozen configuration sufficiently to assess stability; the chosen repetition count must be reported as an engineering/research protocol choice rather than treated as a magical statistical threshold.

## 9. Stage 2 — authorised ZCHPC validation

A later real-world validation stage is part of the approved project. It starts only after the scanner passes the controlled replica-cloud safety and accuracy gates.

The researcher has signed ZCHPC authorisation for the project. The implementation must still constrain every operational run to the exact approved assets, interfaces, accounts, traffic levels and time windows represented in local scope configuration/authorisation-reference metadata.

The scanner uses a restricted non-destructive profile. It does not deliberately introduce weaknesses into operational ZCHPC infrastructure.

Permitted observations depend on the signed scope and may include authorised API/service exposure, approved authentication/access-control behaviour, TLS/HTTP security configuration, documentation exposure, service inventory differences and other safe externally observable deployment misconfigurations.

Explicitly excluded unless separately and specifically authorised: VM escape, hypervisor exploitation, denial-of-service, lateral movement, unrelated tenants/assets, persistence and destructive fuzzing.

Operational ZCHPC results are analysed separately from controlled-cloud accuracy because complete operational ground truth may not exist.

## 10. Scope boundaries

Current dissertation scope excludes additional academic application labs/stacks, comprehensive GraphQL/SOAP/gRPC testing, source-code/static analysis, malware analysis, full hypervisor penetration testing, generic exploit chaining and unrestricted penetration testing.

Fintech, mobile-money, healthcare and additional e-government/commercial environments are future work only.

## 11. Research-integrity lock

Ground truth, matching logic, metric formulas/state treatment and the final controlled-cloud scanner profile must be frozen before final controlled data collection. Failed or inconvenient runs are retained with validity reasons.

No repository document, issue, UI or implementation may silently reintroduce the former three-lab requirement, collapse the replica-cloud stage into a single standalone VM, or make the authorised ZCHPC validation merely optional.
