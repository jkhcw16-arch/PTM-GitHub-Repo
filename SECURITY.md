# Security Policy

## Reporting a Vulnerability

Security vulnerabilities and material semantic-integrity failures SHOULD be reported privately. Do not disclose suspected vulnerabilities through public issues, pull requests, discussions, social media, or other public channels when disclosure could enable exploitation or compromise a supported PTM trust boundary.

Use GitHub private vulnerability reporting when it is enabled for this repository. Reports SHOULD include the affected version or commit, reproduction steps, expected and actual behavior, demonstrated impact, and any known mitigation. Do not submit credentials, private keys, customer data, trade secrets, or third-party restricted information.

## Supported Versions

Unless a release notice states otherwise, security fixes apply to the latest published release and the current maintained development branch. Earlier releases, forks, and third-party modifications are not supported unless expressly stated.

## Severity Classification

PTM security reports SHALL be assigned a project severity based on demonstrated impact, exploitability, scope, detectability, and recoverability.

| Severity | Classification |
|---|---|
| **Critical** | A vulnerability causes or enables catastrophic compromise of a supported PTM trust boundary, release process, or security-sensitive deployment, with no effective ordinary mitigation. |
| **High** | A vulnerability materially compromises authorization, trusted state, semantic integrity, validation, provenance, or supply-chain integrity in a supported deployment. |
| **Medium** | A reproducible vulnerability or integrity defect has meaningful but bounded impact, requires material prerequisites, or is limited to a constrained workflow. |
| **Low** | A defect has limited impact, is readily detectable, and can be safely mitigated without materially compromising a PTM trust boundary. |
| **Informational** | A report identifies a hardening opportunity, documentation issue, or theoretical concern without demonstrating a material vulnerability or semantic-integrity failure. |

### Classification Factors

Severity SHALL be evaluated using the following factors, as applicable:

- **Exploitability:** difficulty and prerequisites required to trigger the defect.
- **Integrity:** potential corruption of states, deltas, validation results, provenance, or release artifacts.
- **Authorization:** ability to bypass required policy, assurance, or execution controls.
- **Scope:** extent of affected artifacts, workflows, releases, or deployments.
- **Detectability:** whether the failure is silent or reliably detected before material impact.
- **Recovery:** ability to restore correct state and artifacts without material loss.

### Mathematical and Semantic Defects

Failure of a PTM mathematical or semantic invariant SHALL NOT, by itself, constitute a security vulnerability.

Applicable invariants include:

```text
delta_ij = r_j - r_i

delta_ik = delta_ij + delta_jk

epsilon(delta_ij + delta_jk)
  = epsilon(delta_ij) * epsilon(delta_jk)

epsilon_inverse(epsilon(delta))
  = delta
```

Severity SHALL be determined from the demonstrated consequences of the failure.

A defect confined to development validation MAY be classified Low or Medium. A defect that silently corrupts trusted or authorization-sensitive state MAY be classified High. Critical classification requires demonstrated catastrophic security impact consistent with the Critical definition above.

### CVSS

Conventional software vulnerabilities MAY additionally be evaluated using CVSS.

CVSS severity and PTM project severity are separate assessments. A difference between the assessments SHALL be documented when material.

### Reclassification

The maintainer MAY revise severity when new evidence changes the assessed exploitability, scope, impact, detectability, available mitigation, or recovery characteristics.

The final published advisory SHOULD reflect the severity supported by the evidence available at publication.

## PTM-Specific Scope

In-scope reports may include:

- validation bypasses;
- incorrect trusted state reconstruction;
- authorization or assurance bypasses;
- material algebraic or semantic-integrity failures;
- prime-realization or inverse-realization failures with demonstrated security consequences;
- parser, dependency, or denial-of-service vulnerabilities;
- CI/CD, release-artifact, manifest, or checksum compromise;
- credential or secret exposure; and
- material vulnerabilities in supported PTM deployments.

Prime-indexed PTM representation is not encryption and SHALL NOT be treated as cryptographic protection.

## Coordinated Disclosure

Reporters SHOULD allow a reasonable opportunity to investigate, reproduce, remediate, test, and release a correction before public disclosure.

Reporters MUST NOT intentionally access unrelated data, disrupt third-party systems, destroy data, establish persistence, or expand testing beyond what is reasonably necessary to demonstrate the reported issue.

This policy does not promise a bounty, fixed response time, remediation deadline, safe harbor, CVE assignment, or public attribution. Any such commitment must be stated separately in writing.

## Security Regression

A confirmed vulnerability correction SHOULD include an executable regression test when reasonably practical. Applicable evidence may include SHACL negative tests, algebraic round-trip tests, prime-composition tests, inverse-exponentiation tests, mutation tests, dependency checks, CI tests, or other relevant validation.

A correction SHOULD preserve valid PTM behavior in addition to preventing recurrence of the reported defect.

## Intellectual Property

A security report does not grant any copyright, patent, trademark, trade-secret, or other intellectual-property license and does not modify the repository LICENSE.

Do not submit confidential invention disclosures, unpublished patent claims, trade secrets, or third-party restricted information through public channels.

## Legal Notice

This policy describes the project's vulnerability-reporting and triage process. It does not authorize unlawful activity, access to third-party systems or data, or conduct that causes harm to others.
