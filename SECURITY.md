# Margo Security Policy

The Margo project takes the security of its specifications, reference implementations, and network-facing tooling seriously. As a project hosted under the Joint Development Foundation (JDF) and the Linux Foundation (LF), Margo acts as an **Open-Source Software Steward** under the EU Cyber Resilience Act (CRA).

This policy outlines how to report security vulnerabilities, our response SLAs, and our coordinated disclosure process.

---

## Supported Versions

Margo is currently in active pre-GA development. Security updates are actively maintained on default branches for live deliverables.

| Deliverable / Component | Repository | Supported | Notes |
| :--- | :--- | :---: | :--- |
| Code First Sandbox | `margo/sandbox` | **Yes** | Active reference implementation |
| Workload Fleet Manager Integration | `margo/symphony` | **Yes** | Active integration (Eclipse Symphony) |
| Application Registry Protocol | `margo/specification` | **Yes**¹ | OCI-compliant network API spec |
| Deprecated / Archived Repositories | Any | **No** | Untracked / inactive branches |

¹ `margo/specification` is documentation, not executable code, and is not itself a Product with Digital Elements (PDE) under the CRA. It is included here voluntarily because it defines the security-relevant behavior (authentication flow, path-traversal and symlink constraints) that `margo/sandbox` and `margo/symphony` implement — a specification defect here can produce a vulnerability downstream. This row is monitored for design-level accuracy; the CRA vulnerability-reporting *obligation* applies to the reference implementation and integration repositories.

*Note: As new repositories reach "reference implementation" or "conformance testing" status, they will be brought under the scope of this security policy.*

---

## Reporting a Vulnerability

If you discover a security vulnerability or flaw in any Margo deliverable, **please do not open a public GitHub issue or discuss it in public channels.** Public disclosure before a fix is available puts downstream adopters at risk.

### How to Submit a Private Report
Please report security vulnerabilities through one of the following channels:

1. **GitHub Private Vulnerability Reporting (Preferred):**
   Navigate to the **Security** tab of the affected Margo repository, click on **Advisories**, and select **Report a vulnerability**.
2. **Encrypted / Private Email:**
   Send your report to **security@project.margo.org**.

### What to Include in Your Report
To help us triage and resolve the issue quickly, please include:
* The affected repository, component, and commit SHA/version.
* A clear description of the vulnerability and its potential security impact.
* Step-by-step instructions or a proof-of-concept (PoC) to reproduce the issue.
* Any potential mitigations or remediations you have identified.

---

## Vulnerability Handling & Response SLAs

Upon receiving a private security report, the Margo maintainers will adhere to the following response timeline:

* **Acknowledgment:** Receipt of report acknowledged within **72 hours**.
* **Triage & Assessment:** Initial validation, severity assessment (CVSS), and impact analysis completed within **7 business days**.
* **Remediation & Advisory:** Fix developed, tested, and coordinated for release alongside a security advisory within a mutually agreed disclosure window (typically 30–90 days, depending on complexity).

---

## Coordinated Disclosure & CRA Compliance

Margo follows Coordinated Vulnerability Disclosure (CVD) principles in accordance with OpenSSF and Linux Foundation guidance.

### 1. EU CRA Steward Escalation Protocol
In compliance with Article 24 and Article 14 of the EU Cyber Resilience Act (Regulation (EU) 2024/2847):
* **Actively Exploited Zero-Days & Severe Incidents:** If a reported vulnerability is determined to be actively exploited in the wild, or if a severe cybersecurity incident affects Margo's development infrastructure, Margo will immediately escalate the issue to Linux Foundation Security (`security@linuxfoundation.org`).
* **EU Authority Reporting Timeline:** LF Security will coordinate the required notifications to the European Union Agency for Cybersecurity (ENISA) via the Single Reporting Platform (SRP) and designated National CSIRTs, in accordance with the mandatory legal timeframes:
  * **Early warning:** within **24 hours** of becoming aware of an actively exploited vulnerability or severe incident.
  * **Vulnerability / incident notification:** within **72 hours**, providing general information on the vulnerability, its nature, and any mitigations taken.
  * **Final report:** no later than **14 days** after a corrective or mitigating measure is available for an actively exploited vulnerability (**1 month** for a severe incident), including a description of the issue, severity, and remediation details.

### 2. Downstream Security Advisories
Once a fix is available, Margo will publish a machine-readable GitHub Security Advisory (GHSA) and request a CVE identifier where applicable. This provides full transparency to commercial manufacturers, industrial vendors, and downstream ecosystem participants integrating Margo deliverables.

---

## Contact

* **Margo Security Team:** `security@project.margo.org`
* **Linux Foundation Security Services:** `security@linuxfoundation.org`
* **Documentation & Specifications:** [docs.margo.org](https://docs.margo.org)
