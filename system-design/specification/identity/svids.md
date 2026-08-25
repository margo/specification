# SVIDs

A MIAF identity is represented by an **X.509-SVID**: an X.509 certificate that binds a SPIFFE ID to a key pair, with the SPIFFE ID in the certificate's URI SAN. This topic defines the SVID profile every principal presents, the cryptographic algorithms those credentials use, and how a verifier validates a presented SVID. It applies to every interface authenticated under a MIAF identity profile.

## X.509-SVID Profile

MIAF adopts the [SPIFFE X.509-SVID specification](https://github.com/spiffe/spiffe/blob/main/standards/X509-SVID.md) by reference. X.509-SVID is the SVID representation used throughout MIAF.

An identity profile MAY further constrain validity periods, key-protection rules, or path conventions for its own principal classes.

The SPIFFE X.509-SVID specification defines the certificate profile and RFC 5280 path validation but leaves how the chain is conveyed out of scope, so MIAF must specify chain delivery. When presenting an X.509-SVID, the presenter MUST include the leaf SVID and every intermediate CA certificate needed to build a path to a trust anchor; a certificate the Trust Bundle already carries as a trust anchor (typically the self-signed root) MAY be omitted. This presented chain travels inline wherever an X.509-SVID is conveyed, including the TLS `Certificate` message during mTLS. Because the [Trust Bundle](./trust-bundle-and-discovery.md) holds only trust anchors, the presented chain is the sole carrier of the intermediates.

## Cryptographic Requirements

This section constrains the signature algorithms and key parameters used for SVIDs, CSRs, and the keys that back them. The signatures below are those approved in [FIPS 186-5](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf), over the elliptic curves specified in [NIST SP 800-186](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-186.pdf); RSA and ECDSA key lengths additionally meet the minimum strengths in [NIST SP 800-131A Rev 2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-131Ar2.pdf). The `ES256`-style codes in the table are JOSE algorithm identifiers ([RFC 7518](https://datatracker.ietf.org/doc/html/rfc7518), and [RFC 8037](https://datatracker.ietf.org/doc/html/rfc8037) for `EdDSA`), used here as familiar shorthand; the certificate itself carries the equivalent PKIX signature-algorithm OID. Transport-layer cryptography is governed separately by the [TLS requirements](./tls-requirements.md).

| Algorithm | Requirements |
| :-------- | :----------- |
| **ECDSA (P-256 or P-384)** | Keys MUST use curve P-256 (`prime256v1`) or P-384 (`secp384r1`); P-256 with SHA-256 (`ES256`) is the interoperable default, and P-384 with SHA-384 (`ES384`) MAY be used where a deployment requires a higher-assurance curve. |
| **EdDSA (Ed25519)** | Keys MUST use the Ed25519 curve; signatures follow [RFC 8032](https://datatracker.ietf.org/doc/html/rfc8032) (`EdDSA`). |
| **RSA (≥3072 + SHA-256)** | Modulus MUST be at least 3072 bits; signatures MUST use SHA-256. RSASSA-PSS (`PS256`, [RFC 8017](https://datatracker.ietf.org/doc/html/rfc8017)) is RECOMMENDED. RSASSA-PKCS#1 v1.5 (`RS256`) MAY be used only for X.509 certificate and CSR signatures (today the only RSA signatures in MIAF), for compatibility with issuing CAs that cannot produce PSS signatures (RSASSA-PKCS1-v1.5 remains an approved signature scheme in [FIPS 186-5, Section 5.4](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf)). Any other RSA signature MIAF defines later MUST use PSS. |

- **ECDSA P-256 with SHA-256 is mandatory to implement.** Every MIAF component MUST implement it, for both presenting and validating SVIDs, so that any two components always share at least one algorithm.
- A component MAY additionally implement EdDSA (Ed25519), RSA, or both. Whether a peer can accept a presented SVID depends on two kinds of algorithm choice. The signature algorithm of each certificate in the chain is chosen by its issuing CA, and the peer needs it to validate the chain. The public-key algorithm of the leaf key is chosen when the key pair is generated, and the peer needs it to verify the TLS handshake signature. A peer that does not implement every algorithm involved fails to authenticate the presenter. Selecting algorithms supported across the Trust Domain, for the principal's key and for every CA in the chain, is therefore the operator's responsibility at issuance (see [operator provisioning playbook](./identity-lifecycle.md#operator-provisioning-playbook)). ECDSA P-256 with SHA-256 throughout is always a safe choice.
- A component that validates SVIDs MUST validate every algorithm it accepts from peers. For RSA, this includes accepting both PSS and PKCS#1 v1.5 signatures on certificates.

> **Crypto-agility (informative):** MIAF names its algorithms explicitly so the permitted set can evolve. The set above is classical; post-quantum signature suites are expected to arrive as additional permitted algorithms rather than a redesign of the framework. Defaulting the transport to TLS 1.3 (see [TLS requirements](./tls-requirements.md)) supports this: it is the version track on which post-quantum key exchange and authentication are being standardized.

Keys MUST be generated with a cryptographically secure random number generator seeded from an entropy source carrying enough genuine entropy for the key size ([RFC 4086](https://datatracker.ietf.org/doc/html/rfc4086)).

These requirements apply to MIAF-generated artifacts and to the keys used in SVIDs and CSRs. They do not constrain an external bootstrap ecosystem (for example, a manufacturer PKI used as a bootstrap input), which MAY use algorithms permitted by its governing standards, subject to Trust Domain policy.

## X.509-SVID Validation

A verifier authenticates a peer by validating the presented X.509-SVID against the peer's Trust Domain and, on success, treating the SPIFFE ID it carries as the peer's identity. A verifier MUST, in order:

- read the SPIFFE ID from the leaf certificate's **URI SAN** to determine the peer's Trust Domain, and reject the SVID unless that Trust Domain is the verifier's own. DNS hostname matching does not apply to SVID identity and MUST NOT override the SPIFFE ID.
- validate the presented chain against that Trust Domain's [Trust Bundle](./trust-bundle-and-discovery.md), accepting an SVID that chains to any anchor in the current bundle. A bundle MAY contain more than one anchor (for example, during a [trust anchor rotation](./identity-lifecycle.md#trust-anchor-rotation-playbook) overlap), and every anchor in it is equally authoritative. Reject any certificate outside its validity period. A verifier MUST NOT rely on AIA fetching or other out-of-band intermediate retrieval; the presenter supplies the intermediates the chain needs.
- enforce the SPIFFE X.509-SVID leaf constraints and reject any SVID that violates them: basic-constraints `cA` MUST be `false`; `keyCertSign` and `cRLSign` MUST NOT be set in key usage; the SPIFFE ID MUST use the `spiffe` scheme with a non-root path; and the certificate MUST carry exactly one URI SAN.

These leaf constraints, and the other structural rules of the SPIFFE X.509-SVID specification, apply during validation as well as issuance.

On success, the verifier applies its local authorization policy to the verified SPIFFE ID (see [Identity model](./identity-framework.md#identity-model)); MIAF has no central authorization server.
