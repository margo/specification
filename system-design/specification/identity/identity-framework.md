# Margo Identity and Authorization Framework

The Margo Identity and Authorization Framework (MIAF) is Margo's common foundation for identity, authentication, and authorization. It is built on cryptographically verifiable credentials aligned with open cloud-native identity standards, notably [SPIFFE](https://spiffe.io/).

MIAF defines:

- a **Trust Domain** model and the **SPIFFE ID** namespace for identifying Margo components;
- an **X.509-SVID** profile (an X.509 certificate carrying a SPIFFE ID in its URI SAN) as the credential a component presents;
- the **SPIFFE bundle** (a JWK Set per [RFC 7517](https://datatracker.ietf.org/doc/html/rfc7517)) as the format for distributing trust anchors, located through an optional [discovery document](./trust-bundle-and-discovery.md);
- the **Margo Identity Service (MIS)** as the identity-authority role within a Trust Domain; and
- a cryptographic and [TLS baseline](./tls-requirements.md) shared by all Margo components, with authentication by mTLS using X.509-SVIDs validated against the Trust Bundle.

The framework is generic: it does not define an enrollment protocol or a specific identity profile. Those are layered on top. The [Margo WFM Identity Profile](./wfm-identity-profile.md) is the first such profile, naming WFMs and WFM Clients and applying MIAF authentication to the [Margo Management Interface](../margo-management-interface/api-requirements-and-security.md).

Authentication is mTLS with an X.509-SVID. Authorization is performed locally by each verifier, based on the peer's verified SPIFFE ID. There is no central authorization server.

## Terminology

The following terms form the common vocabulary for Margo's non-human identity and authorization model. Some are adopted directly from SPIFFE; others are Margo-specific. This section is the authoritative definition of these terms: other Margo documents link here instead of restating them.

These identities belong to *non-human* **Margo components**: the logical units of the Margo system such as the Device Fleet Manager (DFM), Workload Fleet Manager (WFM), their clients, and infrastructure services such as registries or observability collectors. Which of their interfaces MIAF governs is defined in [Scope and Applicability](#scope-and-applicability).

Terms adopted from SPIFFE, used here as SPIFFE defines them:

- **Trust Domain**: the governed security boundary within which identities are issued and mutually recognized, a trust-root-backed identity namespace and policy boundary. A Trust Domain defines its authoritative trust anchors (the X.509 authority certificates published for the domain), the namespace for SPIFFE IDs, and the policies for identity lifecycle and authorization.
- **SPIFFE ID**: a URI of the form `spiffe://<trust-domain>/<path>` that names an identity within a Trust Domain. MIAF adopts [SPIFFE ID](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE-ID.md) syntax and validation rules by reference and defines Margo path conventions where needed (see [Identity model](#identity-model)).
- **SPIFFE Verifiable Identity Document (SVID)**: the verifiable credential representing an identity within a Trust Domain. An SVID binds a SPIFFE ID to a key pair. Its profile, cryptography, and validation are defined in [SVIDs](./svids.md).
- **Trust Bundle**: the cryptographic material (X.509 trust anchors) used to validate SVIDs issued within a Trust Domain, distributed as a SPIFFE bundle (see [Trust Bundle and Discovery](./trust-bundle-and-discovery.md)).

Terms introduced by MIAF:

- **Principal**: a non-human Margo component that holds, or is being provisioned with, a SPIFFE identity in a Trust Domain. WFMs and WFM Clients are the principals for which an identity profile exists today. An Edge Compute Device participates through the WFM Client it hosts; the device itself becomes a principal only under a future identity profile (for example, one for device fleet management).
- **Verifier**: a Margo component that validates a peer's SVID and then authorizes the call locally, using the SPIFFE ID that SVID carries.
- **Margo Identity Service (MIS)**: the identity-authority **role** within a Trust Domain. The MIS issues SVIDs, publishes the discovery document and Trust Bundle, and enforces MIAF's cryptographic and SVID-profile rules. The MIS is defined by its responsibilities, not by a specific API (see [The MIS role](#the-mis-role)).
- **Policy-based authorization**: each verifier makes authorization decisions locally, based on the peer's verified SPIFFE ID. MIAF does not use OAuth-style token scopes or a central authorization server.

## Framework Overview

MIAF has four moving parts: the **Trust Domain**, the **Margo Identity Service (MIS)**, the **Margo components** that hold and verify identities, and the **Trust Bundles** each Trust Domain publishes. Each SPIFFE ID belongs to exactly one Trust Domain, and a verifier validates SVIDs against its own Trust Domain's Trust Bundle. A component acts as a **principal** when it presents its own SVID and as a **verifier** when it validates a peer's SVID.

Once a component holds an SVID:

1. **Acquire trust material.** The component acquires its Trust Domain's Trust Bundle: it either locates the bundle through the discovery document and retrieves it over HTTPS, or receives the bundle through operator-provided configuration or out-of-band delivery (see [initial trust bootstrap](./tls-requirements.md#initial-trust-bootstrap)).
2. **Authenticate to peers.** The component and peer complete an mTLS handshake: the component presents its X.509-SVID, and the peer validates the chain against the Trust Bundle.
3. **Authorize the call.** The peer applies its local policy to the now-verified SPIFFE ID.

A component obtains its SVID through the [operator provisioning playbook](./identity-lifecycle.md#operator-provisioning-playbook).

## Scope and Applicability

MIAF is a general foundation: any Margo component MAY adopt it, and future identity profiles will extend it to new principal classes. In this release, MIAF governs:

- the **MIS trust endpoints**: the discovery document and Trust Bundle retrieval described in [Trust Bundle and Discovery Endpoints](./trust-bundle-and-discovery.md); and
- the **Workload Fleet Management interface**, through the [WFM Identity Profile](./wfm-identity-profile.md), which is the only identity profile defined so far.

Other Margo components (the Device Fleet Manager, observability collectors, or component registries, for example) MAY hold MIAF identities, but no identity profile is defined for their interfaces yet, so how they authenticate is not governed here until such a profile exists. For an interface into an external ecosystem that carries its own established authentication convention (such as an OCI registry), a component's X.509-SVID is expected to serve as the root credential it uses to obtain an ecosystem-native credential, rather than as the wire-level authentication mechanism itself.

Each principal belongs to a single Trust Domain. A WFM and its WFM Clients share one Trust Domain, and that shared Trust Domain is the basis of their mutual recognition. An operator MAY run several independent Trust Domains, for example to separate environments or tiers of differing criticality; these Trust Domains do not trust one another. Trust across Trust Domains (federation) is not defined in this release and is expected to be addressed in a future revision.

## Relationship to SPIFFE

MIAF reuses SPIFFE identity primitives rather than inventing Margo-specific credential formats or trust semantics. This framework:

- adopts by reference the SPIFFE concepts of **Trust Domain**, **SPIFFE ID**, **X.509-SVID**, and **Trust Bundle**;
- profiles or constrains those standards where Margo needs additional rules; and
- defines Margo-specific behavior for discovery and the MIS role, and constrains the SPIFFE ID path namespace to paths beginning with `/margo/`.

MIAF references the current published text of each SPIFFE specification instead of a pinned revision: SPIFFE versions its specifications by [stability level](https://github.com/spiffe/spiffe/blob/main/standards/STABILITY.md), not release tag, and every document MIAF adopts is at **Stable**, where breaking changes are reserved for critical security fixes.

| Topic | Source | Notes |
| :---- | :----- | :---- |
| SPIFFE ID syntax and validation rules | [SPIFFE ID](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE-ID.md), adopted by reference | Margo defines only path conventions where needed. |
| X.509-SVID baseline semantics | [SPIFFE X.509-SVID](https://github.com/spiffe/spiffe/blob/main/standards/X509-SVID.md), adopted by reference and constrained | Margo adds the profile constraints in [SVIDs](./svids.md#x509-svid-profile). |
| Trust Bundle | [SPIFFE Trust Domain and Bundle](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Trust_Domain_and_Bundle.md), adopted by reference | Margo serves a single SPIFFE bundle per Trust Domain and defines discovery conventions around it. |
| Bundle endpoint | [SPIFFE Federation](https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE_Federation.md), bundle-endpoint model adopted by reference | The Trust Bundle retrieval endpoint follows the bundle-endpoint model (one URL per Trust Domain). The `https_web` and `https_spiffe` endpoint profiles are candidates for future adoption; this release authenticates retrieval per [initial trust bootstrap](./tls-requirements.md#initial-trust-bootstrap). |
| Discovery document | Margo | Not part of SPIFFE; defined in [Trust Bundle and Discovery Endpoints](./trust-bundle-and-discovery.md#discovery-document-endpoint). |

## Identity Model

- **Identity representation.** An identity is named by a **SPIFFE ID** and represented by an **SVID** issued under the Trust Domain's MIS.
- **Path namespace.** A SPIFFE ID issued under a MIAF identity profile MUST have a path beginning with `/margo/`. Each identity profile claims a non-conflicting sub-prefix and defines its structure (the path conventions for WFMs and WFM Clients are in the [WFM Identity Profile](./wfm-identity-profile.md)). So that `/margo/` remains a reliable signal of MIAF provenance, a non-MIAF SVID in the same Trust Domain MUST NOT use it.
- **Uniqueness.** Each SPIFFE ID names a single identity within its Trust Domain.
- **Lifecycle.** All identities follow the [lifecycle vocabulary](./identity-lifecycle.md#lifecycle-vocabulary).
- **Extensibility.** The MIS, Trust Domain, SVID, and Trust Bundle concepts are generic; further profiles may be added for new principal classes without redefining the framework.

## The MIS Role

The **Margo Identity Service (MIS)** is a role, not a specific service. Within a Trust Domain, the MIS is responsible for:

- issuing X.509-SVIDs to principals;
- serving the [Trust Bundle retrieval endpoint](./trust-bundle-and-discovery.md#trust-bundle-retrieval-endpoint) and, when used, the [discovery document endpoint](./trust-bundle-and-discovery.md#discovery-document-endpoint) over HTTPS; and
- enforcing MIAF's cryptographic and SVID-profile requirements.

Anything that meets these responsibilities can fill the role: [SPIRE](https://spiffe.io/docs/latest/spire-about/), a CA configured for a MIAF profile, an operator's provisioning workflow, or something else. The only wire contract MIAF fixes for the MIS is the two HTTPS trust endpoints above; it does not standardize how the MIS issues SVIDs, and beyond those endpoints conformance is judged by behavior rather than by API surface.

### Deployment Patterns (informative)

Three common ways to fulfil the MIS role. The framework requirements above apply equally to all of them.

| Pattern | Description | Typical use case |
| :--- | :---------- | :--------------- |
| **Self-signed root CA** | A CA operating as a self-signed root, issuing SVIDs directly. | Self-contained or air-gapped environments. |
| **Intermediate CA under enterprise PKI** | A CA operating as an intermediate, chaining SVIDs to an enterprise or offline root. | Enterprise environments aligned with corporate PKI. |
| **SPIFFE-conformant identity service** | A SPIFFE-conformant service such as SPIRE, configured with the Margo path conventions and Trust Bundle distribution. | Cloud-native or service-mesh environments. |
