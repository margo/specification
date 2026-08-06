# Transport Layer Security Requirements

These requirements are the TLS baseline for every interface authenticated under a MIAF identity profile. The baseline defines *how* TLS and mTLS behave; each identity profile defines *where* mTLS is required (for example, the [Margo Management Interface](../margo-management-interface/api-requirements-and-security.md#identity-and-authentication) requires it for every call). Traffic governed by MIAF MUST run over TLS: the mTLS connections between principals, and the HTTPS connections a client uses to retrieve the discovery document or Trust Bundle. When a peer authenticates with mTLS, its client certificate MUST be a valid X.509-SVID issued under the applicable Trust Domain. The X.509-SVID presented at the mTLS layer is the only authenticated transport credential in scope here; JWT-SVIDs are out of scope.

## Minimum TLS Baseline

MIAF follows [RFC 9852](https://datatracker.ietf.org/doc/html/rfc9852), which requires TLS 1.3 as the default and permits TLS 1.2 only as a non-default fallback.

| Requirement | Normative directive | Reference |
| :---------- | :------------------ | :-------- |
| **Default protocol version** | An implementation MUST use **TLS 1.3** as its default. | [RFC 8446](https://datatracker.ietf.org/doc/html/rfc8446), [RFC 9852](https://datatracker.ietf.org/doc/html/rfc9852) |
| **TLS 1.2 fallback** | TLS 1.2 MAY be supported as a non-default fallback where a deployment requires it. When supported, it MUST conform to [RFC 9325](https://datatracker.ietf.org/doc/html/rfc9325). | [RFC 9852](https://datatracker.ietf.org/doc/html/rfc9852), [RFC 9325](https://datatracker.ietf.org/doc/html/rfc9325) |
| **Deprecated versions** | SSL v2, SSL v3, TLS 1.0, and TLS 1.1 MUST NOT be used. | [RFC 6176](https://datatracker.ietf.org/doc/html/rfc6176) (SSL v2), [RFC 7568](https://datatracker.ietf.org/doc/html/rfc7568) (SSL v3), [RFC 8996](https://datatracker.ietf.org/doc/html/rfc8996) (TLS 1.0, TLS 1.1) |

The TLS 1.2 fallback carries a confidentiality cost specific to MIAF. A MIAF client certificate is an X.509-SVID, and TLS 1.2 sends the certificate messages in cleartext during the handshake (TLS 1.3 encrypts them), so a passive on-path observer can read the peer's SPIFFE ID, and with it the peer's Trust Domain and client relationship, from any TLS 1.2 mTLS handshake. Defaulting to TLS 1.3 avoids this. An operator that enables the fallback accepts the exposure (see [handshake identity disclosure on TLS 1.2 fallback](./identity-security-considerations.md#framework-threats)).

## Initial Trust Bootstrap

A client cannot validate MIAF-issued SVIDs against the Trust Bundle until it holds that bundle. Retrieval of that first bundle therefore cannot be authenticated with an X.509-SVID. A client acquires the trust material (the discovery document, if used, and the Trust Bundle) by one of two paths.

**Authenticated HTTPS retrieval.** The client fetches the discovery document and the Trust Bundle over HTTPS (see [Trust Bundle and Discovery](./trust-bundle-and-discovery.md)). Because an X.509-SVID cannot authenticate these connections, they rely on an initial trust mechanism established outside MIAF. The client MUST authenticate both connections using at least one of:

1. **PKI-anchored validation**: validate the [MIS](./identity-framework.md#the-mis-role) server certificate chain to a configured set of trust anchors (web PKI, enterprise PKI, or an operator-configured private CA), with DNS name validation per [RFC 9525](https://datatracker.ietf.org/doc/html/rfc9525).
2. **Pinned trust**: validate the MIS server certificate chain against operator-provisioned pins. A pin is the base64-encoded SHA-256 digest of the DER-encoded SubjectPublicKeyInfo of a certificate (the SPKI Fingerprint construction of [RFC 7469, Section 2.4](https://datatracker.ietf.org/doc/html/rfc7469#section-2.4)). A provisioned pin identifies a trust anchor for the [certificate validation](#certificate-validation) below. The connection is authenticated when the presented leaf certificate chains to a certificate whose SubjectPublicKeyInfo matches a provisioned pin (for example, a pin over the issuing CA's public key).

An operator MAY deliver the trust material for either option (the configured anchors for the first, or the pins for the second) through the same channel used to provision the principal's SVID. A client that cannot authenticate a connection by one of these mechanisms MUST abort.

**Out-of-band delivery.** The operator delivers the Trust Bundle, and the Trust Bundle URI where later refresh is intended, directly through the provisioning or deployment channel (see [Bundle contents and distribution](./trust-bundle-and-discovery.md#bundle-contents-and-distribution) and the [operator provisioning playbook](./identity-lifecycle.md#operator-provisioning-playbook)). No HTTPS retrieval takes place, so there is no bootstrap connection to authenticate; the integrity and authenticity of the delivered material rest on that channel.

Whichever path is used, a client MUST NOT accept trust material from an unauthenticated source, and MUST NOT treat the first acquisition as "trust on first use". Once acquired, the discovery document (if used) and the Trust Bundle are MIAF's authoritative sources; that bundle then validates SVIDs within the Trust Domain.

## Certificate Validation

Each endpoint MUST validate the peer's TLS certificate chain and identity in accordance with [RFC 5280](https://datatracker.ietf.org/doc/html/rfc5280). The verifier MUST check that the presented certificate chain is within its validity period and MUST reject an expired certificate. MIAF does not use RFC 5280 online revocation checking (CRL or OCSP); a compromised credential is withdrawn by removing its trust anchor from the Trust Bundle and by short SVID lifetimes (see [operator revocation playbook](./identity-lifecycle.md#operator-revocation-playbook) and [Session Lifetime and Re-validation](#session-lifetime-and-re-validation)).

Validity-period evaluation depends on a trustworthy local clock (see [unreliable verifier clock](./identity-security-considerations.md#framework-threats)). A verifier MAY apply a small, bounded clock-skew tolerance consistent with its time-synchronization assumptions.

**Server identity for MIAF HTTPS endpoints (discovery and Trust Bundle retrieval):**

- The client MUST validate the server certificate chain to its configured initial trust anchors (see [Initial Trust Bootstrap](#initial-trust-bootstrap)).
- Under PKI-anchored validation, the client MUST validate the expected DNS name per [RFC 9525](https://datatracker.ietf.org/doc/html/rfc9525). Under pinned trust, the pin itself establishes server identity, so RFC 9525 DNS-name validation applies only where the client connects by a DNS name; a client connecting to a pinned endpoint by IP address is not required to perform it.
- The Trust Bundle selected from `trustBundleUri` MUST NOT replace these TLS server-validation checks for MIAF HTTPS endpoints; it is used to validate SVIDs within the Trust Domain.

**SVID identity for MIAF mTLS:** when a peer presents an X.509-SVID at the mTLS layer, the verifier validates it and derives the peer's identity per the [X.509-SVID validation](./svids.md#x509-svid-validation) rules. SVID identity is established by the SPIFFE ID in the URI SAN, not by a DNS name.

A verifier revokes access to a compromised SVID through the [operator revocation playbook](./identity-lifecycle.md#operator-revocation-playbook).

## Session Lifetime and Re-validation

mTLS authenticates a peer only at the handshake. Because MIAF revokes through short SVID lifetimes and Trust Bundle changes rather than an online status mechanism, a long-lived or pooled connection that outlives its peer's SVID, or that survives a Trust Bundle rotation, extends the revocation lag for as long as it stays open.

A verifier therefore SHOULD limit how long an authenticated connection stays in service after the SVID that established it has expired or has ceased to validate against the current Trust Bundle. That limit SHOULD be short relative to the SVID lifetimes in use (see [SVID lifetime guidance](./identity-lifecycle.md#svid-lifetime-guidance)). Capping the maximum age of a connection satisfies this, since the re-establishing handshake re-validates the peer's current SVID against the current Trust Bundle; a verifier MAY instead re-validate the SVID on the open connection and close it when the SVID is no longer valid, and MAY tighten the limit to the SVID's own `notAfter`. Separately, a verifier SHOULD re-evaluate its local authorization policy for the peer's SPIFFE ID on each request, so that an allowlist removal takes effect without waiting for the connection to close.

These limits are measured from the full TLS handshake that validated the peer's SVID, not from any later resumption of the session. A resumed session inherits the authentication time of that original handshake, so resumption MUST NOT keep a peer authenticated beyond those limits, and a verifier that issues session tickets SHOULD limit their lifetime accordingly. A client SHOULD proactively re-establish affected connections after renewing its own SVID.

## Traffic-Inspecting Proxies

MIAF specifies end-to-end mTLS between a principal and a verifier. Terminating that mTLS at a proxy inside the verifier's trust boundary, instead of in the verifier's own process, is a deployment choice. A proxy that terminates the mTLS, validates the peer's SVID, and forwards the authenticated identity to the backend satisfies the MIAF authentication requirement on the backend's behalf. Where such a proxy forwards the identity over an application-layer header (for example, the [RFC 9440](https://datatracker.ietf.org/doc/html/rfc9440) `Client-Cert` header), that header is the caller's identity and MUST be spoof-proof: the proxy MUST remove or overwrite any `Client-Cert` or `Client-Cert-Chain` header present on an incoming request, and the backend MUST accept a forwarded identity header only on requests arriving over the trusted proxy boundary (see [RFC 9440 §4](https://datatracker.ietf.org/doc/html/rfc9440#section-4)).

**Traffic-inspecting proxies** (NGFW, SWG, SASE products) in the inline path between a principal and a verifier are not supported. Traffic inspection requires the proxy to MITM TLS for content inspection, which is architecturally incompatible with mTLS. An operator MUST exempt Margo mTLS endpoints from inspection. Other B2B mTLS APIs follow the same pattern, and inspection-proxy products commonly expose it as an explicit configuration option.
